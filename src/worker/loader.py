from .dataset import Dataset
import pathlib

class Loader:
    def load(self, options):
        dataset_name = options['dataset_load'].pop(0)
        options['dataset'].add(dataset_name, options)

    def save(self, options):
        dirName = options['dataset_save']
        pathlib.Path(dirName).mkdir(parents=True, exist_ok=True)
        dataset = options['dataset']
        if len(dataset.train.data) != 0:
            dataset.train.save(dirName, 'train')
            print(f'saving {len(dataset.train.data)}')
        if len(dataset.dev.data) != 0:
            dataset.dev.save(dirName, 'dev')
        if len(dataset.test.data) != 0:
            dataset.test.save(dirName, 'test')
        if len(dataset.blind.data) != 0:
            dataset.blind.save(dirName, 'blind')