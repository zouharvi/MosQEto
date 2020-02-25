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
                to_add.append(Sentence(" ".join(s.src), " ".join(s.pe), None, None, " ".join((len(s.pe)+1)*"OK"), None, None))
                s.pe = None
        options['dataset'].train.data += to_add

    def generate(self, options, call=[]):
        print('Generating (this may take a while)')
        remove_p = options['generator']['remove_prob']
        add_p = options['generator']['add_unigram_prob']
        change_p = options['generator']['change_unigram_prob']
        all_words = set()

        train = options['dataset'].train
        # take all words
        for sentence in train.data:
            all_words.update(sentence.tgt)
        all_words = list(all_words)

        for i in range(len(train.data)):
            if i % 5000 == 0:
                print(f"{i/len(train.data)*100:.2f}%\r", end='')
            sentence = train.data[i]
            new_tgt = []
            new_tags = []
            for word in sentence.tgt:
                tag1 = sentence.tags.pop(0)
                tag2 = sentence.tags.pop(0)
                if random() < change_p:
                    new_tags.append(tag1)
                    new_tags.append(False)
                    new_tgt.append(choice(all_words))
                else:
                    new_tags.append(tag1)
                    new_tags.append(tag2)
                    new_tgt.append(word)
                # elif random() < add_p:
                #     new_tgt.append(choice(all_words))
                #     # the space is probably ok
                #     new_tags.append(True)
                #     new_tags.append(False)
                #     new_tgt.append(word)
                #     new_tags.append(sentence.tags.pop(0))
                #     new_tags.append(sentence.tags.pop(0))
                # elif random() < remove_p:
                #     sentence.tags.pop(0)
                #     sentence.tags.pop(0)
                #     continue
                # else:
                #     new_tgt.append(word)
                #     new_tags.append(sentence.tags.pop(0))
                #     new_tags.append(sentence.tags.pop(0))

            # final gap
            new_tags.append(sentence.tags.pop(0))
            sentence.tgt = new_tgt
            sentence.tags = new_tags

        # should we modify the alignment surgically, or do it like this?
        train.add_alignment()