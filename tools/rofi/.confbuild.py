from pathlib import Path


def rofi(conf):
    if not conf.is_linux:
        return

    conf(
        python_version="3.10.4",
        venv_name="rofi",
        use_rofi_menu_dev=True,
        i3_lock_background_image="{{ dep('../i3').bg_image }}",
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
            ("lib/confctl+configs", "code-insiders ~/Develop/confctl.code-workspace"),
            ("my/configs", "code-insiders ~/Develop/configs/"),
            ("lib/qcheck", "code-insiders ~/Develop/qcheck/"),
            ("lib/gqltype", "code-insiders ~/Develop/gqltype/"),
            (
                "prj/openvpn-lightui",
                "code-insiders ~/Develop/experiments/openvpn-lightui/",
            ),
        ],
    )
    conf[
        "dir::{{ rofi_config_dir }}",
        "dir::{{ themes_dir }}",
    ]

    if not conf.sh("which rofi"):
        conf.sudo("apt-get install -y rofi")

    venv = conf["pyenv::python/{{ python_version }}/{{ venv_name }}"]
    venv.state("pip-installed", "rofi-menu==0.6")

    venv_dir = venv.state("dir")
    conf(rofi_venv_python_bin=f"{venv_dir}/bin/python")

    if conf.use_rofi_menu_dev:
        rofi_menu_dir = Path(f"{venv_dir}/lib/python3.10/site-packages/rofi_menu")
        if rofi_menu_dir.exists():
            conf.sh(f"rm -rf {rofi_menu_dir}")
        conf.sh(f"ln -s ~/Develop/rofi-menu/rofi_menu {rofi_menu_dir}")

    if not Path(conf.themes_repo_dir).exists():
        conf.sh("git clone {{ themes_repo }} {{ themes_repo_dir }}")
        conf.sh("cp -R {{ themes_repo_dir }}/themes {{ themes_dir }}")

    conf.render("./rofi.conf.rasi.j2", conf.rofi_config)
    conf.render("./rofi_custom_menu.py.j2", "{{ rofi_custom_menu_bin }}")
    conf.sh("chmod +x {{ rofi_custom_menu_bin }}")
