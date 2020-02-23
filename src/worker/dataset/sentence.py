class Sentence():
    def __init__(self, src, tgt, alignment, pe, tags, tags_src, hter):
        if src:
            self.src = src.rstrip('\n').split(' ')
        if tgt:
            self.tgt = tgt.rstrip('\n').split(' ')
        if pe:
            self.pe  =  pe.rstrip('\n').split(' ')
        if tags:
            self.tags     = [x == 'OK' for x in tags.rstrip('\n').split(' ')]
        if tags_src:
            self.tags_src = [x == 'OK' for x in tags_src.rstrip('\n').split(' ')]
        if hter:
            self.hter = float(hter)
        if alignment:
            self.alignment = [(int(x.split('-')[0]), int(x.split('-')[1])) for x in alignment.split(' ')]

    def __str__(self):
        def pTag(tag):
            return '1' if tag else '0'

        topline = ''.rjust(60, '-')

        if len(self.tgt) == 0:
            return '<Sentence Missing>'

        tgtLine = ' '
        qeLine = ''

        for i in range(len(self.tgt)):
            word = self.tgt[i]
            tgtLine += word + ' '
            if hasattr(self, 'tags'):
                qeLine += pTag(self.tags[2*i])
                qeLine += pTag(self.tags[2*i+1])
            qeLine += ''.rjust(len(word)-1)

        return f'{topline}\n{" ".join(self.src)}\n{tgtLine}\n{qeLine}'

        # if hasattr(self, 'hter'):
        #     obj += f'hter: {self.hter}'

        # we omit alignment, tags_src and pe for now

    def add_ok_tags(self):
        self.tags = [True]*(2*len(self.tgt)+1)