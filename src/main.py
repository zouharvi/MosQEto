#!/usr/bin/env python3
import argparse
import yaml
from dataset import Dataset
from worker import Worker

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MosQEto')
    parser.add_argument('config', type=argparse.FileType('r'), help='YAML experiment config file')
    args, unknown_args = parser.parse_known_args()
    # TODO do config parsing

    config = yaml.safe_load(args.config)
    for arg in unknown_args:
        sp = arg.split('=')
        if len(sp) != 2:
            raise Exception(f'Additional argument is not a key=value pair ({arg}).')
        config[sp[0]] = sp[1]

    if 'dataset' in config:
        config['dataset'] = Dataset(config['dataset']['lang'], config['dataset']['org'])
    
    if 'method' not in config:
        print(f'No `method` key in config, nothing to do.')
        exit()
    
    plan = config.pop('method')
    worker = Worker()

    for planI in plan:
        if hasattr(worker, planI):
            func = getattr(worker, planI)
            func(config)
        else:
            print(f'`{planI}` was not found on Worker.')