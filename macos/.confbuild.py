ASDF_ZSH_RC = """
##
# `asdf` tool
#
. "$HOME/.asdf/asdf.sh"
# append completions to fpath
fpath=(${ASDF_DIR}/completions $fpath)

# Activate plugins
. "$HOME/.asdf/plugins/golang/set-env.zsh"
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

YAZI_ZSH_RC = """
function yy() {
	local tmp="$(mktemp -t "yazi-cwd.XXXXXX")"
	yazi "$@" --cwd-file="$tmp"
	if cwd="$(cat -- "$tmp")" && [ -n "$cwd" ] && [ "$cwd" != "$PWD" ]; then
		cd -- "$cwd"
	fi
	rm -f -- "$tmp"
}
"""


def macos(conf):
    conf[
        ":common",
        "./commands",
        "./brew",
        "./git",
        "./docs",
        "./karabiner",
        "./kitty",
        "./wezterm",
        "./tmux",
        "./nvm",
        "./pyenv",
        "./zsh",
    ]


def bitwarden(conf):
    conf(zsh_rc=BW_ZSH_RC)
    conf["brew::bitwarden-cli"]


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


def yazi(conf):
    conf["brew::yazi"]
    conf(zsh_rc=YAZI_ZSH_RC)


def fd(conf):
    """Fast `find` alternative"""
    conf["brew::fd"]


def fzf(conf):
    """Fuzzy file finder (by file name)"""
    conf[
        "brew::fzf",
        ":fd", # fzf depends on fd
    ]
    conf(
        zsh_rc="""
            # FZF config
            export FZF_DEFAULT_OPTS="--height 40% --layout reverse --inline-info"
            # - setting fd as the default source for fzf
            export FZF_DEFAULT_COMMAND='fd --type f --strip-cwd-prefix --hidden --follow --exclude .git'
            export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
            source <(fzf --zsh)
        """
    )


def common(conf):
    conf[
        "brew::coreutils",
        "brew::moreutils",
        "brew::curl",
        "brew::git",
        "brew::eza",  # ≈ls
        "brew::sd",  # ≈sed
        "brew::jq",
        "brew::yq",
        "brew::pipx",  # todo: install pipx directly to not depend on homebrew python
        "brew::stats",
        "brew::trash",  # cli tool to move files to MacOS trash
        # "brew::awscli",
        # "brew::circleci",
        "pipx::pgcli",
        "pipx::poetry",
        "pipx::litecli",
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
