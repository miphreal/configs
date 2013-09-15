const Gio = imports.gi.Gio;
const Convenience = imports.misc.extensionUtils.getCurrentExtension().imports.convenience;

const prefs = Convenience.getSettings('org.gnome.shell.extensions.per-window-keyboard-layout');
const tracker = imports.gi.Shell.WindowTracker.get_default();

let defaultSource = 0;

let display, focus_connection, source_connection, settings;

//bool - remember even if app closed and opened again
let permanently = prefs.get_boolean('rememberpermanently');

//bool - remember even if Gnome-shell ends and starts again
let forever = prefs.get_boolean('rememberforever');

//an array for remembering {application name:layout} associations
let remembered = { };

function restoreWindowInputSource() {

    let window = display.focus_window;

    if (window) {

        let source = window._inputSource;

        if (source === undefined) {
	    if (permanently) {
		//try to find layout for the app in the remembered layouts
		
		//apps are remembered by app name or wm_class name 
		//(because some windows don't have apps associated, e.g. Guake)
		let index = "";
		
		let app = tracker.get_window_app(window);
		
		if (app)
		    index = app.get_id();
		else
		    index = window.get_wm_class();
		
		if (index in remembered)
		    source = remembered[index];
		else
		    source = defaultSource;
	    }
	    
	    else
	        source = defaultSource;

	}

        settings.set_uint('current', source);
    }

}

function saveWindowInputSource() {

    let current = settings.get_uint('current'),
        window = display.focus_window;

    if (window) {
        window._inputSource = current;
	
	if (permanently) {
	    //remember association
	
	    let index = "";
	    
	    let app = tracker.get_window_app(window);
	    
	    if (app)
		index = app.get_id();
	    else
		index = window.get_wm_class();
	    
	    remembered[index] = current;
	    
	}
	
    }
    
    //settings are written here each time because I don't know how to make
    //a destructor which would be much nicer: 
    //http://stackoverflow.com/questions/15614120/gnome-shell-extension-destructor-run-on-gnome-shell-exit
    if (forever)
	writePrefs();

}

function readPrefs() {
    
    //no better way than two arrays of strings possible in GS extension
    let apps = prefs.get_strv('app-list');
    let layouts = prefs.get_strv('keyboard-layout-list');
    
    let i = 0;
    for (app in apps) {
	remembered[apps[app]] = parseInt(layouts[i++]);    
    }
    
}

function writePrefs() {
    
    let apps = [];
    let layouts = [];
    
    let i = 0;
    for (app in remembered) {
	apps[i] = app;
	layouts[i++] = remembered[app].toString();
    }

    prefs.set_strv('app-list', apps);
    prefs.set_strv('keyboard-layout-list', layouts);
}

function init() {

    display = global.display;
    settings = new Gio.Settings({ schema: 'org.gnome.desktop.input-sources' });
    
    //read previously saved associations
    if (forever)
	readPrefs();

}

function enable() {

    focus_connection = display.connect('notify::focus-window', restoreWindowInputSource);
    source_connection = settings.connect('changed::current', saveWindowInputSource);

    restoreWindowInputSource();

}

function disable() {

    display.disconnect(focus_connection);
    settings.disconnect(source_connection);

    saveWindowInputSource();

    settings.set_uint('current', defaultSource);
    
    if (forever)
	writePrefs();

}
