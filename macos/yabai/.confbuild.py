def yabai(conf):
    conf['brew::koekeishiya/formulae/yabai']
    conf(
        config=conf["path::~/.yabairc"]
    )
    conf.render('.yabairc', conf.config)
    conf.sh('launchctl kickstart -k "gui/${UID}/homebrew.mxcl.yabai"')