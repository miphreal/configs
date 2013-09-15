const Gtk = imports.gi.Gtk;
const Lang = imports.lang;

const Extension = imports.misc.extensionUtils.getCurrentExtension();
const Lib = Extension.imports.lib;
const Shared = Extension.imports.sharedConstants;
const JsPacker = Extension.imports.jsPacker;
const Gdk = imports.gi.Gdk;
const GObject = imports.gi.GObject;
const ButtonCellRenderer = Extension.imports.buttonCellRenderer;

const Gettext = imports.gettext.domain('todotxt');
const _ = Gettext.gettext;

const schema = "org.gnome.shell.extensions.TodoTxt";

const COL_PRIORITY = 0;
const COL_CHANGE_COLOR = 1;
const COL_COLOR = 2;
const COL_BOLD = 3;
const COL_ITALIC = 4;

const shortcuts = {
    "open-key": _("Open task list"),
    "open-and-focus-key": _("Open task list and focus new task entry")
};

function init() {

}

function buildPrefsWidget() {
    let prefs = new Prefs(schema);
    return prefs.buildPrefsWidget();
}

function Prefs(schema) {
    this.init(schema);
}

Prefs.prototype = {
    settings: null,
    hboxsList: [],

    init: function(schema) {
        let settings = new Lib.Settings(schema);
        this.settings = settings.getSettings();
    },

    launchFileChooser: function(caller, entryTarget, title) {
        let dialogTitle = _("Select file");
        if (title !== null) {
            dialogTitle = title;
        }
        let chooser = new Gtk.FileChooserDialog({
            title: dialogTitle,
            action: Gtk.FileChooserAction.OPEN,
            modal: true
        });

        chooser.add_button(Gtk.STOCK_CANCEL, 0);
        chooser.add_button(Gtk.STOCK_OPEN, 1);
        chooser.set_default_response(1);
        let filename = null;
        if (chooser.run() == 1) {
            filename = chooser.get_filename();
            if (filename) {
                entryTarget.set_text(filename);
            }
        }
        chooser.destroy();
    },

    checkForDuplicatePriorities: function(model) {
        let seenPriorities = [];
        let [validIterator, iter] = model.get_iter_first();
        while (validIterator) {
            let priority = model.get_value(iter, COL_PRIORITY);
            if (seenPriorities.indexOf(priority) == -1) {
                seenPriorities.push(priority);
            }
            else {
                let dialog = new Gtk.MessageDialog({
                    buttons: Gtk.ButtonsType.OK,
                    text: _("Duplicate priority: ") + priority,
                    message_type: Gtk.MessageType.ERROR
                });
                dialog.run();
                dialog.destroy();
                return false;
            }
            validIterator = model.iter_next(iter);
        }
        return true;
    },

    checkForInvalidPriorities: function(model) {
        return this.checkPriorityCondition(model, function(priority) {
            return (/^[A-Z]$/).test(priority);
        },
        _("Wrong priority"));
    },

    checkPriorityCondition: function(model, check_function, message) {
        let [validIterator, iter] = model.get_iter_first();
        let result = true;
        let priority = "@";
        while (validIterator && result) {
            priority = model.get_value(iter, COL_PRIORITY);
            result = check_function(priority);
            validIterator = model.iter_next(iter);
        }
        if (!result) {
            let dialog = new Gtk.MessageDialog({
                buttons: Gtk.ButtonsType.OK,
                text: message + ": " + priority,
                message_type: Gtk.MessageType.ERROR
            });
            dialog.run();
            dialog.destroy();
            return false;
        }
        return true;
    },

    validateModel: function(model) {
        if (!this.checkForDuplicatePriorities(model)) {
            return false;
        }
        if (!this.checkForInvalidPriorities(model)) {
            return false;
        }
        return true;
    },

    updatePriorityStylingFromModelRow: function(model, row, replace_prio) {
        if (!this.validateModel(model)) {
            model.remove(row);
            return;
        }
        this.updatePriorityStyling(
        model.get_value(row, COL_PRIORITY), model.get_value(row, COL_CHANGE_COLOR), model.get_value(row, COL_COLOR), model.get_value(row, COL_BOLD), model.get_value(row, COL_ITALIC), replace_prio);
    },

    updatePriorityStyling: function(priority, change_color, color, bold, italic, replace_prio) {
        if (priority === null) {
            log("Priority can not be null");
            return;
        }
        var currentValue = this.prioritiesMarkup[priority];
        if (currentValue === undefined) {
            // create new tuple with default values
            currentValue = [false, "rgb(255,255,255)", false, false];
            this.prioritiesMarkup[priority] = currentValue;
        }
        if (change_color !== null) {
            if (change_color === true) {
                if (color !== null) {
                    currentValue[Shared.STYLE_COLOR] = color;
                }
            }
            currentValue[Shared.STYLE_CHANGE_COLOR] = change_color;
        }
        if (bold !== null) {
            currentValue[Shared.STYLE_BOLD] = bold;
        }
        if (italic !== null) {
            currentValue[Shared.STYLE_ITALIC] = italic;
        }
        if (replace_prio != priority) {
            if (replace_prio != null) {
                delete this.prioritiesMarkup[replace_prio];
            }
        }
        this.settings.set_value("priorities-markup", JsPacker.pack_priorities_dictionary(this.prioritiesMarkup));
    },

    removePriorityStyle: function(priority) {
        if (priority === null) {
            log("Priority can not be null");
            return;
        }
        delete this.prioritiesMarkup[priority];
        this.settings.set_value("priorities-markup", JsPacker.pack_priorities_dictionary(this.prioritiesMarkup));
    },

    buildLocationSettings: function(parentContainer, text, setting, description) {
        let locationHbox = new Gtk.Box({
            orientation: Gtk.Orientation.HORIZONTAL
        });
        let locationLabel = new Gtk.Label({
            label: text,
            xalign: 0
        });
        let locationValue = new Gtk.Entry({
            hexpand: true
        });
        locationValue.set_text(this.settings.get_string(setting));
        let locationBrowse = new Gtk.Button({
            label: _("Browse")
        });
        locationBrowse.connect("clicked", Lang.bind(this, this.launchFileChooser, locationValue, description));
        let locationApply = new Gtk.Button({
            label: _("Apply")
        });
        let _this = this;
        locationApply.connect("clicked", Lang.bind(this, function(object) {
            log("Setting " + setting + " to " + locationValue.get_text());
            _this.settings.set_string(setting, locationValue.get_text());
        }));
        locationHbox.pack_start(locationLabel, true, true, 0);
        locationHbox.add(locationValue);
        locationHbox.add(locationBrowse);
        locationHbox.add(locationApply);

        parentContainer.add(locationHbox);
    },

    buildFilesSettings: function(parentContainer) {
        let label = new Gtk.Label({
            label: _("<b>Files</b>"),
            use_markup: true,
            xalign: 0
        });
        let vbox = new Gtk.Box({
            orientation: Gtk.Orientation.VERTICAL,
            margin_left: 20
        });

        this.buildLocationSettings(vbox, _("Todo.txt location"), "todotxt-location", _("Select location of todo.txt file"));
        this.buildLocationSettings(vbox, _("Done.txt location"), "donetxt-location", _("Select location of done.txt file"));

        parentContainer.add(label);
        parentContainer.add(vbox);
    },

    buildSettingsSwitch: function(parentContainer, labelText, setting) {
        let switchHbox = new Gtk.Box({
            orientation: Gtk.Orientation.HORIZONTAL
        });
        let switchLabel = new Gtk.Label({
            label: labelText,
            xalign: 0
        });
        let settingsSwitch = new Gtk.Switch({
            active: this.settings.get_boolean(setting)
        });
        let _this = this;
        settingsSwitch.connect('notify::active', Lang.bind(this, function(object) {
            log("changing boolean " + setting + " to " + object.active);
            _this.settings.set_boolean(setting, object.active);
        }));
        switchHbox.pack_start(switchLabel, true, true, 0);
        switchHbox.add(settingsSwitch);
        parentContainer.add(switchHbox);
    },

    buildComboBox: function(parentContainer, labelText, setting, options) {
        if (options === null) {
            return;
        }
        let comboHbox = new Gtk.Box({
            orientation: Gtk.Orientation.HORIZONTAL
        });
        let comboLabel = new Gtk.Label({
            label: labelText,
            xalign: 0
        });
        let comboBox = new Gtk.ComboBoxText();
        if (options.length === 0) {
            comboBox.sensitive = false;
        }
        for (let i = 0; i < options.length; i++) {
            comboBox.insert_text(i, options[i]);
            if (i === this.settings.get_int(setting)) {
                comboBox.set_active(i);
            }
        }
        let _this = this;
        comboBox.connect('changed', Lang.bind(this, function(object) {
            log("changing " + setting + " to " + object.get_active() + " (" + options[object.get_active()] + ")");
            _this.settings.set_int(setting, object.get_active());
        }));
        comboHbox.pack_start(comboLabel, true, true, 0);
        comboHbox.add(comboBox);
        parentContainer.add(comboHbox);
    },

    buildAcceleratorSettings: function(parentContainer) {
        let label = new Gtk.Label({
            label: _("<b>Shortcuts</b>"),
            use_markup: true,
            xalign: 0
        });
        parentContainer.add(label);
        let model = new Gtk.ListStore();
        model.set_column_types([
        GObject.TYPE_STRING, GObject.TYPE_STRING, GObject.TYPE_INT, GObject.TYPE_INT]);

        for (let shortcut in shortcuts) {
            if(shortcuts.hasOwnProperty(shortcut)) {
                let row = model.insert(10);
                let[key, mods] = Gtk.accelerator_parse(this.settings.get_strv(shortcut)[0]);
                model.set(row, [0, 1, 2, 3], [shortcut, shortcuts[shortcut], mods, key]);
            }
        }

        let treeview = new Gtk.TreeView({
            'expand': true,
            'model': model
        });

        let cellrend = new Gtk.CellRendererText();
        let col = new Gtk.TreeViewColumn({
            'title': _('Function'),
            'expand': true
        });

        col.pack_start(cellrend, true);
        col.add_attribute(cellrend, 'text', 1);

        treeview.append_column(col);

        cellrend = new Gtk.CellRendererAccel({
            'editable': true,
            'accel-mode': Gtk.CellRendererAccelMode.GTK
        });
        let _this = this;
        cellrend.connect('accel-edited', function(rend, iter, key, mods) {
            let value = Gtk.accelerator_name(key, mods);

            let[succ, iterator] = model.get_iter_from_string(iter);

            if (!succ) {
                throw new Error("Something is broken!");
            }

            let name = model.get_value(iterator, 0);

            model.set(iterator, [2, 3], [mods, key]);

            _this.settings.set_strv(name, [value]);
        });

        cellrend.connect('accel-cleared', function(rend, iter) {
            let[succ, iterator] = model.get_iter_from_string(iter);

            if (!succ) {
                throw new Error("Something is broken!");
            }

            model.set(iterator, [3], [0]);
            let name = model.get_value(iterator, 0);
            _this.settings.set_strv(name, ['']);
        });

        col = new Gtk.TreeViewColumn({
            'title': _('Key')
        });

        col.pack_end(cellrend, false);
        col.add_attribute(cellrend, 'accel-mods', 2);
        col.add_attribute(cellrend, 'accel-key', 3);

        treeview.append_column(col);

        parentContainer.add(treeview);

    },

    buildGeneralSettings: function(parentContainer) {
        let label = new Gtk.Label({
            label: _("<b>General</b>"),
            use_markup: true,
            xalign: 0
        });
        let vbox = new Gtk.Box({
            orientation: Gtk.Orientation.VERTICAL,
            margin_left: 20
        });

        this.buildSettingsSwitch(vbox, _("Auto-archive done tasks"), "auto-archive");
        this.buildSettingsSwitch(vbox, _("Auto-add creation date to new tasks"), "add-creation-date");
        let options = [];
        options[Shared.CLICK_ACTION_EDIT] = _("Edit task");
        options[Shared.CLICK_ACTION_DONE] = _("Mark task as done or archive task");
        options[Shared.CLICK_ACTION_NONE] = _("Nothing");
        this.buildComboBox(vbox, _("Action on clicking task"), "click-action", options);
        this.buildSettingsSwitch(vbox, _("Debug mode"), "debug-mode");

        parentContainer.add(label);
        parentContainer.add(vbox);
    },

    buildGroupingSettings: function(parentContainer) {
        let label = new Gtk.Label({
            label: _("<b>Grouping</b>"),
            use_markup: true,
            xalign: 0
        });
        let vbox = new Gtk.Box({
            orientation: Gtk.Orientation.VERTICAL,
            margin_left: 20
        });

        let options = [];
        options[Shared.NO_GROUPING] = _("No grouping");
        options[Shared.GROUP_BY_PROJECTS] = _("Projects");
        options[Shared.GROUP_BY_CONTEXTS] = _("Contexts");
        this.buildComboBox(vbox, _("Group tasks by"), "group-by", options);
        this.buildSettingsSwitch(vbox, _("Put ungrouped tasks in seperate group"), "group-ungrouped");

        parentContainer.add(label);
        parentContainer.add(vbox);
    },

    buildShowHideElementsSettings: function(parentContainer) {
        let label = new Gtk.Label({
            label: _("<b>Show/hide elements</b>"),
            use_markup: true,
            xalign: 0
        });
        let vbox = new Gtk.Box({
            orientation: Gtk.Orientation.VERTICAL,
            margin_left: 20
        });

        this.buildSettingsSwitch(vbox, _("Show done/archive task button"), "show-done-or-archive-button");
        this.buildSettingsSwitch(vbox, _("Show delete task button"), "show-delete-button");
        this.buildSettingsSwitch(vbox, _("Show edit task button"), "show-edit-button");
        this.buildSettingsSwitch(vbox, _("Show projects"), "show-projects-label");
        this.buildSettingsSwitch(vbox, _("Show contexts"), "show-contexts-label");
        this.buildSettingsSwitch(vbox, _("Show new task entry"), "show-new-task-entry");

        parentContainer.add(label);
        parentContainer.add(vbox);
    },

    buildPrioritiesSettings: function(parentContainer) {
        let label = new Gtk.Label({
            label: _("<b>Priorities display</b>"),
            use_markup: true,
            xalign: 0
        });
        let vbox = new Gtk.Box({
            orientation: Gtk.Orientation.VERTICAL,
            margin_left: 20
        });

        this.buildSettingsSwitch(vbox, _("Style priorities"), "style-priorities");

        parentContainer.add(label);
        parentContainer.add(vbox);
    },

    buildGeneralTab: function(notebook) {
        let page = new Gtk.Box({
            orientation: Gtk.Orientation.VERTICAL,
            border_width: 10,
            vexpand: true
        });
        let title = new Gtk.Label({
            label: _("General")
        });
        this.buildFilesSettings(page);
        this.buildGeneralSettings(page);
        this.buildAcceleratorSettings(page);
        notebook.append_page(page, title);
    },

    buildDisplayTab: function(notebook) {
        let page = new Gtk.Box({
            orientation: Gtk.Orientation.VERTICAL,
            border_width: 10,
            vexpand: true
        });
        let title = new Gtk.Label({
            label: _("Display")
        });
        this.buildGroupingSettings(page);
        this.buildShowHideElementsSettings(page);
        notebook.append_page(page, title);
    },

    buildPriorityStyleWidget: function(model, row, priority, change_color, color, bold, italic) {
        let newRow = model.insert(row);
        model.set(newRow, [COL_PRIORITY, COL_CHANGE_COLOR, COL_COLOR, COL_BOLD, COL_ITALIC], [priority, change_color, color, bold, italic]);
    },

    buildPrioritiesFromSettings: function(parentContainer, startRow) {
        let prioritiesRawValue = this.settings.get_value("priorities-markup");
        this.prioritiesMarkup = {};
        JsPacker.unpack_priorities_dictionary(prioritiesRawValue, this.prioritiesMarkup);
        let i = 1;
        for (let markup in this.prioritiesMarkup) {
            if (this.prioritiesMarkup.hasOwnProperty(markup)) {
                this.buildPriorityStyleWidget(parentContainer, startRow + i, markup, this.prioritiesMarkup[markup][Shared.STYLE_CHANGE_COLOR], this.prioritiesMarkup[markup][Shared.STYLE_COLOR], this.prioritiesMarkup[markup][Shared.STYLE_BOLD], this.prioritiesMarkup[markup][Shared.STYLE_ITALIC]);
                i = i + 1;
            }
        }
        return i;
    },

    buildToggleColumn: function(title, attribute_column, model) {
        let column = new Gtk.TreeViewColumn({
            'title': title,
            'expand': true
        });

        let renderer = new Gtk.CellRendererToggle({
            activatable: true
        });
        let _this = this;
        renderer.connect('toggled', function(rend, iter) {
            let newActiveState = ! rend.active;
            let[returnCode, row] = model.get_iter_from_string(iter);
            if (!returnCode) {
                throw new Error("Something is broken!");
            }
            model.set(row, [attribute_column], [newActiveState]);
            _this.updatePriorityStylingFromModelRow(model, row);
        });
        column.pack_start(renderer, true);
        column.add_attribute(renderer, 'active', attribute_column);
        return column;
    },

    buildPrioritiesStyleScroller: function(parentContainer) {
        let label = new Gtk.Label({
            label: _("<b>Styles</b>"),
            use_markup: true,
            xalign: 0
        });
        let scroller = new Gtk.ScrolledWindow();
        let model = new Gtk.ListStore();
        model.set_column_types([
        GObject.TYPE_STRING, GObject.TYPE_BOOLEAN, GObject.TYPE_STRING, GObject.TYPE_BOOLEAN, GObject.TYPE_BOOLEAN]);
        let nextRow = this.buildPrioritiesFromSettings(model, 1);

        let treeview = new Gtk.TreeView({
            'expand': true,
            'model': model
        });

        let prioCol = new Gtk.TreeViewColumn({
            'title': _('Priority'),
            'expand': true,
            'sort-indicator': true,
            'sort-column-id': COL_PRIORITY,
        });

        let prioRend = new Gtk.CellRendererText({
            editable: true
        });
        let _this = this;
        prioRend.connect('edited', function(rend, iter, newPrio) {
            let[returnCode, row] = model.get_iter_from_string(iter);
            if (!returnCode) {
                throw new Error("Something is broken!");
            }
            let oldPrio = model.get_value(row, [COL_PRIORITY]);
            model.set(row, [COL_PRIORITY], [newPrio]);
            _this.updatePriorityStylingFromModelRow(model, row, oldPrio);
        });
        prioCol.pack_start(prioRend, true);
        prioCol.add_attribute(prioRend, 'text', COL_PRIORITY);

        treeview.append_column(prioCol);

        treeview.append_column(this.buildToggleColumn('Change color', COL_CHANGE_COLOR, model));

        let colorCol = new Gtk.TreeViewColumn({
            'title': _('Color'),
            'expand': true,
        });

        let colorRend = new ButtonCellRenderer.ButtonCellRenderer({
            activatable: true
        });
        colorRend.connect('clicked', function(rend, iter) {
            let[returnCode, row] = model.get_iter_from_string(iter);
            if (!returnCode) {
                throw new Error("Something is broken!");
            }
            let oldColor = new Gdk.RGBA();
            oldColor.parse(model.get_value(row, [COL_COLOR]));
            let colorChooser = new Gtk.ColorChooserDialog({
                modal: true,
                rgba: oldColor
            });
            if (colorChooser.run() == Gtk.ResponseType.OK) {
                let newColor = new Gdk.RGBA();
                colorChooser.get_rgba(newColor);
                model.set(row, [COL_COLOR], [newColor.to_string()]);
                _this.updatePriorityStylingFromModelRow(model, row);
            }
            colorChooser.destroy();
        });
        colorCol.pack_start(colorRend, true);
        colorCol.add_attribute(colorRend, 'cell-background', COL_COLOR);
        colorCol.add_attribute(colorRend, 'sensitive', COL_CHANGE_COLOR);
        treeview.append_column(colorCol);

        treeview.append_column(this.buildToggleColumn('Bold', COL_BOLD, model));
        treeview.append_column(this.buildToggleColumn('Italic', COL_ITALIC, model));

        model.set_sort_column_id(COL_PRIORITY, Gtk.SortType.ASCENDING);
        scroller.add(treeview);
        parentContainer.add(scroller);

        let toolbar = new Gtk.Toolbar();
        toolbar.get_style_context().add_class(Gtk.STYLE_CLASS_INLINE_TOOLBAR);

        let addButton = new Gtk.ToolButton({
            stock_id: Gtk.STOCK_ADD,
            label: _("Add style"),
            is_important: true
        });
        toolbar.add(addButton);
        addButton.connect("clicked", Lang.bind(this, function() {
            let dialog = new Gtk.MessageDialog({
                buttons: Gtk.ButtonsType.OK_CANCEL,
                text: _("Please enter the priority"),
                message_type: Gtk.MessageType.QUESTION,
                title: _("New priority style"),
            });
            let dialogbox = dialog.get_content_area();
            let userentry = new Gtk.Entry();
            dialogbox.pack_end(userentry, false, false, 0);
            dialog.show_all();
            let response = dialog.run();
            let priority = userentry.get_text();
            if (response && (priority !== '')) {
                let newRow = model.insert(10);
                model.set(newRow, [COL_PRIORITY, COL_CHANGE_COLOR, COL_COLOR, COL_BOLD, COL_ITALIC], [priority, false, 'rgb(255,255,255)', false, false]);
                if (!this.validateModel(model)) {
                    model.remove(newRow);
                }
            }
            dialog.destroy();
        }));
        let deleteButton = new Gtk.ToolButton({
            stock_id: Gtk.STOCK_DELETE,
            label: _("Delete")
        });
        toolbar.add(deleteButton);
        deleteButton.connect("clicked", Lang.bind(this, function() {
            let[success, model, iter] = treeview.get_selection().get_selected();
            this.removePriorityStyle(model.get_value(iter, COL_PRIORITY));
            if (success) {
                model.remove(iter);
            }
        }));
        parentContainer.add(toolbar);
    },

    buildPrioritiesTab: function(notebook) {
        let page = new Gtk.Box({
            orientation: Gtk.Orientation.VERTICAL,
            border_width: 10,
            vexpand: true
        });
        let title = new Gtk.Label({
            label: _("Priorities")
        });
        this.buildPrioritiesSettings(page);
        this.buildPrioritiesStyleScroller(page);
        notebook.append_page(page, title);
    },

    buildPrefsWidget: function() {
        let notebook = new Gtk.Notebook();
        this.buildGeneralTab(notebook);
        this.buildDisplayTab(notebook);
        this.buildPrioritiesTab(notebook);
        let frame = new Gtk.Box({
            orientation: Gtk.Orientation.VERTICAL,
            border_width: 10
        });

        frame.add(notebook);

        frame.show_all();

        return frame;
    }
};

/* vi: set expandtab tabstop=4 shiftwidth=4: */

