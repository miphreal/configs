from confctl import Base, Param


class Configuration(Base):
    HOME = Param.PATH("~")
    NVIM_CONFIG_DIR = Param.PATH("~/.config/nvim")
    flags = Param(set())

    def configure(self):
        self.ensure_folders(self.NVIM_CONFIG_DIR)
        self.run_sh(f"mv {self.NVIM_CONFIG_DIR} $(mktemp -d)")

        self.ensure_folders(self.NVIM_CONFIG_DIR)
        self.run_sh(
            f"cp -R {self.CONFIGURATION_DIR / 'nvim/*'} {self.NVIM_CONFIG_DIR}/"
        )

        if "full" in self.flags:
            self.run_sh(
                "git clone https://github.com/wbthomason/packer.nvim ~/.local/share/nvim/site/pack/packer/start/packer.nvim"
            )
