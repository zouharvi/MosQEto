#!/usr/bin/env bash

pip3 install --user -r scripts/requirements.txt

echo "Installing fast_align"
git submodule update --init --recursive fast_align

rm -rf ./fast_align/build
mkdir -p ./fast_align/build
cd ./fast_align/build
cmake ..
make
cd ../../..