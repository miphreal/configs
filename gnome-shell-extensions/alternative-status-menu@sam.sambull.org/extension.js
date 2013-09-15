/* -*- mode: js2 - indent-tabs-mode: nil - js2-basic-offset: 4 -*- */
const Lang = imports.lang;
const St = imports.gi.St;
const Main = imports.ui.main;
const PopupMenu = imports.ui.popupMenu;

const Gettext = imports.gettext.domain('gnome-shell-extensions');
const _ = Gettext.gettext;

const ExtensionUtils = imports.misc.extensionUtils;
const Me = ExtensionUtils.getCurrentExtension();
const Convenience = Me.imports.convenience;

const SUSPEND_LOCK_ENABLED_KEY = imports.ui.userMenu.SUSPEND_LOCK_ENABLED_KEY;
const LOCK_ENABLED_KEY = imports.ui.userMenu.LOCK_ENABLED_KEY;

let settings = null;

let statusMenu = Main.panel.statusArea.userMenu;

function onSuspendActivate(item) {
    Main.overview.hide();

    if (this._screenSaverSettings.get_boolean(LOCK_ENABLED_KEY)) {
        let tmpId = Main.screenShield.connect('lock-screen-shown', Lang.bind(this, function() {
            Main.screenShield.disconnect(tmpId);

            this._upClient.suspend_sync(null);
        }));

        Main.screenShield.lock(true);
    } else {
        this._upClient.suspend_sync(null);
    }
}

function onHibernateActivate(item) {
    Main.overview.hide();

    if (this._screenSaverSettings.get_boolean(LOCK_ENABLED_KEY)) {
        let tmpId = Main.screenShield.connect('lock-screen-shown', Lang.bind(this, function() {
            Main.screenShield.disconnect(tmpId);

            this._upClient.hibernate_sync(null);
        }));

        Main.screenShield.lock(true);
    } else {
        this._upClient.hibernate_sync(null);
    }
}

// Put your extension initialization code here
function init(metadata) {
    Convenience.initTranslations();
}

function updateSuspendOrHibernate(object, pspec, item) {
    this._haveSuspend = object.get_can_suspend() && settings.get_boolean('allow-suspend');
    this._haveHibernate = object.get_can_hibernate() && settings.get_boolean('allow-hibernate');

    if (!this._suspendOrHibernateItem)
        return;

    this._suspendOrHibernateItem.actor.visible = this._haveSuspend || this._haveHibernate;

    // If we can't hibernate show Suspend instead
    // and disable the alt key
    if (!statusMenu._haveSuspend) {
        this._suspendOrHibernateItem.updateText(_("Hibernate"), null);
    } else if (!this._haveHibernate) {
        this._suspendOrHibernateItem.updateText(_("Suspend"), null);
    } else {
        this._suspendOrHibernateItem.updateText(_("Suspend"), _("Hibernate"));
    }
}

function updateRebootOrPowerOff(object, pspec, item) {
    if (!this._rebootOrPowerOffItem)
        return;

    this._rebootOrPowerOffItem.actor.visible = statusMenu._haveShutdown;

    this._rebootOrPowerOffItem.updateText(_("Power Off"), _("Restart"));
}

function _onSuspendOrHibernateActivate() {
    Main.overview.hide();

    if (this._haveSuspend &&
        this._suspendOrHibernateItem.state == PopupMenu.PopupAlternatingMenuItemState.DEFAULT) {
        if (statusMenu._screenSaverSettings.get_boolean(SUSPEND_LOCK_ENABLED_KEY)) {
            let tmpId = Main.screenShield.connect('lock-screen-shown', Lang.bind(this, function() {
                Main.screenShield.disconnect(tmpId);

                statusMenu._upClient.suspend_sync(null);
            }));

            Main.screenShield.lock(true);
        } else {
            statusMenu._upClient.suspend_sync(null);
        }
    } else {
        if (statusMenu._screenSaverSettings.get_boolean(LOCK_ENABLED_KEY)) {
            let tmpId = Main.screenShield.connect('lock-screen-shown', Lang.bind(this, function() {
                Main.screenShield.disconnect(tmpId);

                statusMenu._upClient.hibernate_sync(null);
            }));

            Main.screenShield.lock(true);
        } else {
            statusMenu._upClient.hibernate_sync(null);
        }
    }
}

