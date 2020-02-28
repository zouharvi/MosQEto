from .dataset import Dataset
import pathlib
from pathlib import Path
import shutil

class Loader:
    def rmdir(self, options, call):
        if len(call) == 1 and Path(call[0]).is_dir():
            shutil.rmtree(call[0])

    def flush(self, options, call):
        options['dataset'] = Dataset()

    def load(self, options, call):
        dataset_name = options['dataset_load'].pop(0)
        align = True
        if 'noalign' in call:
            align = False
        options['dataset'].add(dataset_name, options, align)

    def save(self, options, call):
        dirName = options['dataset_save'].pop(0)
        if Path(dirName).is_dir():
            shutil.rmtree(dirName)
        pathlib.Path(dirName).mkdir(parents=True, exist_ok=True)
        dataset = options['dataset']
        if len(dataset.train.data) != 0:
            dataset.train.save(dirName, 'train')
            print(f'Saving {len(dataset.train.data)} sentences to {dirName}')
        if len(dataset.dev.data) != 0:
            dataset.dev.save(dirName, 'dev')
        if len(dataset.test.data) != 0:
            dataset.test.save(dirName, 'test')
        if len(dataset.blind.data) != 0:
            dataset.blind.save(dirName, 'blind')