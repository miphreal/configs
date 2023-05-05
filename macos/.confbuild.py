def macos(conf):
    conf[
        ':common',
        './commands',
        './brew',
        './git',
        './yabai',
        './karabiner',
        './kitty',
        './nvm',
        './pyenv',
        './zsh',
        ':direnv',
    ]

DIRENV_ZSH_RC = """
# Direnv shell integration
eval "$(direnv hook zsh)"
"""

def direnv(conf):
    conf(zsh_rc=DIRENV_ZSH_RC)
    # conf['./zsh'] <<= conf(zsh_rc=DIRENV_ZSH_RC)
    conf["brew::direnv"]

ASDF_ZSH_RC = """
. "$HOME/.asdf/asdf.sh"
# append completions to fpath
fpath=(${ASDF_DIR}/completions $fpath)
"""

def asdf(conf):
    conf(zsh_rc=ASDF_ZSH_RC)


def common(conf):
    conf[
        "brew::coreutils",
        "brew::exa",
        "brew::fzf",
        "brew::jq",
        "brew::yq",
        "brew::pipx",  # todo: install pipx directly to not depend on homebrew python
        
        "brew::awscli",

        "brew::circleci",

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
    - tree view
    - lazygit or neogit?
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
