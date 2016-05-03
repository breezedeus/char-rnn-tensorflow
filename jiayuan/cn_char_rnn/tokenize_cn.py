# coding=utf8
__author__ = 'king'

import sys, os
import jieba


def tokenize_cn(input_file, output_file, sep=' '):
    out_dir = os.path.dirname(output_file)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(output_file, 'w') as out_f:
        with open(input_file, 'r') as in_f:
            for line in in_f:
                seg_list = jieba.cut(line.strip(), cut_all=False)
                out_f.write(sep.join(seg_list).encode('utf-8') + '\n')


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    tokenize_cn(input_file=input_file, output_file=output_file)
