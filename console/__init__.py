from confctl import Base, Param


"""
Console themes:
    BG: #EDEDED or #F0F0F0
    FG: ##343434
"""


class Configuration(Base):
    HOME = Param.PATH("~")
    TARGET = Param()
    YJ_PROJECT_ROOT = Param.PATH("~/Develop/yunojuno/platform")
    tmux_plugin_manager_dir = Param.PATH("~/.tmux/plugins/tpm")
    tmp_repo = "https://github.com/tmux-plugins/tpm"
    fonts_repo = "https://github.com/ryanoasis/nerd-fonts"
    prezto_repo = "https://github.com/sorin-ionescu/prezto"

    def configure(self):
        # patched fonts
        fonts_dir = self.CACHE_DIR / "fonts"
        if not (fonts_dir / ".git").exists():
            self.run_sh(f"git clone --depth 1 {self.fonts_repo} {fonts_dir}")
            self.run_sh(f'bash {fonts_dir / "install.sh"}')

        # tmux
        self.ensure_folders(self.tmux_plugin_manager_dir)
        if not (self.tmux_plugin_manager_dir / ".git").exists():
            self.run_sh(f"git clone {self.tmp_repo} {self.tmux_plugin_manager_dir}")
        self.template("tmux.conf.j2", symlink=self.HOME / ".tmux.conf")

        # prezto
        prezto_dir = self.HOME / ".zprezto"
        if not (prezto_dir / ".git").exists():
            self.run_sh(f'git clone --recursive {self.prezto_repo} "{prezto_dir}"')

        if not (self.HOME / ".zpreztorc").exists():
            init_zprezto = """
setopt EXTENDED_GLOB
for rcfile in "${ZDOTDIR:-$HOME}"/.zprezto/runcoms/^README.md(.N); do
ln -s "$rcfile" "${ZDOTDIR:-$HOME}/.${rcfile:t}"
done
"""
            self.logger.warning(
                f"You may need to manually setup `zprezto`: \n{init_zprezto}"
            )
        else:
            self.template("zpreztorc.j2", symlink=self.HOME / ".zpreztorc")
            self.template("zprofile.j2", symlink=self.HOME / ".zprofile")

        # `personal` zprezto module
        personal_module = prezto_dir / "modules/personal"
        self.ensure_folders(personal_module)
        self.template(
            "zprezto-personal/init.zsh.j2", symlink=personal_module / "init.zsh"
        )
        self.template(
            "zprezto-personal/alias.zsh.j2", symlink=personal_module / "alias.zsh"
        )
        self.template(
            "zprezto-personal/projects.zsh.j2", symlink=personal_module / "projects.zsh"
        )
