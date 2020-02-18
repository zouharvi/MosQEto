#!/usr/bin/env python3

import argparse
from dataset import Dataset

# TODO do config parsing

if __name__ == '__main__':
    dataEnDe = Dataset('en-de', 'wmt19')
    print('WMT19 en-de train:', len(dataEnDe.train.data))
    print('WMT19 en-de dev:', len(dataEnDe.dev.data))
    print('WMT19 en-de test:', len(dataEnDe.test.data))
    print('WMT19 en-de blindtest:', len(dataEnDe.blind.data))