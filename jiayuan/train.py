# coding=utf8
import numpy as np
import tensorflow as tf

import argparse
import time
import os
import cPickle
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

from jy_textloader import JyTextLoader
from model import Model


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='data/jiayuan',
                        help='data directory containing input.txt')
    parser.add_argument('--save_dir', type=str, default='save/jiayuan',
                        help='directory to store checkpointed models')
    parser.add_argument('--rnn_size', type=int, default=128,
                        help='size of RNN hidden state')
    parser.add_argument('--num_layers', type=int, default=1,
                        help='number of layers in the RNN')
    parser.add_argument('--model', type=str, default='gru',
                        help='rnn, gru, or lstm')
    parser.add_argument('--batch_size', type=int, default=50,
                        help='minibatch size')
    parser.add_argument('--seq_length', type=int, default=20,
                        help='RNN sequence length')
    parser.add_argument('--num_epochs', type=int, default=23,
                        help='number of epochs')
    parser.add_argument('--save_every', type=int, default=1000,
                        help='save frequency')
    parser.add_argument('--grad_clip', type=float, default=5.,
                        help='clip gradients at this value')
    parser.add_argument('--learning_rate', type=float, default=0.001,
                        help='learning rate')
    parser.add_argument('--decay_rate', type=float, default=0.97,
                        help='decay rate for rmsprop')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    train(args)

def train(args):
    input_file = '/Users/king/Documents/Useful_Softwares/word2vec/trunk/data/jy_qa_cut.txt'
    class_threshold = 20
    char_threshold = 3
    test_ratio = 0.2
    use_ori = False
    data_loader = JyTextLoader(input_file=input_file, batch_size=args.batch_size,
                         max_seq_length=args.seq_length, class_threshold=class_threshold, char_threshold=char_threshold,
                         test_ratio=test_ratio, use_ori=use_ori)
    # data_loader = TextLoader(args.data_dir, args.batch_size, args.seq_length)
    args.vocab_size = data_loader.vocab_size

    # with open(os.path.join(args.save_dir, 'config.pkl'), 'w') as f:
    #     cPickle.dump(args, f)
    # with open(os.path.join(args.save_dir, 'chars_vocab.pkl'), 'w') as f:
    #     cPickle.dump((data_loader.chars, data_loader.vocab), f)

    model = Model(args)
    print(type(args))

    def print_matrix(mat):
        for i in range(len(mat)):
            print(mat[i])

    def print_sum_matrix(mat):
        results = []
        for i in range(len(mat)):
            print('i = %d ' % i, ([mat[i, i], sum(mat[i, ])-mat[i, i]]))

    def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        #tick_marks = np.arange(len(iris.target_names))
        #plt.xticks(tick_marks, iris.target_names, rotation=45)
        #plt.yticks(tick_marks, iris.target_names)
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')

    with tf.Session() as sess:
        merged = tf.merge_all_summaries()
        writer = tf.train.SummaryWriter('../data/logs', sess.graph_def)

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
                accuracy, train_loss, state, _ = sess.run([model.accuracy, model.cost, model.final_state, model.train_op], feed)
                end = time.time()
                print "{}/{} (epoch {}), train_loss = {:.3f}, train_accuracy = {:.3f}, time/batch = {:.3f}" \
                    .format(e * data_loader.num_batches + b,
                            args.num_epochs * data_loader.num_batches,
                            e, train_loss, accuracy, end - start)
                if (e * data_loader.num_batches + b) % args.save_every == 0:
                    checkpoint_path = os.path.join(args.save_dir, 'model.ckpt')
                    #saver.save(sess, checkpoint_path, global_step = e * data_loader.num_batches + b)
                    print "model saved to {}".format(checkpoint_path)

            # Evaluate valid accuracy
            xtest, ytest = data_loader.xtest, data_loader.ytest
            num_test_batches = xtest.shape[0] / args.batch_size
            accs = []
            losses = []
            preds = []
            for i in xrange(num_test_batches):
                xtest_batch = xtest[i*args.batch_size: (i+1)*args.batch_size]
                ytest_batch = ytest[i*args.batch_size: (i+1)*args.batch_size]
                feed = {model.input_data: xtest_batch, model.targets: ytest_batch, model.initial_state: state}
                if i == num_test_batches - 1:
                    summary_str, accuracy, test_loss, logits = sess.run([merged, model.accuracy, model.cost, model.logits], feed)
                    print(summary_str)
                    writer.add_summary(summary_str, e)
                else:
                    accuracy, test_loss, logits = sess.run([model.accuracy, model.cost, model.logits], feed)
                accs.append(accuracy)
                losses.append(test_loss)
                preds.extend(np.argmax(logits, 1).tolist())
            final_accuracy = np.mean(accs)
            final_loss = np.mean(losses)
            print "(epoch {}), test_loss = {:.3f}, test_accuracy = {:.3f}".format(e, final_loss, final_accuracy)
            cm = confusion_matrix(ytest[:num_test_batches*args.batch_size], preds)
            print_matrix(cm)
            print_sum_matrix(cm)

        def save_bad_cases(file_name, yreal, ypred, data_loader, xtest):
            with open(file_name, 'w') as f:
                yreal, ypred = np.array(yreal), np.array(ypred)
                assert yreal.size == ypred.size
                for i in range(yreal.size):
                    if yreal[i] != ypred[i]:
                        tmp_str = '%d\t%d\t' % (yreal[i], ypred[i])
                        tmp_str2 = data_loader.get_str_of_example_on_set(xtest, i)
                        if use_ori:
                            tmp_str2 = tmp_str2.encode('utf8')
                        f.write(tmp_str + tmp_str2 + '\n')

        data_loader.save_set_as_str('train_str.txt')
        save_bad_cases('bad_cases.txt', ytest[:num_test_batches*args.batch_size], preds, data_loader, xtest)
        plt.figure()
        cm = np.matrix(cm)
        cm[cm > 20] = 20
        cm = cm.tolist()
        plot_confusion_matrix(cm, cmap=plt.cm.gray)
        plt.show()


if __name__ == '__main__':
    main()
