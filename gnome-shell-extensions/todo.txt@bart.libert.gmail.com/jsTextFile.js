const GLib = imports.gi.GLib;
const Shell = imports.gi.Shell;
const Gio = imports.gi.Gio;

function JsTextFile(path) {
	if (path === null) {
		global.logError("JsTextFile: no path specified");
		return false;
	}
	this.path = path;
	this._loadLines();
	return true;
}

JsTextFile.prototype = {
	path: null,
	lines: null,

	// Returns true if file exists, false if not
	exists: function() {
		if (GLib.file_test(this.path, GLib.FileTest.EXISTS)) {
			return true;
		}
		global.logError("JsTextFile: File does not exist : " + this.path);
		return false;
	},

	// Loads all lines from the text file
	_loadLines: function() {
		if (!this.exists()) {
			global.logError("JsTextFile: trying to load non-existing file");
			return false;
		}
		let content = Shell.get_file_contents_utf8_sync(this.path);
		this.lines = content.toString().split('\n');
		return true;
	},

	// Returns the number in the lines-array that contains the matching string
	// Returns -1 if text is not found
	_getLineNum: function(text) {
		if (!this.exists()) {
			return - 1;
		}
		return this.lines.indexOf(text);
	},

	// Saves the lines to a file
	saveFile: function(removeEmptyLines) {
		if (!this.exists()) {
			return false;
		}
		if (removeEmptyLines === true) {
			this._removeEmptyLines();
		}
		let file = Gio.file_new_for_path(this.path);
		let out = file.replace(null, false, Gio.FileCreateFlags.NONE, null);
		Shell.write_string_to_stream(out, this.lines.join('\n') + '\n');
		out.close(null);
		return true;
	},

	_removeEmptyLines: function() {
		this.lines = this.lines.filter(function(value) {
			return (value !== "");
		});
	},

	getLines: function() {
		if (!this.exists()) {
			global.logError("JsTextFile: no path specified");
		}
		return this.lines;
	},

	removeLine: function(text) {
		let lineNum = this._getLineNum(text);
		if (lineNum == - 1) {
			return false;
		}
		this.lines.splice(lineNum, 1);
		return true;
	},

	addLine: function(text) {
		if (!this.exists()) {
			return false;
		}
		this.lines.push(text);
		return true;
	},

	modifyLine: function(oldtext, newtext) {
		if (this.removeLine(oldtext)) {
			return this.addLine(newtext);
		}
		return false;
	},

	setLines: function(newlines) {
		this.lines = newlines;
	}
};

/* vi: set expandtab tabstop=4 shiftwidth=4: */

