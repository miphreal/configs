from confctl import Base, Param


deps = """
    # network utils
    ca-certificates
    curl
    mtr
    wget
    sshpass
    openvpn

    # sys monitors
    htop
    iotop
    dstat
    pv

    # network
    slurm

    # file manager
    mc
    ranger
    tree

    # archives
    atool

    # X11
    xclip
    xsel

    # Python related
    python-pip
    python-gobject

    # Other
    gparted

    # Build-related
    build-essential
    python-dev
    llvm
    libssl-dev
    zlib1g-dev
    libbz2-dev
    libreadline-dev
    libsqlite3-dev
    libpq-dev

    # Other Media
    vlc

    # Audio
    pulseaudio
    pavucontrol
"""


class Configuration(Base):
    HOME = Param.PATH("~")
    flags = Param({"no:full"})

    def configure(self):
        if "full" in self.flags:
            self.install_packages(deps)

        self.ensure_folders(
            self.HOME / ".local/bin",
            self.HOME / ".local/opt",
        )
