def yabai(conf):
    conf['brew::koekeishiya/formulae/yabai']
    conf.render('.yabairc', '~/.yabairc')
    conf.sh('launchctl kickstart -k "gui/${UID}/homebrew.mxcl.yabai"')
