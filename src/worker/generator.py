from .dataset import Dataset
from random import shuffle

class Generator:
    def mix(self, options):
        print('Mixing training datasets')
        print(options['dataset'].train.data[0])
        shuffle(options['dataset'].train.data)
        print(options['dataset'].train.data[0])