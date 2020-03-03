# Experiment notes

### 03-03-2020 
`wmt19_pe_synth.yaml`, QUETCH at `5937ec3`

WMT19 training data + generated data from recomputed tags. For each target token, the unigram precision to post edited gold was considered (OK if exists in pe, otherwise BAD). We chose to make this case insensitive, but there is a switch in the config file. F1MULTI was `25.9%` at epoch 30. 


### 27-02-2020 base + part of generated (Vilda)
`wmt19_opus_random.yaml`, QUETCH at `477cd14`

WMT19 training data + 7k generated data from generator random. F1MULTI was `28.8%` at epoch 30 (slightly more at epoch 21).

### 27-02-2020 base + post edited expanded (Vilda)
`wmt19_pe_ok.yaml`

I ran QUETCH (`477cd14` parameters). The generator simply took all of the post-edited sentences and marked them as `OK`. F1MULTI was `25.1%` at epoch 30.

### 27-02-2020 generated only (Vilda)
`opus_random.yaml`, QUETCH at `477cd14`

Only 14k sentences of our data (only the change operation applied). F1MULTI was `16%` at epoch 29. This suggests, that the data _can be_ useful. Blind F1MULTI (based only on the distribution) would be `13.5%`. A proof follows:

Assume the system find the best probability `p` by which to assign `OK` and `1-p` by which to assign `BAD`. There are `u = 87.8%` `OK` labels in the WMT19 train data (an presumably in dev also).

```
TPOK = u*p,         TPBD = (1-u)*(1-p)
FPOK = (1-u)*p,     FPBD = u*(1-p)
FNOK = u*(1-p),     FNBD = (1-u)*p
TNOK = (1-u)*(1-p), TNBD = u*p
```

```
precOK = TPOK/(TPOK+FPOK) = u*p/(u*p+p-u*p) = u
recOK  = TPOK/(TPOK+FNOK) = u*p/(u*p+u-u*p) = p
precBD = TPBD/(TPBD+FPBD) = ...             = 1-u
recBD  = TPBD/(TPBD+FNBD) = ...             = 1-p
```

```
F1MULTI = F1OK*F1BD` `= (2*u*p)/(u+p) * (2*(1-u)*(1-p))/(2-u-p) = 1.756*p/(0.878+p) * (0.244*(1-p))/(1.122-p)
``` 

This function has a local extrema at `p=0.675` and `F1MULTI = 13.5%`.

#### Note 1
Obviously there's a huge discrepancy between the two types of data (our synthetic vs. WMT19), because the training F1MULTI was `69%`, which is a huge difference compared to F1MULTI on dev. Are we doing transfer learning?

#### Note 2
Unfortunately doubling the amount of data did not improve the score (but had training F1MULTI at `75%`). What does this mean?

### 27-02-2020 base only (Vilda)
`wmt19.yaml`, QUETCH at `477cd14`

Simply the WMT19 training data. F1MULTI was `28.8%` at epoch 30.
