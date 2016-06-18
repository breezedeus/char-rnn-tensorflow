# coding=utf8
#!/bin/bash
cur_dir=`cd $(dirname "$0"); pwd`

code_dir="rnn_ner"
data_dir="data/ner"
save_dir="output_data/ner/save"

model="lstm"
rnn_size=512
num_layers=1
batch_size=2

save_dir=${save_dir}_${rnn_size}
#python ${code_dir}/train.py --data_dir ${data_dir} --save_dir ${save_dir} --model ${model} \
#        --batch_size ${batch_size} --num_epochs 10 --rnn_size ${rnn_size} --num_layers ${num_layers}

python ${code_dir}/predict.py  --save_dir ${save_dir}