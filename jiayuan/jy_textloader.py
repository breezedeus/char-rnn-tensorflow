# coding=utf8
__author__ = 'king'

import collections
import numpy as np
import random

from utils import TextLoader


class JyTextLoader(TextLoader):
    __UNKNOWN_CHAR = '<UNK>'
    __PAD = '<PAD>'
    __SEED = 23412421

    def __init__(self, input_file, batch_size=50, max_seq_length=20, class_threshold=20, char_threshold=3, test_ratio=0.2, use_ori=False):
        self.batch_size = batch_size
        self.max_seq_length = max_seq_length
        self.class_threshold = class_threshold
        self.char_threshold = char_threshold
        self.use_ori = use_ori
        self.classid2idx = {}
        self.idx2classid = []
        self._preprocess(input_file)
        self._split_train_and_test_set(test_ratio=test_ratio)
        self.create_batches()
        self.reset_batch_pointer()

    def _preprocess(self, input_file):
        contents = self.__read_file(input_file)
        contents = self.__choose_classes_by_threshold(self.class_threshold, contents)
        self.xdata = self.__parse_x(contents)
        self.ydata = self.__parse_y(contents)
        print(self.xdata.size)
        assert self.xdata.shape[0] == self.ydata.size


    def __read_file(self, input_file):
        contents = []
        with open(input_file, "r") as f:
            for line in f:
                class_id, ori_text, segmented_text = line.split('\t')
                contents.append((int(class_id.strip()), ori_text.strip(), segmented_text.strip()))
        print('Done! %d lines are read from file %s' % (len(contents), input_file))
        return contents

    def __choose_classes_by_threshold(self, threshold, contents):
        counter = collections.Counter([content[0] for content in contents])
        count_pairs = [item for item in counter.items() if item[1] >= threshold]
        count_pairs = sorted(count_pairs, key=lambda x: -x[1])
        class_ids, _ = list(zip(*count_pairs))
        self.classid2idx = dict(zip(class_ids, range(len(class_ids))))
        self.idx2classid = class_ids
        class_ids = set(class_ids)
        new_contents = [content for content in contents if content[0] in class_ids]
        print('Done! %d lines are left after using class_threshold %d, with #classes = %d' \
              % (len(new_contents), threshold, len(self.idx2classid)))
        return new_contents

    def __parse_y(self, contents):
        classid2idx = self.classid2idx
        y = map(classid2idx.get, [content[0] for content in contents])
        return np.array(y)

    def __parse_x(self, contents):
        char_threshold = self.char_threshold
        use_ori = self.use_ori
        new_x = []
        if use_ori:
            i = 1
            x = [content[i].decode('utf8') for content in contents]
            new_x = [[a for a in content] for content in x]
        else:
            i = 2
            x = [content[i] for content in contents]
            new_x = [content.split('^') for content in x]

        def pad_lines(new_x):
            tmp_x = []
            for content in new_x:
                if len(content) >= self.max_seq_length:
                    tmp_x.append(content[:self.max_seq_length])
                else:
                    tmp_x.append(content + [JyTextLoader.__PAD] * (self.max_seq_length-len(content)))
            return tmp_x
        new_x = pad_lines(new_x)

        counter = collections.Counter(np.hstack(new_x))
        count_pairs = sorted([item for item in counter.items() if item[1] >= char_threshold], key=lambda x: -x[1])
        self.chars, _ = list(zip(*count_pairs))
        if char_threshold > 1:
            tmp_list = [JyTextLoader.__UNKNOWN_CHAR]
            tmp_list.extend(self.chars)
            self.chars = tmp_list
        self.vocab_size = len(self.chars)
        self.vocab = dict(zip(self.chars, range(len(self.chars))))
        tensor = []
        for line_list in new_x:
            tensor.append(map(lambda x: self.vocab.get(x, 0), line_list))
        tensor = np.array(tensor)

        print(self.vocab_size)
        print(tensor.shape)
        print(tensor.size)
        self.print_data(tensor)
        return tensor

    def get_str_of_example_on_set(self, tensor, i, sep=' '):
        if self.use_ori:
            return sep.join(np.array(self.chars)[tensor[i, ]])
        else:
            #return sep.join(np.array(self.chars)[tensor[i, ]]).decode('utf8')
            return sep.join(np.array(self.chars)[tensor[i, ]])

    def print_data(self, tensor, top_n=3):
        for i in range(top_n):
            print(self.get_str_of_example_on_set(tensor, i))

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


    def print_train_examples_with_classid(self, classid, top_n=3):
        print(self.__get_train_examples_with_classid(classid=classid, top_n=top_n))

    def _split_train_and_test_set(self, test_ratio=0.2, use_shuffle=False):
        random.seed(JyTextLoader.__SEED)
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
        print('#train set: %d, #test set:%d' % (self.ytrain.size, self.ytest.size))
        print('top-n train X:')
        self.print_data(self.xtrain)
        print('top-n test X:')
        self.print_data(self.xtest)

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

    def save_set_as_str(self, file_name):
        top_n = 20
        with open(file_name, 'w') as f:
            num_classes = len(self.idx2classid)
            for classid in range(num_classes):
                tmp_str1 = '%d\t' % classid
                tmp_str2 = self.__get_train_examples_with_classid(classid=classid, top_n=top_n)
                f.write(tmp_str1 + tmp_str2 + '\n')


if __name__ == '__main__':
    input_file = '/Users/king/Documents/Useful_Softwares/word2vec/trunk/data/jy_qa_cut.txt'
    batch_size = 50
    max_seq_length = 20
    class_threshold = 20
    char_threshold = 3
    test_ratio = 0.2
    use_ori = False
    jy_tl = JyTextLoader(input_file=input_file, batch_size=batch_size,
                         max_seq_length=max_seq_length, class_threshold=class_threshold, char_threshold=char_threshold,
                         test_ratio=test_ratio, use_ori=use_ori)
    print('--------------------------')
    for i in range(3):
        x, y = jy_tl.next_batch()
        jy_tl.print_data(x, batch_size if batch_size <= 3 else 3)
        print('^^^^^^^^^^^^^^^^^^^^')

    jy_tl.print_train_examples_with_classid(3, 5)