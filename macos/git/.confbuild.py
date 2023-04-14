def git(conf):
    conf[
        'brew::git', 
        'brew::git-lfs',
        'brew::gh',
        'brew::gnupg',
        ':lazygit',
    ]
    conf(
        name="Evgeny Lychkovsky",
        email="miphreal@gmail.com",
        config=conf['path::~/.gitconfig'],
        signingkey=conf['path::~/.ssh/id_github.pub'],
    )
    conf.render('.gitconfig.j2', conf.config)


def lazygit(conf):
    conf['brew::lazygit']
    conf(
        lazygit_config=conf['path::~/Library/Application Support/lazygit/config.yml'],
    )
    conf.render('lazygit_config.yml.j2', conf.lazygit_config)
