def main(conf):
    # conf["brew::tmux"]
    conf(
        tmux_plugin_manager_dir=conf["dir::~/.tmux/plugins/tpm"],
        tmp_repo="https://github.com/tmux-plugins/tpm",
        config=conf["path::{{ env.HOME }}/.tmux.conf"],
    )
    if not (conf.tmux_plugin_manager_dir / ".git").exists():
        conf.sh(f"git clone {conf.tmp_repo} {conf.tmux_plugin_manager_dir}")

    conf.render("./tmux.conf.j2", conf.config)

