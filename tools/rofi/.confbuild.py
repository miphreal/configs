def rofi(ctl):
    ctl.conf(
        ROFI_FONT="Roboto Mono for Powerline 11",
        ROFI_MODES="window,drun,run,ssh,menu:~/.local/bin/rofi-custom-menu",
        ROFI_OPACITY=100,
        ROFI_WIDTH=30,
        ROFI_COLUMNS=1,
        ROFI_VENV_PYTHON_BIN="~/.pyenv/versions/rofi/bin/python",
        rofi_config="~/.config/rofi/config.rasi",
        rofi_custom_menu_bin="~/.local/bin/rofi-custom-menu",
    )

    ctl.sh("sudo apt-get install -y rofi > /dev/null")

    ctl.ensure_dirs("~/.config/rofi")
    # Create venv
    venvs = ctl.sh("pyenv virtualenvs --bare")[0]
    if not b"rofi" in venvs:
        ctl.sh("pyenv virtualenv 3.8.12 rofi")
        # ctl.sh(f"{ctl.ROFI_VENV_PYTHON_BIN} -m pip install rofi-menu")
        ctl.sh(
            "ln -s ~/Develop/rofi-menu/rofi_menu ~/.pyenv/versions/rofi/lib/python3.8/site-packages/rofi_menu"
        )

    ctl.render("./rofi.conf.rasi.j2", ctl.rofi_config)
    ctl.render("./rofi_custom_menu.py.j2", ctl.rofi_custom_menu_bin)
    ctl.sh("chmod +x {{ rofi_custom_menu_bin }}")
