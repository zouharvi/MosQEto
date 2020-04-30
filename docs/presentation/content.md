
class: center, middle

# MosQEto 🦟
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
# MosQEto - Experiments 1

- We performed several experiments using OpenKiwi framework with QUETCH and NuQE
- Oriented on dataset preparation and transfer learning
- TODO (Ondra): notes on OpenKiwi config
- See [https://github.com/zouharvi/MosQEto/blob/master/docs/experiments.md](github.com/zouharvi/MosQEto/blob/master/docs/experiments.md) for more details, unexplained phenomena etc.

---
# MosQEto - Corpora

#### WMT19
- QE annotated (src, tgt, qe), IT domain
- 14k sentences, also contains post-edited sentences
- **in the New From Template dialog box , locate and select a template , and click New .**
- **wählen Sie im Dialogfeld "Neu aus Vorlage" eine Vorlage aus und klicken Sie auf "Neu."**
- **1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1** (all `OK`)

#### OPUS
- Only paralel corpora (src, tgt)
- Copora to match the IT domain: GNOME, KDE4, PHP, Ubuntu
- 300k sentences
- **The default plugin layout for the bottom panel**
- **Das vorgegebene Plugin-Layout der unteren Leiste**

---
# MosQEto - Experiments 2

#### Baseline 
- Only WMT19 data and run QUETCH for 30 epochs
- `F1_{MULTI}` is **28.8%**
- Disclaimer: We did not surpass this.

#### Small OPUS only with changes
- 14k sentences from OPUS
- Change every word to a different one (using zerogram) with probablity **12%** and set the corresponding tag to `BAD`
- `F1_{MULTI}` is **16%**

---
# MosQEto - Experiments 3

#### WMT19 + WMT19 post-edited
- Mark all post-edited WMT19 sentences as `OK`
- Mix with 14k of WMT19 baseline = 28k sentences
- `F1_{MULTI}` is **25.1%**

#### WMT19 + Small OPUS only with changes
- 7k OPUS 'changed' data
- Mixed with WMT19 baseline = 21k sentences
- `F1_{MULTI}` is **28.8%**

---
# MosQEto - Experiments 4

#### WMT19 + PE synth
- Take every sentence from WMT19 and add manual QE tags: `OK` iff a token appears in the post-edited version
- Every (src, tgt) has now two arrays of QE tags
- Mix with 14k of WMT19 baseline = 28k sentences
- `F1_{MULTI}` is **25.9%**

#### Transfer learning (failed)
- Train (NuQE and QUETCH) for 30 epochs on OPUS, then for 30 epochs on WMT19
- `F1_{MULTI}` is **0.07%**
- We tried adjusting learning rates, number of epochs and so on
- We tried "transfer" from WMT19 to WMT19 - the first training worked, after loading the model, F1 decreased
- Conclusion that the problem is with OpenKiwi framework
- See `experiments.md` for more details about a possible bug

<!--
- Opus data and QUETCH: **16%** at 29th epoch
- Mark all post-edited senteces as `OK`, QUETCH, WMT19: 25.1% `F1_{MULTI}`
- Add 7k randomly generated tags (with probability 0.12 change tag on OPUS data) to WMT19 data, 28.8% at epoch 30
- Add new, generated data to WMT19, such that a tag is `OK` if the word (case-insensitive) exists in post edited sentece, `BAD` otherwise. This yields 25.9% `F1_{MULTI}` at epoch 30
-->

---
# MosQEto - Future work

- Revise what went wrong with the transfer learning
- Come up with new ways of QE data synthesis
- - We hoped mostly for the post-edited data synthesis, but that failed
