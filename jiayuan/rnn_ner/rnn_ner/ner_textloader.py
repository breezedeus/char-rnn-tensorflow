# coding=utf8

from __future__ import absolute_import

import os
import collections
import numpy as np
import random

#from utils import TextLoader
from helper import LOGGER


class NerTextLoader(object):
    __X_FILENAME = 'train_x.txt'
    __Y_FILENAME = 'train_y.txt'
    __UNKNOWN_CHAR = '<UNK>'
    __PAD = '<PAD>'
    __Y_PAD = 'O'
    __SEED = 23412421

    def __init__(self, data_dir, batch_size=50, max_seq_length=20, char_threshold=3, test_ratio=0.2):
        #assert char_threshold > 1
        self.batch_size = batch_size
        self.max_seq_length = max_seq_length
        self.char_threshold = char_threshold
        self.classid2idx = {}
        self.idx2classid = []
        x_file = os.path.join(data_dir, NerTextLoader.__X_FILENAME)
        y_file = os.path.join(data_dir, NerTextLoader.__Y_FILENAME)
        self._preprocess(x_file, y_file)
        self._split_train_and_test_set(test_ratio=test_ratio)
        self.create_batches()
        self.reset_batch_pointer()

    def _preprocess(self, x_file, y_file):
        x_data = self.__read_file(x_file)
        y_data = self.__read_file(y_file)

        def assert_data():
            assert len(x_data) == len(y_data)
            for i in xrange(len(x_data)):
                assert len(x_data[i]) == len(y_data[i])
        assert_data()

        self.xdata = self.__parse_x(x_data)
        self.ydata = self.__parse_y(y_data)
        print(self.xdata.size)
        assert self.xdata.shape == self.ydata.shape

    def __read_file(self, input_file):
        contents = []
        with open(input_file) as f:
            for line in f:
                contents.append(line.strip().split())
        LOGGER.info('Done! %d lines are read from file %s' % (len(contents), input_file))
        return contents

    def __parse_x(self, x_data):
        x_data = self.__pad_lines(x_data=x_data, pad=NerTextLoader.__PAD)

        char_threshold = self.char_threshold
        counter = collections.Counter(np.hstack(x_data))
        count_pairs = sorted([item for item in counter.items() if item[1] >= char_threshold], key=lambda x: -x[1])
        self.chars, _ = list(zip(*count_pairs))
        tmp_list = [NerTextLoader.__UNKNOWN_CHAR]
        tmp_list.extend(self.chars)
        self.chars = tmp_list
        self.vocab_size = len(self.chars)
        self.vocab = dict(zip(self.chars, range(len(self.chars))))
        tensor = []
        for line_list in x_data:
            tensor.append(map(lambda x: self.vocab.get(x, 0), line_list))
        tensor = np.array(tensor)

        print(self.vocab_size)
        print(tensor.shape)
        print(tensor.size)
        self.print_data(tensor, self.chars)
        return tensor

    def __parse_y(self, y_data):
        y_data = self.__pad_lines(x_data=y_data, pad=NerTextLoader.__Y_PAD)

        char_threshold = self.char_threshold
        counter = collections.Counter(np.hstack(y_data))
        count_pairs = sorted([item for item in counter.items() if item[1] >= char_threshold], key=lambda x: -x[1])
        self.idx2classid, _ = list(zip(*count_pairs))
        self.classid2idx = dict(zip(self.idx2classid, range(len(self.idx2classid))))
        print(self.idx2classid)

        tensor = []
        for line_list in y_data:
            tensor.append(map(lambda x: self.classid2idx.get(x, 0), line_list))
        tensor = np.array(tensor)
        self.print_data(tensor, self.idx2classid)
        return tensor

    def __pad_lines(self, x_data, pad):
        tmp_x = []
        for line in x_data:
            if len(line) >= self.max_seq_length:
                tmp_x.append(line[:self.max_seq_length])
            else:
                tmp_x.append(line + [pad] * (self.max_seq_length-len(line)))
        return tmp_x

    def get_str_of_example_on_set(self, tensor, code_list, i, sep=' '):
        if i >= len(tensor):
            return ''
        return sep.join(np.array(code_list)[tensor[i, ]])

    def print_data(self, tensor, code_list, top_n=3):
        for i in range(top_n):
            print(self.get_str_of_example_on_set(tensor, code_list, i))

    def __get_train_examples_with_classid(self, classid, top_n=3, sep=' || '):
        examples = self.xtrain[self.ytrain == classid]
        if top_n > examples.shape[0]:
            top_n = examples.shape[0]
        strs = []
        for i in range(top_n):
            strs.append(self.get_str_of_example_on_set(examples, i))
        tmp_str = sep.join(strs)
        if self.use_ori:
            tmp_str = tmp_str.encode('utf8')
        return tmp_str


    #def print_train_examples_with_classid(self, classid, top_n=3):
    #    print(self.__get_train_examples_with_classid(classid=classid, top_n=top_n))

    def _split_train_and_test_set(self, test_ratio=0.2, use_shuffle=False):
        random.seed(NerTextLoader.__SEED)
        total_size = self.xdata.shape[0]
        if use_shuffle:
            idx = range(total_size)
            random.shuffle(idx)
            self.xdata = self.xdata[idx]
            self.ydata = self.ydata[idx]
        test_size = int(total_size*test_ratio)
        test_idx = random.sample(xrange(total_size), test_size)
        train_idx = [i for i in xrange(total_size) if i not in test_idx]
        self.xtrain = self.xdata[train_idx]
        self.ytrain = self.ydata[train_idx]
        self.xtest = self.xdata[test_idx]
        self.ytest = self.ydata[test_idx]
        print('#train set: %d, #test set:%d' % (self.xtrain.shape[0], self.xtest.shape[0]))
        print('top-n train X:')
        self.print_data(self.xtrain, self.chars)
        print('top-n test X:')
        self.print_data(self.xtest, self.chars)

    def create_batches(self):
        self.num_batches = self.xtrain.shape[0] / self.batch_size
        self.num_test_batches = self.xtest.shape[0] / self.batch_size

    def next_batch(self):
        begin_idx = self.pointer * self.batch_size
        end_idx = begin_idx + self.batch_size
        x, y = self.xtrain[begin_idx:end_idx], self.ytrain[begin_idx:end_idx]
        #x = np.expand_dims(x, 0)
        #y = np.expand_dims(y, 0)
        self.pointer += 1
        return x, y

    def reset_batch_pointer(self):
        self.pointer = 0

    def save_set_as_str(self, file_name):
        top_n = 20
        with open(file_name, 'w') as f:
            num_classes = len(self.idx2classid)
            for classid in range(num_classes):
                tmp_str1 = '%d\t' % classid
                tmp_str2 = self.__get_train_examples_with_classid(classid=classid, top_n=top_n)
                f.write(tmp_str1 + tmp_str2 + '\n')


if __name__ == '__main__':
    input_file = '../data/ner'
    batch_size = 2
    max_seq_length = 20
    char_threshold = 1
    test_ratio = 0.2
    use_ori = False
    jy_tl = NerTextLoader(data_dir=input_file, batch_size=batch_size,
                         max_seq_length=max_seq_length, char_threshold=char_threshold,
                         test_ratio=test_ratio)
    print('--------------------------')
    for i in range(3):
        x, y = jy_tl.next_batch()
        jy_tl.print_data(x, jy_tl.chars, batch_size if batch_size <= 3 else 3)
        print('^^^^^^^^^^^^^^^^^^^^')

    #jy_tl.print_train_examples_with_classid(3, 5)