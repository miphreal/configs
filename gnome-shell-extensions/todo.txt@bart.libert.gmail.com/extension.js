// This extension was developed by Bart Libert
//
// Based on code by :
// * Baptiste Saleil http://bsaleil.org/
// * Arnaud Bonatti https://github.com/Obsidien
//
// Licence: GPLv2+
const St = imports.gi.St;
const PanelMenu = imports.ui.panelMenu;
const PopupMenu = imports.ui.popupMenu;
const Main = imports.ui.main;
const Lang = imports.lang;
const Clutter = imports.gi.Clutter;
const Gio = imports.gi.Gio;
const Extension = imports.misc.extensionUtils.getCurrentExtension();
const JsTodo = Extension.imports.jsTodoTxt;
const JsTextFile = Extension.imports.jsTextFile;
const Lib = Extension.imports.lib;
const Shared = Extension.imports.sharedConstants;
const GLib = imports.gi.GLib;
const JsPacker = Extension.imports.jsPacker;
const EditDialog = Extension.imports.editDialog;
const Meta = imports.gi.Meta;

const Gettext = imports.gettext;
const _ = Gettext.domain('todotxt').gettext;

const schema = "org.gnome.shell.extensions.TodoTxt";
const openKey = 'open-key';
const focusKey = 'open-and-focus-key';

let todoTxt;
let metaData;

// TodoTxtManager function
function TodoTxtManager(metadata) {
    let locales = metadata.path + "/locale";
    Gettext.bindtextdomain('todotxt', locales);

    this._init();
}

