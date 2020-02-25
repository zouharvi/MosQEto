import pathlib
import urllib.request
from zipfile import ZipFile
from io import BytesIO
import tarfile
from .data import Data


class Dataset:
    """
    Structure for handling WMT data. Basic example unit is a Sentence.
    """

    def _set_wmt19(self, lang):
        wmt19dir = self._datafolder / 'wmt19'
        wmt19dir.mkdir(exist_ok=True)
        langdir = wmt19dir / lang

        # Here we assume that if the lang directory exists, it contains correct files
        if not langdir.exists():
            print(f'wmt19/{lang} folder not found, downloading')
            langdir.mkdir()

            for kind in ['test', 'blindtest', 'traindev']:
                print(f'Downloading wmt19/{lang}-{kind}')
                URL = f'https://deep-spin.github.io/docs/data/wmt2019_qe/task1_{lang}_{kind}.tar.gz'
                ftpstream = urllib.request.urlopen(URL)
                tarf = tarfile.open(fileobj=ftpstream, mode="r|gz")
                tarf.extractall(path=langdir.absolute())

        self.test.readWMT(langdir, 'test')
        self.dev.readWMT(langdir, 'dev')
        self.train.readWMT(langdir, 'train')
        self.blind.readWMTBlind(langdir, f'task1_{lang}_blindtest')
        print(f'Loaded WMT19, {len(self.train.data)} train sentences in total')

    def _get_opus(self, name, ver, lang1, lang2):
        datadir = self._datafolder / 'opus' / name
        if not datadir.exists():
            print(f'opus/{name} folder not found, downloading')
            datadir.mkdir(parents=True, exist_ok=True)

            URL = f'https://object.pouta.csc.fi/OPUS-{name}/{ver}/moses/{lang1}-{lang2}.txt.zip'
            resp = urllib.request.urlopen(URL)
            zfile = ZipFile(BytesIO(resp.read()))
            text1 = zfile.open(f'{name}.{lang1}-{lang2}.{lang1}').read().decode('utf-8')
            text2 = zfile.open(f'{name}.{lang1}-{lang2}.{lang2}').read().decode('utf-8')
            with open((datadir/f'{lang1}-{lang2}.{lang1}').absolute(), 'w') as f:
                f.write(text1)
            with open((datadir/f'{lang1}-{lang2}.{lang2}').absolute(), 'w') as f:
                f.write(text2)

        return ( datadir / f'{lang1}-{lang2}.{lang1}' ), ( datadir / f'{lang1}-{lang2}.{lang2}' ) 

    def _set_opus_tech(self, options, align):
        self.train.readParallel(*self._get_opus('KDE4', 'v2', 'de', 'en'))
        self.train.readParallel(*self._get_opus('GNOME', 'v1', 'de', 'en'))
        self.train.readParallel(*self._get_opus('Ubuntu', 'v14.10', 'de', 'en'))
        self.train.readParallel(*self._get_opus('PHP', 'v1', 'de', 'en'))
        print(f'Loaded technical domain from OPUS, {len(self.train.data)} sentences in total')
        if align:
            self.train.add_alignment()

    def _set_custom(self, name, options):
        langdir = pathlib.Path(name)
        if (langdir/'test').exists():
            self.test.readWMT(langdir, 'test')
        if (langdir/'dev').exists():
            self.dev.readWMT(langdir, 'dev')
        if (langdir/'train').exists():
            # is it parallel or full WMT?
            if (langdir/'train/train.tags').exists():
                self.train.readWMT(langdir, 'train')
            else:
                self.train.readParallel(langdir/'train.src', langdir/'train.mt')
        if (langdir/'blind').exists():
            self.blind.readWMTBlind(langdir, 'blind')

        print(f'Loaded custom data {name}, {len(self.train.data)} sentences in total')

    def __init__(self):
        # we may be wasting memory by always creating such data, but hopefully they are stored efficiently
        self.test = Data()
        self.dev = Data()
        self.train = Data()
        self.blind = Data()

        self._datafolder = pathlib.Path().parent / 'data_raw'
        self._datafolder.mkdir(parents=True, exist_ok=True)

    def add(self, name, options, align=False):
        name = name.split('/')
        if name[0] == 'wmt19':
            if name[1] in ['en-de', 'en-ru']:
                self._set_wmt19(name[1])
                return
        elif name[0] == 'opus' and name[1] == 'tech':
            if name[2] in ['en-de']:
                self._set_opus_tech(options, align)
                return
        elif name[0] == 'custom':
            self._set_custom(name[1], options)
            return

        raise Exception(f"Unsupported dataset {name}")
