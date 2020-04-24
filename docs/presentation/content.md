
class: center, middle

# MosQEto
### Vilém Zouhar, Ondřej Měkota
### 2020, MFF

---
# Quality Estimation

- MT evaluation: (source?, translation, reference) -> score
- QE: (source, translation) -> score
- Part of WMT since 2012
- Levels:
- - {document,paragraph}-level: a score, or list spans containing errors
- - sentence-level: HTER (edit distance metrics)
- - word-level: probabilities for every token and gap token (in WMT only `OK/BAD`)
- {document,paragraph,sentence}-level can be infered from word-level

---
# Quality Estimation - Example

<img src="presentation/word_qe_example_1.png" style="width: 98%" />
Quality estimation tags for tokens and gaps on German sentence translated from English (from WMT19 quality estimation shared task)


---
# Quality Estimation - Evaluation

- Given list of (predicted, gold), we want to get some score of success
- (Root) Mean Square Error, Mean Square Error, {Spearman,Pearson}'s correlation
- - Easy to compute
- - Data is very imbalanced (contains very few `BAD` tags, most `OK`)
- - Can be used for {paragraph,sentence}-level, where we have single numbers: HTER
- F-score
- - Solves data imbalance
- - Note that `F_{BAD} != F_{OK}`
- - `F_{MULTI}` is usually used `F_{MULTI} = F_{BAD} * F_{OK}`
- State of the art results:
- - For SMT systems:
- - - EN->DE: `0.6246`, gaps: `0.4999`
- - For NMT systems:
- - - EN->DE: `0.4752`, gaps: `0.1193`

---
# Quality Estimation Approaches
- From MT systems (self-reported confidence): not used by models submitted to WMT
- Supervised:
- - Train, dev, test data supplied (source, target, per-word scores)
- - QuEst++ (Specia et. al. 2015): First baseline
- - - Feature extraction (matching alignment, POS of source and target, n-gram frequencies, ...)
- - - Classical ML algorithm (Cross-Validated Lasso or Conditional Random Fields)
- - DeepQuest (Ive et. al., 2018): First neural baseline
- - - biRNN - one of the simplest NN architectures
- - - Predictor-Estimator - utilizes also (source, target) data to learn contexts
- - OpenKiwi (Kepler et. al., 2019): Public state of the art
- - - Reimplements QUETCH (single layer feature combination), NuQE (similar to QUETCH), biRNN, PredEst
- Our observation (from our Ptakopět experiments):
- - Especially out-of-domain performance is unsuable in end applications

---
# MosQEto - Infrastructure

- Most of dev time spent here (50-70%)
- We suspect turing completeness
- An experiment (of any kind: training, testing, data creatin) can be easily defined using a single YAML file
- Oriented for data manipulation, but can be used for anything if relevant `Worker` classes are implemented
- We unintentionally created a system for robust experiment replication
- Datesets are loaded automatically
- `fast_align` is also part of the whole system
- Remaining time spend on experiments

---
# MosQEto - Infrastrucutre - Config example

<!-- class: split-40 -->

.column[
<div style='margin-top: -30px;'></div>
```
dataset_load:
  - "opus/tech/en-de"
  - "wmt19/en-de"

dataset_save: 
  - "data_all/"

method:
  - Loader:rmdir:data_tmp
  
  - Loader:load:noalign
  - DataUtils:info
  - Generator:synthetize_random
  - DataUtils:head:7000
  - DataUtils:info

  - Loader:load
  - DataUtils:info

  - Generator:mix
  - Loader:save

generator:
  change_prob: 0.12
```
]
.column[
  
__Can you guess what this script does?__


<div style='margin-top: 50px;'></div>

- `Loader:load` pops one item of the `dataset_load` stack
- `"opus/tech/en-de"` is just a parallel corpus

<div style='margin-top: 50px;'></div>


Note on `__DataUtils:info__`:
- The most important command we implemented
- Lets us examine the distribution of current data

```
Sentences: 20442
Target: |   328008|    45511| 87.82% OK|
Gaps:   |   388140|     5821| 98.52% OK|
All:    |   716148|    51332| 93.31% OK|
```
]

---
# MosQEto - Experiments

- We performed several experiments using OpenKiwi framework with QUETCH and NuQE
- TODO (ondra): notes on openkiwi config

### Baseline 
- WMT19 data and run QUETCH for 30 epochs

- `F1_{MULTI}` is **28.8%** at 30th epoch
- Opus data and QUETCH: **16%** at 29th epoch

---
# MosQEto - Experiments cont.

- Mark all post-edited senteces as `OK`, QUETCH, WMT19: 25.1% `F1_{MULTI}`
- Add 7k randomly generated tags (with probability 0.12 change tag on OPUS data) to WMT19 data, 28.8% at epoch 30.
- Add new, generated data to WMT19, such that a tag is `OK` if the word (case-insensitive) exists in post edited sentece, `BAD` otherwise. This yields 25.9% `F1_{MULTI}` at epoch 30.
- Transfer learning (failed): train (NuQE and QUETCH) for 30 epochs on OPUS, then train for another 30 epochs on WMT19. Final F1 score: 0.07%
We have tried adjusting learning rates, number of epochs and so on.i Then we tried "transfer" from WMT19 to WMT19 - the first training worked, after loading the model, F1 decreased. So we arrived at a conclusion that the problem is with OpenKiwi framework.

