def main(conf):
    conf[
        "brew::zsh-history-substring-search",
        "brew::zsh-syntax-highlighting",
        "brew::zsh-autosuggestions",
    ]

    conf.render(".zprofile.j2", "~/.zprofile")
    conf.render(".zshenv.j2", "~/.zshenv")
    conf.render(".zshrc.j2", "~/.zshrc")

    # Do not output "Last login:" in the shell prompt
    conf.sh("touch ~/.hushlogin")
