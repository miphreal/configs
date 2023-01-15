def i3(ctl):
    if not ctl.is_linux:
        return

    ctl.conf(
        python_version="3.10.4",
        i3_config_dir=ctl.dep("dir::{{ user.config }}/i3"),
        bg_image="{{ i3_config_dir }}/bg.png",
        i3_status_venv_python_bin="~/.pyenv/versions/i3status/bin/python",
        rofi_bin="rofi",
        rofi_cmd="{{ rofi_bin }} -show-icons -click-to-exit",
        statusbar_config="{{ i3_config_dir }}/statusbar.py",
        font="FontAwesome",
    )
    ctl.conf(
        autostart=[
            "nm-applet",
            f"/usr/bin/feh --bg-scale {ctl.bg_image}",
            "/usr/bin/compton -f --opengl -b",
            "i3-sensible-terminal",
            "/usr/lib/policykit-1-gnome/polkit-gnome-authentication-agent-1",
            "flameshot",
            "/usr/bin/google-chrome",
            # * messengers
            # "slack",
            # "Telegram",
            # "skypeforlinux",
            # "~/.local/opt/viber.AppImage",
            # "teams",
            # * "syndaemon" monitors keyboard and disables the touchpad when the keyboard is being used #
            # "/usr/bin/syndaemon -i 0.5 -K -R"
        ]
    )

    if "full" in ctl.ctx:
        ctl.sudo("apt-get install -y i3 compton fonts-font-awesome xbacklight")

    if "i3status" not in ctl.sh("pyenv virtualenvs --bare"):
        ctl.sh("pyenv virtualenv {{ python_version }} i3status")
        ctl.sh(
            # i3pystatus deps
            f"{ctl.i3_status_venv_python_bin} -m pip install --quiet git+https://github.com/enkore/i3pystatus.git"
        )
        ctl.sh(
            f"{ctl.i3_status_venv_python_bin} -m pip install --quiet xkbgroup netifaces colour psutil",
        )

    # ctl.copy("./bg.png", ctl.bg_image)
    ctl.render("config.j2", "{{ i3_config_dir }}/config")
    ctl.render("i3pystatusbar.py.j2", "{{ statusbar_config }}")

    if "no-restart" not in ctl.ctx:
        ctl.sh("i3-msg restart")
