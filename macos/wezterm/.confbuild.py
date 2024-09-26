ZSH_RC = """
##
# Wezterm Intergration
_wezterm_integration_file="$HOME/.local/share/wezterm.sh"
if [[ ! -f "$_wezterm_integration_file" ]]; then
  curl -o "$_wezterm_integration_file" -L "https://raw.githubusercontent.com/wez/wezterm/master/install.sh"
fi
. "$_wezterm_integration_file"

"""

def wezterm(conf):
    conf(
        zsh_rc=ZSH_RC,
    )
