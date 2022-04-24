from confctl import Base, Param


class Configuration(Base):
    HOME = Param.PATH("~")
    TARGET = Param()
    flags = Param()
    i3_config = Param.PATH("~/.config/i3/config")
    bg_image = Param.PATH("~/.config/i3/bg.png")
    statusbar_config = Param.PATH("~/.config/i3/statusbar.py")
    I3_STATUS_VENV_PYTHON_BIN = Param.PATH("~/.pyenv/versions/i3status/bin/python")
    ROFI_BIN = Param("rofi")

    def configure(self):
        self.ensure_folders(self.i3_config.parent)

        if "full" in self.flags:
            self.run_sh(
                # i3 deps
                "sudo apt-get install -y i3 compton fonts-font-awesome xbacklight > /dev/null",
            )

        venvs = self.run_sh("pyenv virtualenvs --bare")[0]
        if not b"i3status" in venvs:
            self.run_sh("pyenv virtualenv 3.8.12 i3status")
            self.run_sh(
                # i3pystatus deps
                f"{self.I3_STATUS_VENV_PYTHON_BIN} -m pip install --quiet git+https://github.com/enkore/i3pystatus.git",
                f"{self.I3_STATUS_VENV_PYTHON_BIN} -m pip install --quiet xkbgroup netifaces colour psutil",
            )

        self.copy_file("bg.png", symlink=self.bg_image)
        self.template("config.j2", "config", self.i3_config)
        self.template("i3pystatusbar.py.j2", "statusbar.py", self.statusbar_config)

        self._restart_i3()

    def _restart_i3(self):
        import i3ipc

        i3 = i3ipc.Connection()
        try:
            i3.command("restart")
        except Exception as e:
            self.error("[restart rofi error] %s", e)
        self.debug("[ -> i3] Reload i3")