function _onRebootOrPowerOffActivate() {
    Main.overview.hide();

    if (statusMenu._haveShutdown &&
        this._rebootOrPowerOffItem.state == PopupMenu.PopupAlternatingMenuItemState.DEFAULT) {
        statusMenu._session.ShutdownRemote();
    } else {
        statusMenu._session.RebootRemote();
    }
}

function enable() {
    settings = Convenience.getSettings();

    let children = statusMenu.menu._getMenuItems();
    let index = children.length;

    /* find and destroy the old entry */
    for (let i = children.length - 1; i >= 0; i--) {
        if (children[i] == statusMenu._suspendOrPowerOffItem) {
            children[i].destroy();
            index = i;
            break;
        }
    }

    item = new PopupMenu.PopupAlternatingMenuItem(_("Suspend"),
                                                  _("Hibernate"));
    statusMenu.menu.addMenuItem(item, index);
    item.connect('activate', Lang.bind(this, this._onSuspendOrHibernateActivate));
    this._suspendOrHibernateItem = item;
    this.suspend_signal_id = statusMenu._upClient.connect('notify::can-suspend', Lang.bind(statusMenu, updateSuspendOrHibernate, this._suspendOrHibernateItem));
    this.hibernate_signal_id = statusMenu._upClient.connect('notify::can-hibernate', Lang.bind(statusMenu, updateSuspendOrHibernate, this._suspendOrHibernateItem));
    updateSuspendOrHibernate(statusMenu._upClient, null, this._suspendOrHibernateItem);

    item = new PopupMenu.PopupAlternatingMenuItem(_("Power Off"),
                                                  _("Restart"));
    statusMenu.menu.addMenuItem(item, index + 1);
    item.connect('activate', Lang.bind(this, this._onRebootOrPowerOffActivate));
    this._rebootOrPowerOffItem = item;
    updateRebootOrPowerOff(statusMenu._upClient, null, this._rebootOrPowerOffItem);

    // clear out this to avoid criticals (we don't mess with
    // updateSuspendOrPowerOff)
    statusMenu._suspendOrPowerOffItem = null;

    this.setting_changed_id = settings.connect('changed', function() {
        updateSuspendOrHibernate(statusMenu._upClient, null, this._suspendOrHibernateItem);
        updateRebootOrPowerOff(statusMenu._upClient, null, this._rebootOrPowerOffItem);
    });
}

function disable() {
    let children = statusMenu.menu._getMenuItems();
    let index = children.length;

    /* find the index for the previously created items */
    for (let i = children.length - 1; i >= 0; i--) {
        if (children[i] == this._suspendOrHibernateItem) {
            index = i;
        }
    }

    /* disconnect signals */
    statusMenu._upClient.disconnect(suspend_signal_id);
    statusMenu._upClient.disconnect(hibernate_signal_id);
    this.suspend_signal_id = this.hibernate_signal_id = 0;

    settings.disconnect(this.setting_changed_id);
    this.setting_changed_id = 0;
    settings = null;

    /* destroy the entries we had created */
    this._rebootOrPowerOffItem.destroy();
    this._suspendOrHibernateItem.destroy();

    /* create a new suspend/poweroff entry */
    /* empty strings are fine for the labels, since we immediately call updateSuspendOrPowerOff */
    let item = new PopupMenu.PopupAlternatingMenuItem("", "");
    /* restore the userMenu field */
    statusMenu._suspendOrPowerOffItem = item;
    statusMenu.menu.addMenuItem(item, index);
    item.connect('activate', Lang.bind(statusMenu, statusMenu._onSuspendOrPowerOffActivate));
    statusMenu._updateSuspendOrPowerOff();
}
