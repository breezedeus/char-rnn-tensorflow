#!/bin/bash

cur_dir=`dirname $0`
log_dir=${cur_dir}/../data/logs
pk_dir=/usr/local/lib/python2.7/site-packages

python ${pk_dir}/tensorflow/tensorboard/tensorboard.py --logdir=${log_dir}

# open http://localhost:6006/ with brower
