from __future__ import absolute_import
from __future__ import print_function

import tensorflow as tf

import argparse
import time
import os
import sys
import cPickle

from rnn_ner.model import Model
from rnn_ner.helper import cut_line

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=str, default='output_data/save',
                       help='model directory to store checkpointed models')
    parser.add_argument('--batch_size', type=int, default=50,
                        help='minibatch size')
    parser.add_argument('--seq_length', type=int, default=50,
                        help='RNN sequence length')
    args = parser.parse_args()
    predict(args)

def predict(args):
    with open(os.path.join(args.save_dir, 'config.pkl')) as f:
        saved_args = cPickle.load(f)
        #saved_args.batch_size = args.batch_size
        saved_args.batch_size = 1
        #saved_args.seq_length = args.seq_length
    with open(os.path.join(args.save_dir, 'chars_vocab.pkl')) as f:
        chars, vocab, idx2classid, classid2idx = cPickle.load(f)
    model = Model(saved_args, infer=False)

    print(args)

    def predict_sentence(sentence):
        return model.predict(sentence, saved_args.seq_length, sess, vocab, idx2classid)

    with tf.Session() as sess:
        tf.initialize_all_variables().run()
        saver = tf.train.Saver(tf.all_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            #print model.predict(sess, chars, vocab, args.n, args.prime)
            sys.stdout.write("> ")
            sys.stdout.flush()
            sentence = sys.stdin.readline()
            while sentence:
                print(predict_sentence(sentence))
                print("> ", end="")
                sys.stdout.flush()
                sentence = sys.stdin.readline()

if __name__ == '__main__':
    main()
