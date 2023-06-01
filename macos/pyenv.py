ZSH_RC = """
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
"""


def main(conf):
    conf(
        zsh_rc=ZSH_RC,
    )
    conf[
        'brew::pyenv',
        'brew::pyenv-virtualenv',
    ]
