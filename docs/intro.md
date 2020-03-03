# Config files
- directory `data`: configurations for creating data
    * `wmt19.yaml`: original data
    * `wmt19_pe_ok.yaml`: expands post edited as OK
    * `wmt19_opus_random.yaml`: adds 7k opus generated samples to wmt
    * `opus_random.yaml`: takes only opus
    * `wmt19_pe_synth.yaml`: original data + target according to unigram precision to post edited
- directory `openkiwi`: configurations for `openkiwi` tool

# Running the experiments
One should always run a specific data creation experiment (from the `config/data` folder) and then a specific training model. All `config/data` processes save the data into `data_all`, which should be referenced by the QE models. Do not use `data_raw` directly.

To run a process: `./src/main.py config/PROCESS.yaml`