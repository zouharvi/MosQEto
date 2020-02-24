from .dataset import Dataset

class DataUtils:
    def gap_only(self, options):
        for s in options['dataset'].train.data:
            s.tags = s.tags[::2]
        for s in options['dataset'].dev.data:
            s.tags = s.tags[::2]
        for s in options['dataset'].test.data:
            s.tags = s.tags[::2]