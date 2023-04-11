def git(conf):
    conf[
        'brew::git', 
        'brew::gh',
        'brew::gnupg',
        # Experiment with
        'brew::gitui',
        'brew::lazygit',
    ]
    conf(
        name="Evgeny Lychkovsky",
        email="miphreal@gmail.com",
        config=conf['path::~/.gitconfig'],
        signingkey=conf['path::~/.ssh/id_github.pub'],
    )
    conf.render('.gitconfig.j2', conf.config)

