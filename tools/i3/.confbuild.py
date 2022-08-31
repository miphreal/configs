def _restart_i3(ctl):
    import i3ipc

    i3 = i3ipc.Connection()
    try:
        i3.command("restart")
    except Exception as e:
        ctl.error("[restart rofi error] %s", e)


def i3(ctl):
    ctl.conf(
        i3_config="~/.config/i3/config",
        bg_image="~/.config/i3/bg.png",
        statusbar_config="~/.config/i3/statusbar.py",
        I3_STATUS_VENV_PYTHON_BIN="~/.pyenv/versions/i3status/bin/python",
        ROFI_BIN="rofi",
    )

    ctl.ensure_dirs(ctl.i3_config)

    if "full" in ctl.params:
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

    ctl.copy("./bg.png", ctl.bg_image)
    ctl.render("config.j2", "config", ctl.i3_config)
    ctl.render("i3pystatusbar.py.j2", "statusbar.py", ctl.statusbar_config)

    ctl.debug("[ -> i3] Reload i3")
    _restart_i3(ctl)
