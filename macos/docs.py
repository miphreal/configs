def main(conf):
    conf[
        './pandoc',
        './latex',
    ]

def pandoc(conf):
    conf['brew::pandoc']

def latex(conf):
    conf['brew::mactex']
    conf(
        bin_dir='/Library/TeX/texbin',
    )

