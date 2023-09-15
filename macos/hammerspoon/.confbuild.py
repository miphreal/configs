import json
import typing as t
from pathlib import Path


def hammerspoon(conf):
    conf['brew::hammerspoon']
    conf(conf_dir='{{ env.HOME }}/.hammerspoon')
    conf.sh('ln -fs "{{ current_config_dir }}" "{{ conf_dir }}"')

