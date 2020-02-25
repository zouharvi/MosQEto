from .sentence import Sentence
import subprocess
import os
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

    def readParallel(self, file1, file2):
        with open(file1, 'r') as f:
            src = f.readlines()
        with open(file2, 'r') as f:
            tgt = f.readlines()
        for args in zip(src, tgt):
            sentence = Sentence(*args, alignment=None, pe=None, tags=None, tags_src=None, hter=None)
            sentence.add_ok_tags()
            self.data.append(sentence)

    def add_alignment(self):
        print('Doing alignment (this may take a while)')
        
        with open('.tmp', 'w') as f:
            out = []
            for s in self.data:
                out.append(f'{" ".join(s.src)} ||| {" ".join(s.tgt)}')
            f.write("\n".join(out))
        command = './fast_align/build/fast_align -i .tmp'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        output, _error = process.communicate()
        os.remove('.tmp')
        # print(_error)
        
        alignments = output.decode('utf-8').split('\n')
        # last line is empty
        alignments.pop()

        newdata = []
        for s, a in zip(self.data, alignments):
            # removing sentences, which were not alignable
            if a == '':
                continue
            s.add_alignment(a)
            newdata.append(s)
        self.data = newdata


    def save(self, dirName, name):
        root = (pathlib.Path(dirName) / name).absolute()
        pathlib.Path(root).mkdir(parents=True, exist_ok=True)
        
        fpref = f'{root}/{name}.'
        with open(f'{fpref}mt', 'w') as fMT, open(f'{fpref}src', 'w') as fSRC:
            for sentence in self.data:
                print(' '.join(sentence.tgt), file=fMT)
                print(' '.join(sentence.src), file=fSRC)

        if all(hasattr(s, 'alignment') for s in self.data):
            with open(f'{fpref}src-mt.alignments', 'w') as fPE:
                for sentence in self.data:
                    print(' '.join([f'{x[0]}-{x[1]}' for x in sentence.alignment]), file=fPE)

        if all(hasattr(s, 'pe') for s in self.data):
            with open(f'{fpref}pe', 'w') as fPE:
                for sentence in self.data:
                    print(' '.join(sentence.pe), file=fPE)
            
        if all(hasattr(s, 'tags') for s in self.data):
            with open(f'{fpref}tags', 'w') as fTAGS:
                for sentence in self.data:
                    print(' '.join(['OK' if x else 'BAD' for x in sentence.tags]), file=fTAGS)

        if all(hasattr(s, 'tags_src') for s in self.data):
            with open(f'{fpref}source_tags', 'w') as fTAGSSRC:
                for sentence in self.data:
                    print(' '.join(['OK' if x else 'BAD' for x in sentence.tags_src]), file=fTAGSSRC)

        if all(hasattr(s, 'hter') for s in self.data):
            with open(f'{fpref}hter', 'w') as fHTER:
                for sentence in self.data:
                    print(sentence.hter, file=fHTER)