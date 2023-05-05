from pathlib import Path


def kitty(conf):
    conf(
        kitty_font=conf["../fonts"].FiraCodeRetina,
        kitty_conf=conf["path::{{ user.config }}/kitty/kitty.conf"],
        themes_dir=conf["dir::{{ user.config }}/kitty/kitty-themes"],
        theme="SpaceGray",
    )

    conf.render("./kitty.conf.j2", conf.kitty_conf)

    if not conf.themes_dir.exists():
        conf.sh("git clone --depth 1 https://github.com/dexpota/kitty-themes.git {{ themes_dir }}")

    conf.sh(f"cp -r {Path(__file__).parent}/icons/* {conf.kitty_conf.parent}")

    # reload kitty
    conf.sh("kill -USR1 $(pgrep -a kitty) | true")
