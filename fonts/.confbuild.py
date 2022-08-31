def fonts(ctl):
    ctl.conf(
        fonts_cache_dir="{{ user.cache }}/fonts",
        fonts_repo="https://github.com/ryanoasis/nerd-fonts",
    )

    ctl.sh("git clone --depth 1 {{ fonts_repo }} {{ fonts_cache_dir }}")
    ctl.sh("bash {{ fonts_cache_dir }}/install.sh")

    ctl.conf(
        FiraCode="Fira Code",
    )
