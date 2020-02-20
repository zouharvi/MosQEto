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
                
        if hasattr(self, 'hter'):
            obj += f'hter: {self.hter}'

        # we omit alignment, tags_src and pe for now
        return obj