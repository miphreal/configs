ZSH_RC = """
##
# Rust / Cargo
#
. "$HOME/.cargo/env"
"""


def main(conf):
    conf(zsh_rc=ZSH_RC)
    conf.sh("command -v rustup >/dev/null || curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path")
