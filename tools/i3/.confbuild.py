def i3(ctl):
    if not ctl.is_linux:
        return

    ctl.conf(
        python_version="3.8.13",
        i3_config_dir="{{ user.config }}/i3",
        bg_image="{{ i3_config_dir }}/bg.png",
        i3_status_venv_python_bin="~/.pyenv/versions/i3status/bin/python",
        ROFI_BIN="rofi",
        statusbar_config="{{ i3_config_dir }}/statusbar.py",
    )

    ctl.ensure_dirs(ctl.i3_config_dir)

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
