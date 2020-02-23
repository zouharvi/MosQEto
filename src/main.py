#!/usr/bin/env python3
import argparse
import yaml
import worker

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

    if 'method' not in config:
        print(f'No `method` key in config, nothing to do.')
        exit()
    
    config['dataset'] = worker.dataset.Dataset()

    # dynamically load a worker class
    plan = config.pop('method')

    workers = {}
    for wMethod in plan:
        workerName, method = wMethod.split(':')

        if workerName in workers:
            workerObj = workers[workerName]
        else:
            if hasattr(worker, workerName):
                workerObj = getattr(worker, workerName)()
            else:
                print(f'`{workerName}` class not found')
                continue
        workers[workerName] = workerObj

        if hasattr(workerObj, method):
            func = getattr(workerObj, method)
            func(config)
        else:
            print(f'`{method}` was not found on {workerName}.')