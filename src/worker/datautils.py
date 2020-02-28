from .dataset import Dataset

class DataUtils:
    def gap_only(self, options, call):
        for s in options['dataset'].train.data:
            s.tags = s.tags[::2]
        for s in options['dataset'].dev.data:
            s.tags = s.tags[::2]
        for s in options['dataset'].test.data:
            s.tags = s.tags[::2]
        
    def head(self, options, call):
        length = 10
        if len(call) == 1:
            length = int(call[0])
        options['dataset'].train.data = options['dataset'].train.data[:length]

    def flush_train(self, options, call):
        options['dataset'].train.data = []

    def info(self, options, call):
        t_tgt = 0
        f_tgt = 0
        t_gap = 0
        f_gap = 0
        for s in options['dataset'].train.data:
            t_tgt += sum([1*(x==True) for x in s.tags[1::2]])
            f_tgt += sum([1*(x==False) for x in s.tags[1::2]])
            t_gap += sum([1*(x==True) for x in s.tags[0::2]])
            f_gap += sum([1*(x==False) for x in s.tags[0::2]])
        t_all = t_tgt + t_gap
        f_all = f_tgt + f_gap
        if t_all == 0 and f_all == 0:
            print('No training data')
        else:
            print(f'Target: |{t_tgt:9}|{f_tgt:9}|{t_tgt/(t_tgt+f_tgt)*100:6.2f}|')
            print(f'Gaps:   |{t_gap:9}|{f_gap:9}|{t_gap/(t_gap+f_gap)*100:6.2f}|')
            print(f'All:    |{t_all:9}|{f_all:9}|{t_all/(t_all+f_all)*100:6.2f}|')