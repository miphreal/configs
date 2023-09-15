# TODO: install nerd fonts

def main(conf):
    # conf(
    #     fonts_cache_dir=conf["dir::{{ user.cache }}/fonts"],
    #     fonts_repo="https://github.com/ryanoasis/nerd-fonts",
    # )

    # if not any(conf.fonts_cache_dir.iterdir()):
    #     conf.sh("git clone --depth 1 {{ fonts_repo }} {{ fonts_cache_dir }}")
    #     conf.sh("bash {{ fonts_cache_dir }}/install.sh")

    # brew tap homebrew/cask-fonts
    # brew install font-hack-nerd-font

    conf.conf(
        FiraCode="Fira Code",
        FiraCodeRetina="FiraCode-Retina",
    )
