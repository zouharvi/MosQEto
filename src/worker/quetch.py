#!/usr/bin/env python3
import kiwi
import kiwibase as kb

class Quetch:
    def train(self, options):
        if options['use_kiwi']:
            kiwi.train(options['quetch_config'])
        print("Doing some heavy training with a train dataset of size:", len(options['dataset'].train.data))

    def test(self, options):
        sentence = options['dataset'].train.data[0]
        print(sentence)
        print("Doing some positive testing on my test data")

    def inference(self, options):
        kiwi_config = kb.load_kiwi_config(options['quetch_config'])
        if options['use_kiwi']:
            pred = kiwi.load_model(kiwi_config['load-model'])
            # TODO finish this:
            """
            src = ['a b c', 'd e f g']
            tgt = ['q w e r', 't y']
            align = ['0-0 1-1 1-2', '1-1 3-0']
            examples = [kiwi.constants.SOURCE: src,
                        kiwi.constants.TARGET: tgt,
                        kiwi.constants.ALIGNMENTS: align]
            predictor.predict(examples)
            """
            pred.predict(examples)

        print("Doing some inference on my blind data of size:", len(options['dataset'].blind.data))