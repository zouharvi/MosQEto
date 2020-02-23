#!/usr/bin/env python3
import kiwi
import worker.kiwibase as kb

class Quetch:
    def train(self, options):
        print("Doing some heavy training with a train dataset of size:", len(options['dataset'].train.data))
        kiwi.train(options['quetch_train'])

    def test(self, options):
        raise NotImplementedError()
        print("Doing some positive testing on my test data")

    def inference(self, options):
        """ Returns a list of predictions.
        A list of lists, number for each word in sentence."""
        data = options['dataset'].blind.data

        kiwi_config = kb.load_kiwi_config(options['quetch_test'])
        pred = kiwi.load_model(kiwi_config['load-model'])
        src = [' '.join(sent.src) for sent in data]
        tgt = [' '.join(sent.tgt) for sent in data]
        alg = [' '.join((f'{alg[0]}-{alg[1]}' for alg in sent.alignment)) for sent in data]
        examples = {kiwi.constants.SOURCE: src, kiwi.constants.TARGET: tgt, kiwi.constants.ALIGNMENTS: alg}

        print("Doing some inference on my blind data of size:", len(options['dataset'].blind.data))
        predictions = pred.predict(examples)
        return predictions['tags']
