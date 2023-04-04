ZSH_RC = """
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
"""


def main(conf):
    conf['brew::nvm']
    conf(
        zsh_rc=ZSH_RC,
    )
