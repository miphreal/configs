const Clutter = imports.gi.Clutter;
const Lang = imports.lang;
const St = imports.gi.St;
const Signals = imports.signals;

const ModalDialog = imports.ui.modalDialog;
const ShellEntry = imports.ui.shellEntry;

const Gettext = imports.gettext;
const _ = Gettext.domain('todotxt').gettext;

const EditDialog = new Lang.Class({
    Name: 'EditDialog',
    Extends: ModalDialog.ModalDialog,

    _init: function(callback) {
        this.callback = callback;
        this.parent({
            styleClass: 'prompt-dialog'
        });

        let label = new St.Label({
            style_class: 'edit-dialog-label',
            text: _("Edit task:")
        });

        this.contentLayout.add(label, {
            y_align: St.Align.START
        });

        let entry = new St.Entry({
            style_class: 'edit-dialog-entry'
        });
        entry.label_actor = label;

        this._entryText = entry.clutter_text;
        this.contentLayout.add(entry, {
            y_align: St.Align.START
        });
        this.setInitialKeyFocus(this._entryText);

        let buttons = [{
            label: _('Cancel'),
            action: Lang.bind(this, this._onCancelButton),
            key: Clutter.Escape
        },
        {
            label: _('Ok'),
            action: Lang.bind(this, this._onOkButton),
        }];

        this.setButtons(buttons);

        this._entryText.connect('key-press-event', Lang.bind(this, function(o, e) {
            let symbol = e.get_key_symbol();
            if (symbol == Clutter.Return || symbol == Clutter.KP_Enter) {
                this._onOkButton();
            }
        }));
    },

    close: function() {
        this.parent();
    },

    _onCancelButton: function() {
        this.close();
    },

    _onOkButton: function() {
        this.callback(this._entryText.get_text());
        this.close();
    },

    open: function(initialText) {
        if (initialText === null) {
            this._entryText.set_text('');
        }
        else {
            this._entryText.set_text(initialText);
        }

        this.parent();
    },
});
Signals.addSignalMethods(EditDialog.prototype);

/* vi: set expandtab tabstop=4 shiftwidth=4: */

