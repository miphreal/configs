from pathlib import Path


def rofi(ctl):
    if not ctl.is_linux:
        return

    ctl.conf(
        python_version="3.8.13",
        venv_name="rofi",
        i3_lock_background_image="{{ dep('//tools/i3').bg_image }}",
        rofi_venv_python_bin="{{ user.home }}/.pyenv/versions/rofi/bin/python",
        rofi_font="Roboto Mono for Powerline 11",
        rofi_modes="window,drun,run,ssh,menu:{{ rofi_custom_menu_bin }}",
        rofi_config_dir="{{ user.config }}/rofi",
        rofi_config="{{ rofi_config_dir }}/config.rasi",
        rofi_custom_menu_bin="{{ user.bin }}/rofi-custom-menu",
        # Rofi theme
        themes_repo="https://github.com/lr-tech/rofi-themes-collection",
        themes_repo_dir="{{ rofi_config_dir }}/themes-repo",
        themes_dir="{{ rofi_config_dir }}/themes",
        rofi_theme=["squared-everforest", "gruvbox-light-soft"][0],
        projects=[
            ("prj/imagen", "code-insiders ~/Develop/imagen/imagen.code-workspace"),
            ("lib/rofi-menu", "code-insiders ~/Develop/rofi-menu/"),
            ("my/configs", "code-insiders ~/Develop/configs/"),
            ("lib/qcheck", "code-insiders ~/Develop/qcheck/"),
            ("lib/gqltype", "code-insiders ~/Develop/gqltype/"),
            (
                "prj/openvpn-lightui",
                "code-insiders ~/Develop/experiments/openvpn-lightui/",
            ),
        ],
    )

    if not ctl.sh("which rofi"):
        ctl.sudo("apt-get install -y rofi")

    ctl.ensure_dirs(ctl.rofi_config_dir)

    if ctl.venv_name not in ctl.sh("pyenv virtualenvs --bare"):
        ctl.sh("pyenv virtualenv {{ python_version }} {{ venv_name }}")
        # ctl.sh(f"{ctl.ROFI_VENV_PYTHON_BIN} -m pip install rofi-menu")
        ctl.sh(
            "ln -s ~/Develop/rofi-menu/rofi_menu ~/.pyenv/versions/rofi/lib/python3.8/site-packages/rofi_menu"
        )

    if not Path(ctl.themes_repo_dir).exists():
        ctl.sh("git clone {{ themes_repo }} {{ themes_repo_dir }}")
        ctl.sh("cp -R {{ themes_repo_dir }}/themes {{ themes_dir }}")

    ctl.render("./rofi.conf.rasi.j2", ctl.rofi_config)
    ctl.render("./rofi_custom_menu.py.j2", "{{ rofi_custom_menu_bin }}")
    ctl.sh("chmod +x {{ rofi_custom_menu_bin }}")
