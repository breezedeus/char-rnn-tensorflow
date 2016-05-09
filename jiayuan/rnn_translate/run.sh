#!/bin/bash

cd `dirname $0`

train_data_dir=data
output_dir=output_data

size=128
num_layers=1
decode=True

python rnn_translate/translate.py --data_dir ${train_data_dir} --train_dir ${output_dir} \
                    --en_vocab_size 40000 --fr_vocab_size 40000 \
                    --decode ${decode} --size ${size} --num_layers ${num_layers}
