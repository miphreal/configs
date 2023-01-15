import os
import platform

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


def __resolve_platform__(spec: str):
    spec = spec.lower()
    match (spec, system_name):
        case ("linux", "Linux"):
            return True
        case ("macos", "Darwin"):
            return True
    return False


def linux(conf):
    conf.dep("//tools/i3")
    conf.dep("//tools/rofi")

    conf.dep("//tools/zsh")
    conf.dep("//tools/pyenv")
    conf.dep("//tools/nvm")

    conf.dep("//tools/kitty")
    conf.dep("//tools/nvim")
