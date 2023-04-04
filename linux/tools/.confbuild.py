def tools(conf):
    if conf.is_linux:
        conf.dep("./i3")
        conf.dep("./rofi")
        conf.dep("./nvim")

    elif conf.is_macos:
        conf.dep("//tools/homebrew")

    # conf.dep("//tools/zsh")
    # conf.dep("//tools/pyenv")
    # conf.dep("//tools/nvm")

    # conf.dep("//tools/kitty")
    # conf.dep("//tools/nvim")
