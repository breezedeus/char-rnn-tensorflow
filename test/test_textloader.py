# coding=utf8
__author__ = 'king'

import unittest
import tensorflow as tf
from tensorflow.models.rnn import rnn_cell, rnn
from tensorflow.models.rnn import seq2seq

from utils import TextLoader


class TestTextLoader(unittest.TestCase):
    def test_create_batches(self):
        return
        data_dir = '../data/tinyshakespeare'
        data_loader = TextLoader(data_dir, batch_size=3, seq_length=4)

        idx2word = data_loader.chars
        def _get_str(data=data_loader.tensor[:100]):
            return ''.join([idx2word[x] for x in data])

        def print_str(data=data_loader.tensor[:100]):
            print('-----------START-----------------')
            print(''.join([idx2word[x] for x in data]))
            print('------------END--------------------')
        print_str()

        xdata = data_loader.tensor
        xdata.reshape(data_loader.batch_size, -1)
        for i in range(5):
            tmp_x_data = data_loader.x_batches[i]
            tmp_y_data = data_loader.y_batches[i]
            tmp_x_strs = []
            tmp_y_strs = []
            for j in range(tmp_x_data.shape[0]):
                tmp_x_strs.append(_get_str(tmp_x_data[j]))
                tmp_y_strs.append(_get_str(tmp_y_data[j]))
            print('-----------START-----------------')
            print(tmp_x_strs)
            print(tmp_y_strs)
            print('------------END--------------------')

    def test_model(self):
        data_dir = '../data/tinyshakespeare'
        data_loader = TextLoader(data_dir, batch_size=3, seq_length=4)
        data = data_loader.x_batches[0]

        batch_size = 3
        seq_length = 4
        rnn_size = 5
        vocab_size = data_loader.vocab_size
        print(vocab_size)

        cell_fn = rnn_cell.BasicRNNCell
        cell = cell_fn(rnn_size)

        initial_state = cell.zero_state(batch_size, tf.float32)
        input_data = tf.placeholder(tf.int32, [batch_size, seq_length])
        output_data = tf.abs(input_data)
        with tf.variable_scope('rnnlm'):
            softmax_w = tf.get_variable("softmax_w", [rnn_size, vocab_size])
            softmax_b = tf.get_variable("softmax_b", [vocab_size])
            with tf.device("/cpu:0"):
                embedding = tf.get_variable("embedding", [vocab_size, rnn_size])
                #inputs = tf.nn.embedding_lookup(embedding, input_data)
                inputs = tf.split(1, seq_length, tf.nn.embedding_lookup(embedding, input_data))
                inputs = [tf.squeeze(input_, [1]) for input_ in inputs]
                inputs_shape = tf.shape(inputs[0])
        #outputs, states = seq2seq.rnn_decoder(inputs, initial_state, cell, None, scope='rnnlm')

        with tf.Session() as sess:
            tf.initialize_all_variables().run()
            result = sess.run([inputs[0], inputs_shape], {input_data: data})
            print(result)

    def test_tf(self):
        import numpy as np
        seq_length = tf.placeholder(tf.int32)
        batch_size = 3
        input_data = tf.placeholder(tf.int32, [batch_size, None])
        output = tf.reduce_sum(input_data)
        with tf.Session() as sess:
            tf.initialize_all_variables().run()
            result = sess.run([output], {seq_length: 2, input_data: np.reshape(range(9), [batch_size, -1])})
            print(result)


    def test_tf2(self):
        import numpy as np
        input = tf.placeholder(tf.float32, [2, 4])
        outputs = [input] * 3
        output = tf.math_ops.add_n(outputs)
        #output = tf.math_ops.div(output, len(outputs))
        with tf.Session() as sess:
            tf.initialize_all_variables().run()
            result = sess.run([output], {input: np.reshape(range(8), [2, 4])})
            print(result)

if __name__ == '__main__':
    unittest.main()
