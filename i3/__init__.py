from confctl import Base, Param


class Configuration(Base):
    HOME = Param.PATH("~")
    TARGET = Param()
    flags = Param()
    i3_config = Param.PATH("~/.config/i3/config")
    bg_image = Param.PATH("~/.config/i3/bg.png")
    statusbar_config = Param.PATH("~/.config/i3/statusbar.py")

    def configure(self):
        self.ensure_folders(self.i3_config.parent)

        if "full" in self.flags:
            self.run_sh(
                # i3 deps
                "sudo apt-get install -y i3 rofi compton fonts-font-awesome xbacklight > /dev/null",
                # i3pystatus deps
                "sudo /usr/bin/python3 -m pip install --quiet git+https://github.com/enkore/i3pystatus.git",
                "sudo /usr/bin/python3 -m pip install --quiet xkbgroup netifaces colour psutil",
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
