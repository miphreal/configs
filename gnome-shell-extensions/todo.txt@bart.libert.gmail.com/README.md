# todo.txt gnome-shell extension

This extension enables you to manage your [todo.txt](http://todotxt.com/ "Todo.txt homepage") file from gnome-shell.

##Supported features
* Adding new tasks
* Marking tasks as completed
* Deleting tasks
* Show tasks grouped by projects or contexts
* Auto-achive of done tasks to done.txt
* Tasks are sorted by priority
* Done but not archived tasks are shown in italic text and include "archive" button
* Editing tasks
* Changes in todo.txt file via other ways are reflected in the extension
* Tasks can be shown in a specific style, based on the priority

##Known issues/missing features
* Task priority is not shown (but is considered for sorting)
* No confirmation is asked before deleting a task
* There is no possibility to show archived tasks
* ...

##Screenshots
Ungrouped mode, some tasks with projects and/or contexts, one task with high priority:

![Ungrouped todo.txt screenshot](http://lapino.be/media/todotxt.png "Todo.txt in ungrouped mode")

Grouped by projects, ungrouped tasks not in a seperate group:

![Grouped todo.txt screenshot](http://lapino.be/media/todotxt_groups.png "Todo.txt in grouped mode")

Preferences:

![Preferences screenshot](http://lapino.be/media/todotxt_prefs.png "Todo.txt preferences")

##Installation
You can either use [the Gnome extensions webpage](http://extensions.gnome.org) or do it yourself:

* Put the code in ~/.local/share/gnome-shell/extensions/todo.txt@bart.libert.gmail.com
* Execute glib-compile-schemas ~/.local/share/gnome-shell/extensions/todo.txt@bart.libert.gmail.com/schemas
* Enable the extension with gnome-tweak-tool
* Configure the extension with gnome-shell-extension-preferences

##Credits
This extension uses [jsTodoTxt](https://github.com/jmhobbs/jsTodoTxt "jsTodoTxt homepage") by John Hobbs

Parts of this extension are based on:

* [Todo list](https://extensions.gnome.org/extension/162/todo-list/) by bsaleil
* [SettingsCenter](https://extensions.gnome.org/extension/341/settingscenter/) by Xes

Thank you!

##Licence
This code is released under GPLv2+

