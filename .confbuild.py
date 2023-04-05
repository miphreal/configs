import os
import platform

CONFCTL_RESOLVERS = [
    "confctl.contrib.pyenv.setup",
    "confctl.contrib.pipx.setup",
    "confctl.contrib.homebrew.setup",
]

system_name = platform.system()

# Root context
is_linux = system_name == "Linux"
is_macos = system_name == "Darwin"
user = dict(
    bin="{{ env.HOME }}/.local/bin",
    opt="{{ env.HOME }}/.local/opt",
    config="{{ env.HOME }}/.config",
    cache="{{ env.HOME }}/.cache",
)
env = os.environ
terminal = dict(
    font_family="{{ dep('//fonts').FiraCode }}",
    font_size=12,
)

def main(conf):
    if is_macos:
        conf.dep('macos')
    elif is_linux:
        conf.dep('linux')

