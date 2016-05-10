# coding=utf8
#!/bin/bash
cur_dir=`cd $(dirname "$0"); pwd`

code_dir="cn_char_rnn"
data_dir="data/qiushibaike"
save_dir="output_data/save"

use_ori=0
rnn_size=512
num_layers=1

python ${code_dir}/train.py --data_dir ${data_dir} --save_dir ${save_dir} \
        --use_ori ${use_ori} --num_epochs 10 --rnn_size ${rnn_size} --num_layers ${num_layers}

#python ${code_dir}/sample.py  --save_dir ${save_dir} --prim '我 是'