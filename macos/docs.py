def main(conf):
    conf[
        './pandoc',
        './latex',
    ]

def pandoc(conf):
    conf['brew::pandoc']

def latex(conf):
    conf['brew::basictex']
    conf(
        bin_dir='/Library/TeX/texbin',
    )

