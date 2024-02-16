DIRENV_ZSH_RC = """
##
# Direnv shell integration
eval "$(direnv hook zsh)"
"""

ASDF_ZSH_RC = """
##
# `asdf` tool
#
. "$HOME/.asdf/asdf.sh"
# append completions to fpath
fpath=(${ASDF_DIR}/completions $fpath)

# Activate plugins
. ~/.asdf/plugins/golang/set-env.zsh
"""

BW_ZSH_RC = """
##
# `bitwarden` tool
secrets-unlock() {
    security add-generic-password -a "$(whoami)" -s "bw/session" -w "$(bw unlock --raw)" -U
}
get-secret() {
    session=$(security find-generic-password -a "$(whoami)" -s "bw/session" -w)
    bw --session "${session}" get notes $1
}
"""


def macos(conf):
    conf[
        ":common",
        "./commands",
        "./brew",
        "./git",
        "./docs",
        "./yabai",
        "./karabiner",
        "./kitty",
        "./nvm",
        "./pyenv",
        "./zsh",
    ]


def bitwarden(conf):
    conf(zsh_rc=BW_ZSH_RC)
    conf["brew::bitwarden-cli"]


def direnv(conf):
    conf(zsh_rc=DIRENV_ZSH_RC)
    conf["brew::direnv"]


def asdf(conf):
    """
    Installed plugins:
    - awscli
    - golang
    - java
    - python
    - ruby
    - shellcheck
    - terraform
    """
    plugins = [
        "awscli",
        "golang",
        "java",
        "python",
        "ruby",
        "shellcheck",
        "terraform",
    ]
    conf(zsh_rc=ASDF_ZSH_RC)
    for plugin in plugins:
        conf.sh(f"asdf plugin add {plugin}")


def common(conf):
    conf[
        "brew::coreutils",
        "brew::moreutils",
        "brew::exa",
        "brew::fzf",
        "brew::jq",
        "brew::yq",
        "brew::pipx",  # todo: install pipx directly to not depend on homebrew python
        "brew::stats",
        "brew::trash",  # cli tool to move files to MacOS trash
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
    - lazygit
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
