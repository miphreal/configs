from pathlib import Path


def nvim(conf):
    conf(
        nvim_config_src_dir="{{ env.HOME }}/Develop/nvim-config",
        nvim_config_dir=conf["dir::{{ user.config }}/nvim"],
    )

    if Path(conf.nvim_config_dir).exists():
        conf.sh("mv {{ nvim_config_dir }} $(mktemp -d --suffix=nvim-conf)")

    conf.sh("cp -R {{ nvim_config_src_dir }}/* {{ nvim_config_dir }}/")

    if "full" in conf.ctx:
        conf.sh(
            "git clone https://github.com/wbthomason/packer.nvim ~/.local/share/nvim/site/pack/packer/start/packer.nvim"
        )

    conf.sh("rm -rf {{ nvim_config_dir }}/plugin/packer_compiled.lua")
