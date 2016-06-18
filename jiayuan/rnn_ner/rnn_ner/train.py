from __future__ import absolute_import

import tensorflow as tf

import argparse
import time
import os
import cPickle

from rnn_ner.helper import LOGGER
from rnn_ner.ner_textloader import NerTextLoader
from rnn_ner.model import Model

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='data/ner',
                       help='data directory containing input.txt')
    parser.add_argument('--save_dir', type=str, default='output_data/ner/save',
                       help='directory to store checkpointed models')
    parser.add_argument('--rnn_size', type=int, default=128,
                       help='size of RNN hidden state')
    parser.add_argument('--num_layers', type=int, default=1,
                       help='number of layers in the RNN')
    parser.add_argument('--model', type=str, default='gru',
                       help='rnn, gru, or lstm')
    parser.add_argument('--batch_size', type=int, default=50,
                       help='minibatch size')
    parser.add_argument('--seq_length', type=int, default=50,
                       help='RNN sequence length')
    parser.add_argument('--num_epochs', type=int, default=50,
                       help='number of epochs')
    parser.add_argument('--save_every', type=int, default=50,
                       help='save frequency')
    parser.add_argument('--grad_clip', type=float, default=5.,
                       help='clip gradients at this value')
    parser.add_argument('--learning_rate', type=float, default=0.002,
                       help='learning rate')
    parser.add_argument('--decay_rate', type=float, default=0.97,
                       help='decay rate for rmsprop')
    args = parser.parse_args()
    train(args)

def train(args):
    LOGGER.info(args)
    data_loader = NerTextLoader(args.data_dir, args.batch_size, args.seq_length)
    args.vocab_size = data_loader.vocab_size
    args.y_vocab_size = len(data_loader.idx2classid)
    print('y_vocab_size = ' + str(args.y_vocab_size))

    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    with open(os.path.join(args.save_dir, 'config.pkl'), 'w') as f:
        cPickle.dump(args, f)
    with open(os.path.join(args.save_dir, 'chars_vocab.pkl'), 'w') as f:
        cPickle.dump((data_loader.chars, data_loader.vocab, data_loader.idx2classid, data_loader.classid2idx), f)

    model = Model(args)

    with tf.Session() as sess:
        tf.initialize_all_variables().run()
        saver = tf.train.Saver(tf.all_variables())
        for e in xrange(args.num_epochs):
            sess.run(tf.assign(model.lr, args.learning_rate * (args.decay_rate ** e)))
            data_loader.reset_batch_pointer()
            state = model.initial_state.eval()
            for b in xrange(data_loader.num_batches):
                start = time.time()
                x, y = data_loader.next_batch()
                feed = {model.input_data: x, model.targets: y, model.initial_state: state}
                train_loss, state, _ = sess.run([model.cost, model.final_state, model.train_op], feed)
                end = time.time()
                LOGGER.info("{}/{} (epoch {}), train_loss = {:.3f}, time/batch = {:.3f}" \
                    .format(e * data_loader.num_batches + b,
                            args.num_epochs * data_loader.num_batches,
                            e, train_loss, end - start))
                if (e * data_loader.num_batches + b) % args.save_every == 0:
                    checkpoint_path = os.path.join(args.save_dir, 'model.ckpt')
                    saver.save(sess, checkpoint_path, global_step = e * data_loader.num_batches + b)
                    LOGGER.info("model saved to {}".format(checkpoint_path))

if __name__ == '__main__':
    main()
