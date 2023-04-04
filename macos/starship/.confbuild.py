def main(conf):
    conf['brew::starship']
    conf(
        zsh_rc='eval "$(starship init zsh)"',
        config=conf['path::{{ user.config }}/starship.toml'],
    )
    conf.render('./starship.toml', conf.config)