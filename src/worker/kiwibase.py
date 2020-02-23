#!/usr/bin/env python3
import yaml
import pathlib
from os.path import join

def load_kiwi_config(path):
    with open(path, 'r') as f:
        config = yaml.safe_load(f.read())
    return config

def mkdirs(name):
    # NOT USED
    path = join(['runs', name])
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

