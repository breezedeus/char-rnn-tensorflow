# coding=utf8
from __future__ import absolute_import

import os
import collections
import cPickle
import numpy as np

from cn_char_rnn.helper import tokenize_cn

class CnTextLoader():
    _INPUT_FILE = 'input.txt'
    _VOCAB_FILE = 'vocab.pkl'
    _DATA_FILE = 'data.npy'

    def __init__(self, data_dir, batch_size, seq_length, use_ori=True):
        if not use_ori:
            tokenized_data_dir = os.path.join(data_dir, 'tokenized')
            input_file = os.path.join(data_dir, CnTextLoader._INPUT_FILE)
            output_file = os.path.join(tokenized_data_dir, CnTextLoader._INPUT_FILE)
            if not os.path.exists(output_file):
                tokenize_cn(input_file=input_file, output_file=output_file)
            data_dir = tokenized_data_dir
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.use_ori = use_ori

        input_file = os.path.join(data_dir, CnTextLoader._INPUT_FILE)
        vocab_file = os.path.join(data_dir, CnTextLoader._VOCAB_FILE)
        tensor_file = os.path.join(data_dir, CnTextLoader._DATA_FILE)

        if not (os.path.exists(vocab_file) and os.path.exists(tensor_file)):
            print "reading text file"
            self.preprocess(input_file, vocab_file, tensor_file)
        else:
            print "loading preprocessed files"
            self.load_preprocessed(vocab_file, tensor_file)
        self.create_batches()
        self.reset_batch_pointer()

    def preprocess(self, input_file, vocab_file, tensor_file):
        with open(input_file, "r") as f:
            data = f.read()
        if self.use_ori:
            data = data.decode('utf8')
            data = ' '.join(data).encode('utf8')
        else:
            data = data.replace('\n', ' \n ')
        data = data.split(' ')
        counter = collections.Counter(data)
        count_pairs = sorted(counter.items(), key=lambda x: -x[1])
        self.chars, _ = list(zip(*count_pairs))
        def save_vocab_txt(word_list):
            with open(vocab_file+'.txt', 'w') as f:
                for idx, word in enumerate(word_list):
                    f.write(str(idx) + '\t' + word + '\n')
        save_vocab_txt(self.chars)
        print(len(self.chars))
        self.vocab_size = len(self.chars)
        self.vocab = dict(zip(self.chars, range(len(self.chars))))
        with open(vocab_file, 'w') as f:
            cPickle.dump(self.chars, f)
        self.tensor = np.array(map(self.vocab.get, data))
        np.save(tensor_file, self.tensor)

    def load_preprocessed(self, vocab_file, tensor_file):
        with open(vocab_file) as f:
            self.chars = cPickle.load(f)
            #print(''.join([x.encode('utf-8') for x in self.chars]))
        self.vocab_size = len(self.chars)
        self.vocab = dict(zip(self.chars, range(len(self.chars))))
        self.tensor = np.load(tensor_file)
        self.num_batches = self.tensor.size / (self.batch_size * self.seq_length)

    def create_batches(self):
        self.num_batches = self.tensor.size / (self.batch_size * self.seq_length)
        self.tensor = self.tensor[:self.num_batches * self.batch_size * self.seq_length]
        xdata = self.tensor
        ydata = np.copy(self.tensor)
        ydata[:-1] = xdata[1:]
        ydata[-1] = xdata[0]
        self.x_batches = np.split(xdata.reshape(self.batch_size, -1), self.num_batches, 1)
        self.y_batches = np.split(ydata.reshape(self.batch_size, -1), self.num_batches, 1)


    def next_batch(self):
        x, y = self.x_batches[self.pointer], self.y_batches[self.pointer]
        self.pointer += 1
        return x, y

    def reset_batch_pointer(self):
        self.pointer = 0

