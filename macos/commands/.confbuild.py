from pathlib import Path

SIMPLE_COMMANDS = [
    
]



COMMANDS = """
# ⌘ ⇧ ⌥ ⌃
Spaces
    [🚀] Focus Space 1 (⌘ 1)
        # configured manually

Windows
    [] Focus Right ()
    [] Move Active Window to Space 1 (right_command right_shift 1)



Command:
- icon/title/description
- context/conditions (active app, enabled mode)
- shortcut
- searchable
- command/action
    - defined separately
    - with or without args
    - can be triggered via shortcut/terminal/raycast

"""







RAYCAST_COMMAND_TEMPLATE = """
#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title {title}
# @raycast.mode fullOutput
# @raycast.icon {icon}
# @raycast.packageName {category}

{command}
"""

def commands(conf):
    conf(
        scripts_dir=conf['dir::{{ user.opt }}/scripts'],
    )

    for f in Path(__file__).parent.rglob('*.sh'):
        sh = conf.scripts_dir / f.name
        conf.render(f, sh)
        sh.chmod(0o700)

    for cmd in SIMPLE_COMMANDS:
        sh = conf.scripts_dir / cmd['name']
        sh.write_text(
            conf.render_str(RAYCAST_COMMAND_TEMPLATE.format(**cmd))
        )
        sh.chmod(0o700)

