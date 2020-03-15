#!/usr/bin/env bash

qsub -cwd -j y -b y -l mem_free=10G -pe smp 8 ./src/main.py configs/quetch_all.yaml
