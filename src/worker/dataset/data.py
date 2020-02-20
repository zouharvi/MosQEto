from .sentence import Sentence
import pathlib

class Data():
    def __init__(self):
        self.data = []

    def readWMT(self, dir, name):
        def readFileLines(extension):
            with open((dir/name/f'{name}.{extension}').absolute(),'r') as f:
                return f.readlines()
        src = readFileLines('src')
        tgt = readFileLines('mt')
        alignment = readFileLines('src-mt.alignments')
        pe = readFileLines('pe')
        hter = readFileLines('hter')
        tags = readFileLines('tags')
        tags_src = readFileLines('source_tags')
        for args in zip(src, tgt, alignment, pe, tags, tags_src, hter):
            self.data.append(Sentence(*args))

    def readWMTBlind(self, dir, name):
        def readFileLinesBlind(extension):
            with open((dir/name/f'test.{extension}').absolute(),'r') as f:
                return f.readlines()
        src = readFileLinesBlind('src')
        tgt = readFileLinesBlind('mt')
        alignment = readFileLinesBlind('src-mt.alignments')
        for args in zip(src, tgt, alignment):
            self.data.append(Sentence(*args, pe=None, tags=None, tags_src=None, hter=None))

    def readParallel(self, dir, name):
        pass

    def save(self, dirName, name):
        root = (pathlib.Path(dirName) / name).absolute()
        pathlib.Path(root).mkdir(parents=True, exist_ok=True)
        
        fpref = f'{root}/{name}.'
        with open(f'{fpref}mt', 'w') as fMT, open(f'{fpref}src', 'w') as fSRC:
            for sentence in self.data:
                print(' '.join(sentence.tgt), file=fMT)
                print(' '.join(sentence.src), file=fSRC)

        # we are using the last sentence for testing whether all of the sentences have such attributes

        if hasattr(sentence, 'alignment'):
            with open(f'{fpref}src-mt.alignments', 'w') as fPE:
                for sentence in self.data:
                    print(' '.join([f'{x[0]}-{x[1]}' for x in sentence.alignment]), file=fPE)

        if hasattr(sentence, 'pe'):
            with open(f'{fpref}pe', 'w') as fPE:
                for sentence in self.data:
                    print(' '.join(sentence.pe), file=fPE)
            
        if hasattr(sentence, 'tags'):
            with open(f'{fpref}tags', 'w') as fTAGS:
                for sentence in self.data:
                    print(' '.join(['OK' if x else 'BAD' for x in sentence.tags]), file=fTAGS)

        if hasattr(sentence, 'tags_src'):
            with open(f'{fpref}source_tags', 'w') as fTAGSSRC:
                for sentence in self.data:
                    print(' '.join(['OK' if x else 'BAD' for x in sentence.tags_src]), file=fTAGSSRC)

        if hasattr(sentence, 'hter'):
            with open(f'{fpref}hter', 'w') as fHTER:
                for sentence in self.data:
                    print(sentence.hter, file=fHTER)