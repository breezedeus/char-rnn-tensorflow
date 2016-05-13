#!/bin/bash

cd `dirname $0`

train_data_dir=data/qiuai
output_dir=output_data

size=512
num_layers=1
decode=True
use_ori=True

output_dir="${output_dir}/save${size}_${num_layers}"
python rnn_translate/translate.py --data_dir ${train_data_dir} --train_dir ${output_dir} \
                    --en_vocab_size 40000 --fr_vocab_size 40000 \
                    --decode ${decode} --size ${size} --num_layers ${num_layers} -use_ori ${use_ori}