// Prototype
TodoTxtManager.prototype = {
    schema: null,
    settings: null,
    autoarchive: false,
    __proto__: PanelMenu.Button.prototype,
    connectedSignals: null,
    tasks: null,
    debugMode: false,
    groupBy: null,
    groupUngrouped: false,
    monitor: null,

    _init: function() {
        PanelMenu.Button.prototype._init.call(this, St.Align.START);

        this.tasks = [];
        this.groupedTasksParameter = [];
        this.groupedTasksParameter[Shared.NO_GROUPING] = "";
        this.groupedTasksParameter[Shared.GROUP_BY_PROJECTS] = "projects";
        this.groupedTasksParameter[Shared.GROUP_BY_CONTEXTS] = "contexts";

        this.buttonText = new St.Label({
            text: _("[...]")
        });
        this.buttonText.set_style("text-align:center;");
        this.actor.add_actor(this.buttonText);
        this.buttonText.get_parent().add_style_class_name("panelButtonWidth");
        this.schema = schema;

        this._initSettings();

        this._loadSettings();

        this._installShortcuts();

        this._refresh();
    },

    _createNewTaskEntry: function() {
        this.newTask = new St.Entry({
            name: "newTaskEntry",
            hint_text: _("New task..."),
            track_hover: true,
            can_focus: true
        });

        let tasksMenu = this.menu;
        let buttonText = this.buttonText;

        let entryNewTask = this.newTask.clutter_text;

        let _this = this;

        entryNewTask.connect('key-press-event', function(o, e) {
            let symbol = e.get_key_symbol();
            if (symbol == Clutter.Return) {
                tasksMenu.close();
                if (o.get_text() === "") {
                    return;
                }
                buttonText.set_text(_("..."));
                let newTask = new JsTodo.TodoTxtItem(o.get_text());
                _this.addTask(newTask);
            }
        });
    },

    _applyPriorityStyling: function(task, item) {
        if (!this.stylePriorities) {
            return;
        }
        let markup = this.prioritiesMarkup[task.priority];
        if (markup == null) {
            return;
        }
        let style = "";
        if (markup[Shared.STYLE_CHANGE_COLOR] === true) {
            style = style + 'color:' + markup[Shared.STYLE_COLOR] + ';';
        }
        if (markup[Shared.STYLE_BOLD] === true) {
            style = style + 'font-weight: bold;';
        }
        if (markup[Shared.STYLE_ITALIC] === true) {
            style = style + 'font-style: italic;';
        }
        item.actor.set_style(style);
    },

    _addLabel: function(task, labelSource, item) {
        let label = new St.Label({
            text: ""
        });
        if (task[labelSource] !== null) {
            label.set_text(task[labelSource].join());
        }
        item.addActor(label);
    },

    _addProjectsLabel: function(task, item) {
        if (this.showProjectsLabel) {
            this._addLabel(task, "projects", item);
        }
    },

    _addContextsLabel: function(task, item) {
        if (this.showContextsLabel) {
            this._addLabel(task, "contexts", item);
        }
    },

    _createButton: function(icon) {
        let button = new St.Button({
            child: new St.Icon({
                icon_name: icon,
                icon_size: 16
            })
        });
        return button;
    },

    _addDoneButton: function(task, item) {
        let doneButton = this._createButton('object-select-symbolic');
        let _this = this;
        doneButton.connect('clicked', function() {
            _this.buttonText.set_text("[...]");
            _this.completeTask(task);
        });
        item.addActor(doneButton);
    },

    _addArchiveButton: function(task, item) {
        let archiveButton = this._createButton('document-save-symbolic');
        let _this = this;
        archiveButton.connect('clicked', function() {
            _this.buttonText.set_text("[...]");
            _this.archiveTask(task);
        });
        item.actor.add_style_class_name("doneTaskItem");
        item.addActor(archiveButton);
    },

    _addDeleteButton: function(task, item) {
        let deleteButton = this._createButton('edit-delete-symbolic');
        let _this = this;
        deleteButton.connect('clicked', function() {
            _this.buttonText.set_text("[...]");
            _this.removeTask(task);
        });
        item.addActor(deleteButton);
    },

    _addEditButton: function(task, item) {
        let editButton = this._createButton('input-keyboard-symbolic');
        let _this = this;
        editButton.connect('clicked', function() {
            _this._launchEditDialog(task);
        });
        item.addActor(editButton);
    },

    _addButtons: function(task, item) {
        if (this.showDoneButton) {
            if (!task.complete) {
                this._addDoneButton(task, item);
            }
            else {
                this._addArchiveButton(task, item);
            }
        }
        if (this.showDeleteButton) {
            this._addDeleteButton(task, item);
        }
        if (this.showEditButton) {
            this._addEditButton(task, item);
        }
    },

    _launchEditDialog: function(task) {
        let oldTask = task;
        let _this = this;
        let editDialog = new EditDialog.EditDialog(function(newTask) {
            _this.modifyTask(oldTask, newTask, true);
        });
        editDialog.open(task.toString());
    },

    _createTodoItem: function(task) {
        let item = new PopupMenu.PopupMenuItem(task.text);
        this._addProjectsLabel(task, item);
        this._addContextsLabel(task, item);
        this._addButtons(task, item);
        this._applyPriorityStyling(task, item);
        if (this.clickAction == Shared.CLICK_ACTION_NONE) {
            return item;
        }
        let _this = this;
        item.connect('activate', function() {
            switch (_this.clickAction) {
            case Shared.CLICK_ACTION_EDIT:
                _this._launchEditDialog(task);
                break;
            case Shared.CLICK_ACTION_DONE:
                _this.completeTask(task);
                break;
            }
        });
        return item;
    },

    _initSettings: function() {
        let settings = new Lib.Settings(this.schema);
        this.settings = settings.getSettings();
    },

    _loadSettings: function() {
        this.todofile = this.settings.get_string("todotxt-location").replace("$HOME", GLib.get_home_dir()).replace("~", GLib.get_home_dir());
        this.donefile = this.settings.get_string("donetxt-location").replace("$HOME", GLib.get_home_dir()).replace("~", GLib.get_home_dir());
        this.autoarchive = this.settings.get_boolean("auto-archive");
        this.debugMode = this.settings.get_boolean("debug-mode");
        this.groupBy = this.settings.get_int("group-by");
        this.groupUngrouped = this.settings.get_boolean("group-ungrouped");
        let prioritiesRawValue = this.settings.get_value("priorities-markup");
        this.prioritiesMarkup = {};
        JsPacker.unpack_priorities_dictionary(prioritiesRawValue, this.prioritiesMarkup);
        this.showDoneButton = this.settings.get_boolean("show-done-or-archive-button");
        this.showDeleteButton = this.settings.get_boolean("show-delete-button");
        this.showProjectsLabel = this.settings.get_boolean("show-projects-label");
        this.showContextsLabel = this.settings.get_boolean("show-contexts-label");
        this.showNewTaskEntry = this.settings.get_boolean("show-new-task-entry");
        this.stylePriorities = this.settings.get_boolean("style-priorities");
        this.addCreationDate = this.settings.get_boolean("add-creation-date");
        this.showEditButton = this.settings.get_boolean("show-edit-button");
        this.clickAction = this.settings.get_int("click-action");
        this.openKey = this.settings.get_string("open-key");
        this.focusKey = this.settings.get_string("open-and-focus-key");
    },

    _connectSettingsSignals: function() {
        if (this.connectedSignals === null) {
            this.connectedSignals = [];
            this.connectedSignals.push(this.settings.connect("changed::auto-archive", Lang.bind(this, this.onParamChanged)));
            this.connectedSignals.push(this.settings.connect("changed::todotxt-location", Lang.bind(this, this.onTodoFileChanged)));
            this.connectedSignals.push(this.settings.connect("changed::donetxt-location", Lang.bind(this, this.onParamChanged)));
            this.connectedSignals.push(this.settings.connect("changed::debug-mode", Lang.bind(this, this.onParamChanged)));
            this.connectedSignals.push(this.settings.connect("changed::group-by", Lang.bind(this, this.onParamChanged)));
            this.connectedSignals.push(this.settings.connect("changed::group-ungrouped", Lang.bind(this, this.onParamChanged)));
            this.connectedSignals.push(this.settings.connect("changed::priorities-markup", Lang.bind(this, this.onParamChanged)));
            this.connectedSignals.push(this.settings.connect("changed::show-done-or-archive-button", Lang.bind(this, this.onParamChanged)));
            this.connectedSignals.push(this.settings.connect("changed::show-delete-button", Lang.bind(this, this.onParamChanged)));
            this.connectedSignals.push(this.settings.connect("changed::show-projects-label", Lang.bind(this, this.onParamChanged)));
            this.connectedSignals.push(this.settings.connect("changed::show-contexts-label", Lang.bind(this, this.onParamChanged)));
            this.connectedSignals.push(this.settings.connect("changed::show-new-task-entry", Lang.bind(this, this.onParamChanged)));
            this.connectedSignals.push(this.settings.connect("changed::style-priorities", Lang.bind(this, this.onParamChanged)));
            this.connectedSignals.push(this.settings.connect("changed::add-creation-date", Lang.bind(this, this.onParamChanged)));
            this.connectedSignals.push(this.settings.connect("changed::show-edit-button", Lang.bind(this, this.onParamChanged)));
            this.connectedSignals.push(this.settings.connect("changed::click-action", Lang.bind(this, this.onParamChanged)));
            this.connectedSignals.push(this.settings.connect("changed::open-key", Lang.bind(this, this.onShortcutChanged)));
            this.connectedSignals.push(this.settings.connect("changed::open-and-focus-key", Lang.bind(this, this.onShortcutChanged)));
        }
    },

    _refresh: function() {
        let tasksMenu = this.menu;
        let buttonText = this.buttonText;

        this._createNewTaskEntry();

        // Clear
        tasksMenu.removeAll();

        // Sync
        let todoFile = new JsTextFile.JsTextFile(this.todofile);
        if (!todoFile.exists()) {
            return false;
        }

        this._createTasksFromFile(todoFile.getLines());

        this._createTasksMenu();

        buttonText.set_text("[" + this.tasks.length + "]");
        if (this.tasks.length < 10) {
            buttonText.get_parent().add_style_class_name("panelButtonWidth");
        }
        else {
            buttonText.get_parent().remove_style_class_name("panelButtonWidth");
        }

        // Separator
        this.Separator = new PopupMenu.PopupSeparatorMenuItem();
        tasksMenu.addMenuItem(this.Separator);

        if (!this.showNewTaskEntry) {
            return true;
        }
        // Bottom section
        let bottomSection = new PopupMenu.PopupMenuSection();

        bottomSection.actor.add_actor(this.newTask);
        bottomSection.actor.add_style_class_name("newTaskSection");
        tasksMenu.addMenuItem(bottomSection);
        return true;
    },

    _createTasksMenu: function() {
        if (this.groupBy == Shared.NO_GROUPING) {
            this.tasks.sort(this.sortByPriority);
            for (let i = 0; i < this.tasks.length; i++) {
                let item = this._createTodoItem(this.tasks[i]);
                this.menu.addMenuItem(item);
            }
            return;
        }
        let groupedTasks = {};
        for (let i = 0; i < this.tasks.length; i++) {
            this._createGroupedTask(this.tasks[i], groupedTasks);
        }
        for (let groupArray in groupedTasks) {
            if (groupedTasks.hasOwnProperty(groupArray)) {
                groupedTasks[groupArray].sort(this.sortByPriority);
            }
        }
        for (let group in groupedTasks) {
            if (groupedTasks.hasOwnProperty(group)) {
                if (group == "__nogroup__") {
                    if (this.groupUngrouped) {
                        var groupItem = new PopupMenu.PopupSubMenuMenuItem(_("Ungrouped"));
                    }
                    else {
                        var groupItem = this;
                    }
                }
                else {
                    var groupItem = new PopupMenu.PopupSubMenuMenuItem(group);
                }
                for (let i = 0; i < groupedTasks[group].length; i++) {
                    let item = this._createTodoItem(groupedTasks[group][i]);
                    groupItem.menu.addMenuItem(item);
                }
                if (groupItem != this) {
                    this.menu.addMenuItem(groupItem);
                }
            }
        }
    },

    _createTasksFromFile: function(lines) {
        this.tasks.length = 0;
        for (let i = 0; i < lines.length; i++) {
            if (lines[i] !== '' && lines[i] != '\n') {
                try {
                    let task = new JsTodo.TodoTxtItem(lines[i]);
                    this.tasks.push(task);
                }
                catch(exception) {
                    this.debug("Error while reading task: " + exception.message);
                }
            }

        }
    },

    _createGroupedTask: function(task, groupedTasks) {
        let groups = task[this.groupedTasksParameter[this.groupBy]];
        if (groups === null) {
            groups = ['__nogroup__'];
        }
        for (let group in groups) {
            if (typeof groupedTasks[groups[group]] == 'undefined') {
                groupedTasks[groups[group]] = [task];
            }
            else {
                groupedTasks[groups[group]].push(task);
            }
        }
    },

    _get_symlink_target_absolute: function(symlinkGFile) {
        this.debug("Getting absolute path for symlink " + symlinkGFile.get_path());
        let parentDir = symlinkGFile.get_parent();
        if (parentDir === null) {
            parentDir = Gio.file_new_for_path("/");
        }
        let symlinkTarget = symlinkGFile.query_info("standard::symlink-target", 0, null).get_symlink_target();
        return parentDir.resolve_relative_path(symlinkTarget);
    },

    _linkChanged: function() {
        if (this._monitorFile()) {
            this._refresh();
        }
    },

    _get_g_file_for_path: function(path) {
        let gFile = Gio.file_new_for_path(path);
        if (gFile.query_info("standard::is-symlink", 0, null).get_is_symlink()) {
            this.linkMonitor = gFile.monitor(Gio.FileMonitorFlags.NONE, null);
            this.linkMonitor.connect('changed', Lang.bind(this, this._linkChanged));
            return this._get_symlink_target_absolute(gFile);
        }
        return gFile;
    },

    _monitorFile: function() {
        let jsTextFile = new JsTextFile.JsTextFile(this.todofile);
        if (jsTextFile.exists()) {
            this._cancel_monitors();
            this.debug("File found: " + this.todofile);
            let fileM = this._get_g_file_for_path(this.todofile);
            this.debug("Monitoring " + fileM.get_path());
            this.monitor = fileM.monitor(Gio.FileMonitorFlags.NONE, null);
            this.monitor.connect('changed', Lang.bind(this, this._refresh));
            return true;
        }
        else {
            this.buttonText.set_text("[X]");
            let errorItem = new PopupMenu.PopupMenuItem(_("No valid todo.txt file specified"));
            let chooseItem = new PopupMenu.PopupMenuItem("> " + _("Select location in settings"));
            chooseItem.connect('activate', Lang.bind(this, function() {
                var runPrefs = 'gnome-shell-extension-prefs ' + Extension.metadata.uuid;
                Main.Util.trySpawnCommandLine(runPrefs);
            }));
            let createPath = GLib.build_pathv('/', [GLib.get_user_data_dir(), 'todo.txt']);
            let createItem = new PopupMenu.PopupMenuItem("> " + _("Create todo.txt and done.txt file in ") + createPath);
            createItem.connect('activate', Lang.bind(this, function() {
                GLib.mkdir_with_parents(createPath, 493);
                let todoPath = GLib.build_filenamev([createPath, 'todo.txt']);
                let donePath = GLib.build_filenamev([createPath, 'done.txt']);
                GLib.file_set_contents(todoPath, '');
                GLib.file_set_contents(donePath, '');
                this.settings.set_string("todotxt-location", todoPath);
                this.settings.set_string("donetxt-location", donePath);
            }));
            this.menu.removeAll();
            this.menu.addMenuItem(errorItem);
            this.menu.addMenuItem(chooseItem);
            this.menu.addMenuItem(createItem);
            return false;
        }
    },

    _enable: function() {
        let menuManager = Main.panel._menus || Main.panel.menuManager;
        menuManager.addMenu(this.menu);

        this._monitorFile();
        this._connectSettingsSignals();
    },

    _cancel_monitors: function() {
        if (this.monitor !== null) {
            this.monitor.cancel();
        }
        if (this.linkMonitor != null) {
            this.linkMonitor.cancel();
        }
    },

    _disable: function() {
        let menuManager = Main.panel._menus || Main.panel.menuManager;
        menuManager.removeMenu(this.menu);
        this._cancel_monitors();
        global.display.remove_keybinding(openKey);
        global.display.remove_keybinding(focusKey);
        let letSettings = this.settings;
        if (this.connectedSignals !== null) {
            this.connectedSignals.forEach(
            function(signal) {
                if (signal) {
                    letSettings.disconnect(signal);
                }
            }

            );
        }
        this.connectedSignals = null;
    },

    onTodoFileChanged: function() {
        this._loadSettings();
        if (this.monitor !== null) {
            this.monitor.cancel();
        }
        if (this._monitorFile()) {
            this.debug("Refresh");
            this._refresh();
            return;
        }
        // If the file is invalid, connect to the signals to cover change to valid one
        this._connectSettingsSignals();
    },

    onParamChanged: function() {
        this._loadSettings();
        this._refresh();
    },

    _installShortcuts: function() {
		global.display.add_keybinding
		(
			openKey,
			this.settings,
			Meta.KeyBindingFlags.NONE,
			Lang.bind(this, function() {
                this.menu.open();
            })
		);
		global.display.add_keybinding
		(
			focusKey,
			this.settings,
			Meta.KeyBindingFlags.NONE,
			Lang.bind(this, function() {
                this.menu.open();
                this.newTask.grab_key_focus();
            })
		);
    },

    onShortcutChanged: function() {
        global.display.remove_keybinding(this.openKey);
        global.display.remove_keybinding(this.focusKey);
        this._loadSettings();
    },

    removeTask: function(task) {
        let index = this.tasks.indexOf(task);
        if (index == - 1) {
            this.debug("Task not found");
            return false;
        }
        this.tasks.splice(index, 1);
        return this.saveTasksToFile();
    },

    addTask: function(task) {
        if (this.addCreationDate) {
            task.date = new Date();
        }
        this.tasks.push(task);
        return this.saveTasksToFile();
    },

    modifyTask: function(oldTask, newTask, save) {
        let index = this.tasks.indexOf(oldTask);
        if (index == - 1) {
            this.debug("Task not found");
            return false;
        }
        this.tasks[index] = newTask;
        if (save) {
            return this.saveTasksToFile();
        }
        return true;
    },

    completeTask: function(task) {
        let doneTask = new JsTodo.TodoTxtItem(task.toString());
        doneTask.complete = true;
        doneTask.completed = new Date();
        // Modify tasks list, but don't save yet
        if (!this.modifyTask(task, doneTask, false)) {
            return false;
        }
        // If autoarchive is on, archive task and save both files
        if (this.autoarchive) {
            return this.archiveTask(doneTask);
        }
        // If autoarchive is off, only save todo.txt file
        return this.saveTasksToFile();
    },

    archiveTask: function(task) {
        if (!task.complete) {
            this.debug("archiveTask: trying to archive task that is not done");
            return false;
        }
        let jsTextFile = new JsTextFile.JsTextFile(this.donefile);
        if (!jsTextFile.addLine(task.toString())) {
            this.debug("Could not add task to done file");
        }
        if (!jsTextFile.saveFile(true)) {
            this.debug("Could not save done file");
        }
        return this.removeTask(task);
    },

    saveTasksToFile: function() {
        let jsTextFile = new JsTextFile.JsTextFile(this.todofile);
        let textArray = [];
        for (let i = 0; i < this.tasks.length; i++) {
            textArray[i] = this.tasks[i].toString();
        }
        jsTextFile.setLines(textArray);
        return jsTextFile.saveFile(true);
    },

    debug: function(text) {
        if (this.debugMode) {
            global.log("[todo.txt] " + text + "\n");
        }
    },

    sortByPriority: function(a, b) {
        if (a.priority === null) {
            if (b.priority === null) {
                return 0;
            }
            // Convention: "null" has smaller priority then everything else
            return 1;
        }
        if (b.priority === null) {
            // Case a==null, b==null already covered
            return - 1;
        }
        return (a.priority.charCodeAt(0) - b.priority.charCodeAt(0));
    }
};

// Init function
function init(metadata) {
    metaData = metadata;
}

function enable() {
    todoTxt = new TodoTxtManager(metaData);
    todoTxt._enable();
    Main.panel.addToStatusArea('todoTxt', todoTxt);
}

function disable() {
    todoTxt._disable();
    todoTxt.destroy();
    todoTxt = null;
}

/* vi: set expandtab tabstop=4 shiftwidth=4: */

