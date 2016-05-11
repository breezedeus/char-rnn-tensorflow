from __future__ import absolute_import

import tensorflow as tf

import argparse
import time
import os
import cPickle

from cn_char_rnn.model import Model
from cn_char_rnn.helper import cut_line

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=str, default='output_data/save',
                       help='model directory to store checkpointed models')
    parser.add_argument('-n', type=int, default=500,
                       help='number of characters to sample')
    parser.add_argument('--prime', type=str, default=' ',
                       help='prime text')
    parser.add_argument('--use_ori', type=int, default=1,
                        help='whether use original cn sentences, 0 for segmented cn sentences')
    args = parser.parse_args()
    sample(args)

def sample(args):
    with open(os.path.join(args.save_dir, 'config.pkl')) as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(args.save_dir, 'chars_vocab.pkl')) as f:
        chars, vocab = cPickle.load(f)
    model = Model(saved_args, True)
    if len(args.prime) > 1:
        if args.use_ori:
            prime = args.prime.decode('utf8')
            args.prime = ' '.join(prime).encode('utf8')
        else:
            args.prime = ' '.join(cut_line(args.prime.strip()))
            args.prime = args.prime.encode('utf8')

    print(args)
    with tf.Session() as sess:
        tf.initialize_all_variables().run()
        saver = tf.train.Saver(tf.all_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            print model.sample(sess, chars, vocab, args.n, args.prime)

if __name__ == '__main__':
    main()
