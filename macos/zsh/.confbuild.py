def main(conf):
    conf.render(".zprofile.j2", "~/.zprofile")
    conf.render(".zshenv.j2", "~/.zshenv")
    conf.render(".zshrc.j2", "~/.zshrc")
    