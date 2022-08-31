def i3(ctl):
    if not ctl.is_linux:
        return

    ctl.conf(
        i3_config_dir="~/.config/i3",
        i3_config="{{ i3_config_dir }}/config",
        bg_image="{{ i3_config_dir }}/bg.png",
        statusbar_config="{{ i3_config_dir }}/statusbar.py",
        I3_STATUS_VENV_PYTHON_BIN="~/.pyenv/versions/i3status/bin/python",
        ROFI_BIN="rofi",
    )

    ctl.ensure_dirs(ctl.i3_config_dir)

    if "full" in ctl.ctx:
        ctl.sh(
            # i3 deps
            "sudo apt-get install -y i3 compton fonts-font-awesome xbacklight > /dev/null",
        )

    venvs = ctl.sh("pyenv virtualenvs --bare")[0]
    if not b"i3status" in venvs:
        ctl.sh("pyenv virtualenv 3.8.12 i3status")
        ctl.sh(
            # i3pystatus deps
            f"{ctl.I3_STATUS_VENV_PYTHON_BIN} -m pip install --quiet git+https://github.com/enkore/i3pystatus.git",
            f"{ctl.I3_STATUS_VENV_PYTHON_BIN} -m pip install --quiet xkbgroup netifaces colour psutil",
        )

    # ctl.copy("./bg.png", ctl.bg_image)
    ctl.render("config.j2", ctl.i3_config)
    ctl.render("i3pystatusbar.py.j2", ctl.statusbar_config)

    ctl.sh("i3-msg restart")
