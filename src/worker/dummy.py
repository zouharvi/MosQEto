class Dummy:
    def train(self, options):
        print("Doing some heavy training with a train dataset of size:", len(options['dataset'].train.data))

    def test(self, options):
        sentence = options['dataset'].train.data[0]
        print(sentence)
        print("Doing some positive testing on my test data")

    def inference(self, options):
        print("Doing some inference on my blind data of size:", len(options['dataset'].blind.data))