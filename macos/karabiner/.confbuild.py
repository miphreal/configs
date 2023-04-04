def karabiner(conf):
    conf['brew::karabiner-elements']
    conf(config=conf['path::{{ user.config }}/karabiner/karabiner.json'])
    conf.render('karabiner.json', conf.config)