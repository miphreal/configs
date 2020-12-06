from confctl import Base, Param


class Configuration(Base):
    ROFI_FONT = Param("Roboto Mono for Powerline 11")
    ROFI_MODES = Param("window,drun,run,ssh,menu:~/.local/bin/rofi-custom-menu")
    ROFI_OPACITY = Param(100)
    ROFI_WIDTH = Param(30)
    ROFI_COLUMNS = Param(1)
    ROFI_VENV_PYTHON_BIN = Param.PATH("~/.pyenv/versions/rofi/bin/python")
    rofi_config = Param.PATH("~/.config/rofi/config")
    rofi_custom_menu_bin = Param.PATH("~/.local/bin/rofi-custom-menu")

    def configure(self):
        self.ensure_folders(self.rofi_config.parent)
        # Create venv
        venvs = self.run_sh("pyenv virtualenvs --bare")[0]
        if not b"rofi" in venvs:
            self.run_sh("pyenv virtualenv 3.8.2 rofi")
            self.run_sh(f"{self.ROFI_VENV_PYTHON_BIN} -m pip install rofi_menu")

        self.template("rofi.conf.j2", "config", self.rofi_config)
        self.template("rofi.conf.rasi.j2", "config.rasi", self.rofi_config)  # newer config format
        self.template(
            "rofi_custom_menu.py.j2", "rofi-custom-menu", self.rofi_custom_menu_bin
        )
        self.run_sh(f"chmod +x {self.rofi_custom_menu_bin}")
