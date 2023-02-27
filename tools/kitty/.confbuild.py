def kitty(conf):
    # conf.dep(
    #     "platform::linux || platform::macos",
    #     "apt::htop || brew::htop",
    #     "pipx::confctl@1.0.0",
    #     "pyenv::python@3.10.4",
    #     "asdf::python@3.10.4",
    #     "conf::tools/i3:i3?no-restart",
    # )
    conf(
        kitty_font=conf["fonts"].FiraCode,
        kitty_bin=conf["path::{{ user.bin }}/kitty"],
        kitty_dist_dir=conf["dir::{{ user.opt }}/kitty.app-fake"],
        kitty_conf=conf["path::{{ user.config }}/kitty.conf-fake"],
    )

    if "full" in conf.ctx:
        conf.sh(
            """
            curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin \\
                launch=n dest={{ kitty_dist_dir }}
            #ln -s {{ kitty_dist_dir }}/bin/kitty {{ kitty_bin }}
            """
        )

    conf.render("./kitty.conf.j2", conf.kitty_conf)
