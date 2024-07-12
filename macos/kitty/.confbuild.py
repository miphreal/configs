ZSH_RC = """
##
# Kitty integration
if test -n "$KITTY_INSTALLATION_DIR"; then
    export KITTY_SHELL_INTEGRATION="enabled"
    autoload -Uz -- "$KITTY_INSTALLATION_DIR"/shell-integration/zsh/kitty-integration
    kitty-integration
    unfunction kitty-integration
fi
"""

def kitty(conf):
    conf(
        kitty_font="FiraCode Nerd Font Mono",
        kitty_font_size="11.0",
        kitty_font_italic="Hack Nerd Font Mono",
        kitty_conf=conf["path::{{ user.config }}/kitty/kitty.conf"],
        themes_dir=conf["dir::{{ user.config }}/kitty/kitty-themes"],
        theme="SpaceGray",
        zsh_rc=ZSH_RC,
    )

    conf.render("./kitty.conf.j2", conf.kitty_conf)

    if not conf.themes_dir.exists():
        conf.sh(
            "git clone --depth 1 https://github.com/dexpota/kitty-themes.git {{ themes_dir }}"
        )

    conf.sh("cp -r {{ current_config_dir }}/icons/* {{ kitty_conf.parent }}")
    conf.sh("cp {{ current_config_dir }}/current-theme.conf {{ kitty_conf.parent }}")

    # reload kitty
    conf.sh("kill -USR1 $(pgrep -a kitty) | true")
