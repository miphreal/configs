HOMEBREW_ZSH_RC = """
# Homebrew
export HOMEBREW_AUTO_UPDATE_SECS="86400"
eval "$(/opt/homebrew/bin/brew shellenv)"
"""

def main(conf):
    conf(
        zsh_profile=HOMEBREW_ZSH_RC,
        homepage="https://brew.sh/",
    )

