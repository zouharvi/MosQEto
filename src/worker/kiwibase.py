#!/usr/bin/env python3
import yaml

def load_kiwi_config(path):
    with open(path, 'r') as f:
        config = yaml.safe_load(f.read())
    return config
