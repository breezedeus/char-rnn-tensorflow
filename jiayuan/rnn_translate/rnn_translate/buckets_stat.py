# coding=utf-8

import sys
import os
import numpy as np
import matplotlib.pyplot as plt


def get_seq_length_per_line(file_name):
    lengths = []
    with open(file_name, 'r') as f:
        for line in f:
            lengths.append(len(line.strip().split()))
    return lengths


def plot(x, y, buckets=[5, 10, 20, 40, 50]):
    mat = []
    for i in range(len(buckets)):
        mat.append([])
    for i, v in enumerate(x):
        for j, blen in enumerate(buckets):
            if v < blen:
                mat[j].append(y[i])
                break
    plt.figure(1)
    plt.boxplot(mat, vert=True, patch_artist=True)
    plt.xticks(range(1, len(buckets)+1), [str(x) for x in buckets])
    #plt.plot(x, y, 'o')
    #plt.xlim(0, 50)
    plt.ylim(0, 40)
    plt.show()


if __name__ == '__main__':
    data_dir = sys.argv[1]
    file_name_prefix = sys.argv[2]
    q_file_name = os.path.join(data_dir, file_name_prefix+'.q')
    a_file_name = os.path.join(data_dir, file_name_prefix+'.a')
    q_seq_lengths = get_seq_length_per_line(q_file_name)
    a_seq_lengths = get_seq_length_per_line(a_file_name)
    assert len(q_seq_lengths) == len(a_seq_lengths)

    plot(np.array(q_seq_lengths), np.array(a_seq_lengths))
