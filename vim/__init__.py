from confctl import Base, Param


class Configuration(Base):
    HOME = Param.PATH("~")
    NVIM_CONFIG_DIR = Param.PATH("~/.config/nvim")
    flags = Param(set())

    def configure(self):
        if "full" in self.flags:
            self.install_packages(
                """
                neovim
                python3-neovim
                """
            )

        self.ensure_folders(self.NVIM_CONFIG_DIR)
        self.template("init.vim.j2", self.NVIM_CONFIG_DIR / "init.vim")

        if "full" in self.flags:
            _vim_plug_url = (
                "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
            )
            _vim_plug_dst = self.HOME / ".local/share/nvim/site/autoload/plug.vim"
            self.run_sh(f"curl -fLo {_vim_plug_dst} --create-dirs {_vim_plug_url}")

        self.run_sh("nvim +PlugInstall +qall")
