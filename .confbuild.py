import os
import platform


def main(ctl):
    """Root target"""
    system_name = platform.system()
    ctl.conf(
        # Root context
        is_linux=system_name == "Linux",
        is_macos=system_name == "Darwin",
        user=dict(
            home="{{ env.HOME }}",
            bin="{{ user.home }}/.local/bin",
            opt="{{ user.home }}/.local/opt",
            config="{{ user.home }}/.config",
            cache="{{ user.home }}/.cache",
        ),
        env=os.environ,
        terminal=dict(
            font_family="{{ dep('//fonts').FiraCode }}",
            font_size=12,
        ),
    )


def setup(ctl):
    if ctl.is_linux:
        ctl.dep("//tools/i3")
        ctl.dep("//tools/rofi")

    elif ctl.is_macos:
        ctl.dep("//tools/homebrew")

    ctl.dep("//tools/zsh")
    ctl.dep("//tools/pyenv")
    ctl.dep("//tools/nvm")

    ctl.dep("//tools/kitty")
    ctl.dep("//tools/nvim")
