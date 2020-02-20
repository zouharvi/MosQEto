import pathlib
import urllib.request
import tarfile
from .data import Data

class Dataset:
    """
    Structure for handling WMT data. Basic example unit is a Sentence.

    ```
    dataEnDe = Dataset('en-de', 'wmt19')
    print('WMT19 en-de train:', len(dataEnDe.train.data)) # 13442
    ```
    """
    def _set_wmt19(self, lang):
        wmt19dir = self._datafolder / 'wmt19'
        wmt19dir.mkdir(exist_ok=True)
        langdir = wmt19dir / lang

        # Here we assume that if the lang directory exists, it contains correct files 
        if not langdir.exists():
            print(f'wmt19/{lang} folder not found')
            langdir.mkdir()

            for kind in ['test', 'blindtest', 'traindev']:
                print(f'Downloading wmt19/{lang}-{kind}')
                URL = f'https://deep-spin.github.io/docs/data/wmt2019_qe/task1_{lang}_{kind}.tar.gz'
                ftpstream = urllib.request.urlopen(URL)
                tarf = tarfile.open(fileobj=ftpstream, mode="r|gz")
                tarf.extractall(path=langdir.absolute())

        self.test = Data()
        self.test.readWMT(langdir, 'test')

        self.dev = Data()
        self.dev.readWMT(langdir, 'dev')

        self.train = Data()
        self.train.readWMT(langdir, 'train')

        self.blind = Data()
        self.blind.readWMTBlind(langdir, f'task1_{lang}_blindtest')

    def __init__(self, lang, org='wmt19'):
        self._datafolder = pathlib.Path().parent / 'data_raw'
        self._datafolder.mkdir(parents=True, exist_ok=True)

        if org == 'wmt19':
            if lang in ['en-de', 'en-ru']:
                self._set_wmt19(lang)
                return

        raise Exception(f"Unsupported dataset {org}/{lang}")