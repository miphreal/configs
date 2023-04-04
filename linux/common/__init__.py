from confctl import Base, Param


apt_deps = """
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
    procps
    ## network interface monitor
    slurm

    # file manager
    git
    mc
    ranger
    tree
    fzf
    file

    # archives
    atool

    # X11
    xclip
    xsel

    # Python related
    # python-pip
    # python-gobject

    # Other
    flameshot
    peek
    gparted
    exa

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
            self.install_packages(apt_deps)
            self.run_sh(
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            )

        self.ensure_folders(
            self.HOME / ".local/bin", self.HOME / ".local/opt",
        )
