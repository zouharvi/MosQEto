#!/usr/bin/env bash

# Downloads WMT18 and WMT19 datasets
# WMT18 to be implemented

for lang2 in de ru fr; do
    mkdir -p "data_raw/wmt19/en-$lang2"
done

mkdir -p "data_raw/wmt18"

function fetch_extract() {
    printf "Fetching "
    printf "$1" | sed -E "s|^.*/||g"
    printf " to $2\n"
    wget -q --show-progress -c "$1" -O - | tar -xz -C "$2"
}


# WMT19

# EN-RU
fetch_extract "https://deep-spin.github.io/docs/data/wmt2019_qe/task2_en-fr_test_gold.tar.gz" "data_raw/wmt19/en-fr";
fetch_extract "https://deep-spin.github.io/docs/data/wmt2019_qe/task2_en-fr_blindtest.tar.gz" "data_raw/wmt19/en-fr";
fetch_extract "https://deep-spin.github.io/docs/data/wmt2019_qe/task2_en-fr_traindev.tar.gz" "data_raw/wmt19/en-fr";
# EN-DE
fetch_extract "https://deep-spin.github.io/docs/data/wmt2019_qe/task1_en-de_test.tar.gz" "data_raw/wmt19/en-de";
fetch_extract "https://deep-spin.github.io/docs/data/wmt2019_qe/task1_en-de_blindtest.tar.gz" "data_raw/wmt19/en-de";
fetch_extract "https://deep-spin.github.io/docs/data/wmt2019_qe/task1_en-de_traindev.tar.gz" "data_raw/wmt19/en-de";
# EN-RU
fetch_extract "https://deep-spin.github.io/docs/data/wmt2019_qe/task1_en-ru_test.tar.gz" "data_raw/wmt19/en-ru";
fetch_extract "https://deep-spin.github.io/docs/data/wmt2019_qe/task1_en-ru_blindtest.tar.gz" "data_raw/wmt19/en-ru";
fetch_extract "https://deep-spin.github.io/docs/data/wmt2019_qe/task1_en-ru_traindev.tar.gz" "data_raw/wmt19/en-ru";