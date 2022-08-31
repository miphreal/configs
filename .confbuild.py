import os


def main(ctl):
    """Root target"""
    ctl.conf(
        # Root context
        user=dict(
            home="{{ env.HOME }}",
            bin="{{ user.home }}/.local/bin",
            opt="{{ user.home }}/.local/opt",
            config="{{ user.home }}/.config",
            cache="{{ user.home }}/.cache",
        ),
        env=os.environ,
        terminal=dict(
            font_family=ctl.dep("//fonts/fira_code").font_name,
            font_size=12,
        ),
    )
