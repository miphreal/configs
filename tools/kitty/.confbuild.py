def kitty(ctl):
    ctl.conf(
        kitty_font=ctl.dep("//fonts:fira_code").font_name,
        kitty_bin="{{ user.bin }}/kitty",
        kitty_conf_dir="{{ user.config }}/kitty",
        kitty_conf="{{ kitty_conf_dir }}/kitty.conf-fake",
        kitty_dist_dir="{{ user.opt }}/kitty.app-fake",
    )
    ctl.ensure_dirs(ctl.kitty_conf_dir, ctl.kitty_dist_dir)

    if "full" in ctl.ctx:
        ctl.sh(
            """
            curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin \\
                launch=n dest={{ kitty_dist_dir }}
            #ln -s {{ kitty_dist_dir }}/bin/kitty {{ kitty_bin }}
            """
        )

    ctl.render("./kitty.conf.j2", ctl.kitty_conf)
