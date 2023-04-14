def macos(conf):
    conf[
        'macos:common',
        './commands',
        './brew',
        './git',
        './yabai',
        './karabiner',
        './kitty',
        './nvm',
        './pyenv',
        './zsh',
    ]


def common(conf):
    conf[
        "brew::exa",
        "brew::fzf",
        "brew::jq",
        "brew::yq",
        "brew::pipx",
        "brew::awscli",
        "pipx::pgcli",
        "pipx::poetry",
        "pipx::litecli",

        "brew::youtube-dl",
        "pipx::yt-dlp",
    ]


"""
TODO:
- vscode
- fuzzy search command history
- raycast scripts?
    is there a way to make them more interactive?
- nvim
- hammerspoon?
- shortcuts/keybindings help depending on the active window?

- replace fig's completion with something more terminal native?
- manage my scripts?

- transition/hydra-like mode for os (like modes in i3 wm) with decent hint/help?

Can manage may ad-hoc scripts/commands:
- any shell scripts (.local/bin)
- fig scripts with autocompletion
- raycast scripts [easy search]

Can triggier from console:
- raycast deeplinks -- https://manual.raycast.com/deeplinks

Can manage hotkeys/keybindings:
- raycast for available commands
- karabiner to redefine keys; trigger any command



"""
