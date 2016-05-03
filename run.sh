# coding=utf8
#!/bin/bash
code_dir='jiayuan/cn_char_rnn'
data_dir='data/qiushibaike'

# tokenize raw jokes
#python ${code_dir}/tokenize_cn.py ${data_dir}/input.txt ${data_dir}/tokenized/input.txt

python ${code_dir}/train.py --data_dir ${data_dir}/tokenized --use_ori 1 --num_epochs 10

#python ${code_dir}/sample.py --prim '我们 就是'