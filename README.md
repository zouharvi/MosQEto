# MosQEto 🦟 /məˈski.toʊ/
A tool to experiment with machine translation quality estimation, possibly with results submittable to WMT 2020.

## Project specification
Our goal is to create a QE tool, which could be deployable to the [Ptakopět/Bergamot](https://ptakopet.vilda.net) project, but also on which we could experiment with QE models. We are interested mostly in word-level QE. If all goes well, we would like to participate in the WMT QE shared task. This project is split into several phases, with most important being the first phase and depending on the amount of work it takes, we would like to follow up also with phases two and three.

### Phase 1
Create a functioning framework with a simple trainable neural network QE model (simple encoder-decoder or replicate [QUETCH](https://www.aclweb.org/anthology/W15-3037.pdf)). This is to create end-to-end functioning QE system, which can be run on a server and tested in Ptakopět. It is not expected to perform well, but comparable to QUETCH. This is the hardest part and it is to test, that all of the pipeline is functioning properly.

### Phase 2
Implement more complex already existing models. This can be for example the NuQE architecture or some other (more research needed).

### Phase 3
Try any of the following ideas. They are expected to fail, but it can be interesting to think about how they fail and describe them in a paper.

- Penalize words, which are out of vocabulary for a given MT system (not applicable to the WMT competition)
- Since word alignment is provided, we can use it to either improve the attention (maybe too hard to implement) or find another way to make use of it (more research needed)
- 1. Drop provided post-edited data even in training
  2. Translate the source using our own MT model, so now we have src, tgt1, qe (for tgt1), tgt2
  3. The hypothesis is, that if tgt1 and tgt2 are close, then tgt1 is more correct, because tgt2 is correct ("ground truth")
  -  This can get really complex, for example because we will need alignment between tgt1 and tgt2. So we will need word alignment for the same language

We would also like to think about how can we train a QE system with limited amount of QE data, but almost infinite parallel texts. If we could synthetise new QE data, this would be very helpful. 

### Division of work
This is a semestral project by @zouharvi (Vilém Zouhar) and @pixelneo (Ondřej Měkota). Vilém is expected to create the framework and manage unsupervised ways of improving QE, while Ondřej is expected to implement the neural network model architectures. There's no clear mapping between the work needed to be done and phases, so the work is expected to happen concurrently.

## Technical details
The project is going to be implemented in Python 3, with the deep learning framework TBD (PyTorch or TensorFlow 2+).