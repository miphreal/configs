from pathlib import Path
import os

from confctl import Base, Param


"""
Console themes:
    BG: #EDEDED or #F0F0F0
    FG: ##343434
"""


class Configuration(Base):
    HOME = Param.PATH("~")
    TARGET = Param()
    tmux_plugin_manager_dir = Param.PATH("~/.tmux/plugins/tpm")
    tmp_repo = "https://github.com/tmux-plugins/tpm"
    fonts_repo = "https://github.com/ryanoasis/nerd-fonts"
    prezto_repo = "https://github.com/sorin-ionescu/prezto"
    project_aliases = Param()
    flags = Param(set())

    def _configure_fonts(self):
        fonts_dir = self.CACHE_DIR / "fonts"
        if not (fonts_dir / ".git").exists():
            self.run_sh(f"git clone --depth 1 {self.fonts_repo} {fonts_dir}")
            self.run_sh(f'bash {fonts_dir / "install.sh"}')

    def _configure_tmux(self):
        self.ensure_folders(self.tmux_plugin_manager_dir)
        if not (self.tmux_plugin_manager_dir / ".git").exists():
            self.run_sh(f"git clone {self.tmp_repo} {self.tmux_plugin_manager_dir}")
        self.template("tmux.conf.j2", symlink=self.HOME / ".tmux.conf")

    def _configure_prezto(self):
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
        for f in ("init", "alias", "nvm", "poetry", "pyenv"):
            self.template(
                f"zprezto-personal/{f}.zsh.j2", symlink=personal_module / f"{f}.zsh"
            )

    def _configure_kitty(self):
        self.ensure_folders("~/.config/kitty")
        if "full" in self.flags:
            self.run_sh(
                "curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin"
            )

        self.copy_file("kitty.conf", symlink=self.HOME / ".config/kitty/kitty.conf")

        kitty_theme = "Tomorrow"
        self.run_sh("git clone --depth 1 git@github.com:dexpota/kitty-themes.git ~/.config/kitty/kitty-themes")
        self.symlink("~/.config/kitty/theme.conf", f"~/.config/kitty/kitty-themes/themes/{kitty_theme}.conf", )

    def get_project_aliases(self):
        project_aliases = []

        for prj in Path("~/Develop").expanduser().iterdir():
            prjbin = prj / prj.name
            if prjbin.exists() and prjbin.is_file() and os.access(prjbin, os.X_OK):
                with prjbin.open("rt") as script_file:
                    script_text = script_file.read()
                    if "# confctl.console:gen-alias" in script_text:
                        self.info(f"* Found project management script: {prjbin}")
                        project_aliases.append([prj.name, f"source {prjbin}"])

        return project_aliases

    def configure(self):
        self.project_aliases = self.get_project_aliases()

        self.copy_file("profile", "~/.profile")

        self._configure_kitty()
        self._configure_fonts()
        # self._configure_tmux()
        self._configure_prezto()
