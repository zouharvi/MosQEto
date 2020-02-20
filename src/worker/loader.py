from .dataset import Dataset
import pathlib

class Loader:
    def load(self, options):
        options['dataset'] = Dataset(options['dataset_load']['lang'], options['dataset_load']['org'])

    def save(self, options):
        dirName = options['dataset_save']
        pathlib.Path(dirName).mkdir(parents=True, exist_ok=True)
        dataset = options['dataset']
        if hasattr(dataset, 'train'):
            dataset.train.save(dirName, 'train')
        if hasattr(dataset, 'dev'):
            dataset.dev.save(dirName, 'dev')
        if hasattr(dataset, 'test'):
            dataset.test.save(dirName, 'test')
        if hasattr(dataset, 'blind'):
            dataset.blind.save(dirName, 'blind')