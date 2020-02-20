import pathlib
import urllib.request
import tarfile

class Dataset:
    """
    Structure for handling WMT data. Basic example unit is a Sentence.

    ```
    dataEnDe = Dataset('en-de', 'wmt19')
    print('WMT19 en-de train:', len(dataEnDe.train.data)) # 13442
    ```
    """

    class Sentence():
        def __init__(self, src, tgt, alignment, pe, tags, tags_src, hter, blind=False):
            self.blind = blind
            if not blind:
                self.src = src.split(' ')
                self.tgt = tgt.split(' ')
                self.pe  =  pe.split(' ')
                self.tags     = [x == 'OK' for x in tags.split(' ')]
                self.tags_src = [x == 'OK' for x in tags_src.split(' ')]
                self.hter = float(hter)
                self.alignment = [(int(x.split('-')[0]), int(x.split('-')[1])) for x in alignment.split(' ')]
            else:
                self.src = src.split(' ')
                self.tgt = tgt.split(' ')
                self.alignment = [(int(x.split('-')[0]), int(x.split('-')[1])) for x in alignment.split(' ')]

        def __str__(self):
            obj = ' '.join(self.src)
            maxTgt = max([len(x) for x in self.tgt])

            def pTag(tag):
                return '1' if tag else '0'

            for i in range(len(self.tgt)):
                if i == len(self.tgt)-1:
                    obj += self.tgt[i].rstrip('\n').rjust(maxTgt) + ' '
                    obj += f'{pTag(self.tags[2*i+1])} ↑{pTag(self.tags[2*i])} ↓{pTag(self.tags[2*i+2])}\n'
                else:
                    obj += self.tgt[i].rjust(maxTgt) + ' '
                    obj += f'{pTag(self.tags[2*i+1])} ↑{pTag(self.tags[2*i])}\n'
                    
            if not self.blind:
                obj += f'hter: {self.hter}'

            # we omit alignment, tags_src and pe for now
            return obj

    class Data():
        def __init__(self, dir, name, blind=False):
            self.data = []

            def readFileLines(extension):
                with open((dir/name/f'{name}.{extension}').absolute(),'r') as f:
                    return f.readlines()

            def readFileLinesBlind(extension):
                with open((dir/name/f'test.{extension}').absolute(),'r') as f:
                    return f.readlines()
            
            if not blind:
                src = readFileLines('src')
                tgt = readFileLines('mt')
                pe = readFileLines('pe')
                hter = readFileLines('hter')
                tags = readFileLines('tags')
                tags_src = readFileLines('source_tags')
                alignment = readFileLines('src-mt.alignments')
                for args in zip(src, tgt, alignment, pe, tags, tags_src, hter):
                    self.data.append(Dataset.Sentence(*args, blind=False))
            else:
                src = readFileLinesBlind('src')
                tgt = readFileLinesBlind('mt')
                alignment = readFileLinesBlind('src-mt.alignments')
                for args in zip(src, tgt, alignment):
                    self.data.append(Dataset.Sentence(*args, pe=None, tags=None, tags_src=None, hter=None, blind=True))

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

        self.test  = self.Data(langdir, 'test')
        self.dev   = self.Data(langdir, 'dev')
        self.train = self.Data(langdir, 'train')
        self.blind = self.Data(langdir, f'task1_{lang}_blindtest', blind=True)

    def __init__(self, lang, org='wmt19'):
        self._datafolder = pathlib.Path().parent / 'data_raw'
        self._datafolder.mkdir(parents=True, exist_ok=True)

        if org == 'wmt19':
            if lang in ['en-de', 'en-ru']:
                self._set_wmt19(lang)
                return

        raise Exception(f"Unsupported dataset {org}/{lang}")