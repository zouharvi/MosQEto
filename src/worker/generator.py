from .dataset import Dataset
from .dataset import Sentence
from random import shuffle, random, choice
from copy import deepcopy

class Generator:
    def mix(self, options, call):
        shuffle(options['dataset'].train.data)

    def supersample(self, options, call):
        i = 1
        if len(call) != 0:
            i = int(call[0])
        
        sample = deepcopy(options['dataset'].train.data)
        for _ in range(i):
            options['dataset'].train.data += deepcopy(sample)

    def expand_post_edited(self, options, call):
        to_add = []
        for s in options['dataset'].train.data:
            if s.pe:
                to_add.append(Sentence(" ".join(s.src), " ".join(s.pe), None, None, " ".join((2*len(s.pe)+1)*["OK"]), None, None))
                s.pe = None
        options['dataset'].train.data += to_add
        options['dataset'].train.add_alignment()

    def synthetize_gold(self, options, call):
        case_insensitive = ('case_insensitive' in options['generator']) and (options['generator']['case_insensitive'])
        for s in options['dataset'].train.data:
            new_tags = []
            # start gap token
            new_tags.append(True)
            source = [ (x.lower() if case_insensitive else x) for x in s.pe ]
            for t in s.tgt:
                if (t.lower() if case_insensitive else t) in source:
                    new_tags.append(True)
                else:
                    new_tags.append(False)
                # gap token, always True for now
                new_tags.append(True)
            s.tags = new_tags

    def synthetize_random(self, options, call):
        all_words = set()

        do_change = 'change_prob' in options['generator']
        do_remove = 'remove_prob' in options['generator']
        do_append = 'append_prob' in options['generator']
        if do_append:
            append_p = options['generator']['append_prob']
        if do_remove:
            remove_p = options['generator']['remove_prob']
        if do_change:
            change_p = options['generator']['change_prob']

        train = options['dataset'].train
        # take all words
        for sentence in train.data:
            all_words.update(sentence.tgt)
        all_words = list(all_words)

        skip_next = False
        for i in range(len(train.data)):
            if i % 5000 == 0:
                print(f"{i/len(train.data)*100:.2f}%\r", end='')
            sentence = train.data[i]
            new_tgt = []
            new_tags = []
            for word in sentence.tgt:
                tag1 = sentence.tags.pop(0)
                tag2 = sentence.tags.pop(0)
                if not skip_next:
                    if do_change and random() < change_p:
                        # and (not word in ['.', '?', '!', '"', "'", ',', '(', ')']):
                        new_tags.append(tag1)
                        new_tags.append(False)
                        new_tgt.append(choice(all_words))
                    elif do_remove and random() < remove_p:
                        skip_next = True
                    elif do_append and random() < append_p:
                        # previous gap
                        new_tags.append(True)
                        # inserted word
                        new_tags.append(False)
                        # next gap
                        new_tags.append(tag1)
                        # next word
                        new_tags.append(tag2)
                        new_tgt.append(choice(all_words))
                        new_tgt.append(word)
                    else:
                        new_tags.append(tag1)
                        new_tags.append(tag2)
                        new_tgt.append(word)
                else:
                    new_tags.append(False)
                    new_tags.append(tag2)
                    new_tgt.append(word)
                    skip_next = False
            # final gap
            new_tags.append(sentence.tags.pop(0))
            sentence.tgt = new_tgt
            sentence.tags = new_tags

        print('100%   ')
        # should we modify the alignment surgically, or do it like this?
        train.add_alignment()