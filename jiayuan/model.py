import tensorflow as tf
from tensorflow.models.rnn import rnn_cell
from tensorflow.models.rnn import seq2seq

import numpy as np

class Model():
    def __init__(self, args, infer=False):
        self.args = args
        # if infer:
        #     args.batch_size = 1
        #     args.seq_length = 1

        if args.model == 'rnn':
            cell_fn = rnn_cell.BasicRNNCell
        elif args.model == 'gru':
            cell_fn = rnn_cell.GRUCell
        elif args.model == 'lstm':
            cell_fn = rnn_cell.BasicLSTMCell
        else:
            raise Exception("model type not supported: {}".format(args.model))

        cell = cell_fn(args.rnn_size)

        self.cell = cell = rnn_cell.MultiRNNCell([cell] * args.num_layers)

        #self.seq_length = tf.placeholder(tf.int32)
        #args.seq_length = self.seq_length
        self.input_data = tf.placeholder(tf.int32, [args.batch_size, args.seq_length])
        self.targets = tf.placeholder(tf.int32, [args.batch_size])
        self.initial_state = cell.zero_state(args.batch_size, tf.float32)

        with tf.variable_scope('rnnlm'):
            softmax_w = tf.get_variable("softmax_w", [args.rnn_size, args.vocab_size])
            softmax_b = tf.get_variable("softmax_b", [args.vocab_size])
            with tf.device("/cpu:0"):
                embedding = tf.get_variable("embedding", [args.vocab_size, args.rnn_size])
                inputs = tf.split(1, args.seq_length, tf.nn.embedding_lookup(embedding, self.input_data))
                # len(inputs)==args.seq_length, shape(inputs[0])==(args.batch_size, args.rnn_size)
                inputs = [tf.squeeze(input_, [1]) for input_ in inputs]

        def loop(prev, _):
            return None  # TODO
            prev = tf.nn.xw_plus_b(prev, softmax_w, softmax_b)
            prev_symbol = tf.stop_gradient(tf.argmax(prev, 1))
            return tf.nn.embedding_lookup(embedding, prev_symbol)

        # len(outputs)==args.seq_length, shape(outputs[0])==(args.batch_size, args.rnn_size)
        outputs, states = seq2seq.rnn_decoder(inputs, self.initial_state, cell, loop_function=loop if infer else None, scope='rnnlm')
        # # shape(output) = (batch_size*seq_length, rnn_size)
        # output = tf.reshape(tf.concat(1, outputs), [-1, args.rnn_size])
        def handle_outputs(use_lastone=True):
            """ Shape of return is [batch_size, rnn_size].
            """
            if use_lastone:
                return outputs[-1]
            output = tf.math_ops.add_n(outputs)
            output = tf.math_ops.div(output, len(outputs))
            return output
        output = handle_outputs(use_lastone=False)
        # shape(logits) = (batch_size, vocab_size)
        self.logits = tf.nn.xw_plus_b(output, softmax_w, softmax_b)
        self.probs = tf.nn.softmax(self.logits)
        loss = seq2seq.sequence_loss_by_example([self.logits],
                [tf.reshape(self.targets, [-1])],
                [tf.ones([args.batch_size])],
                args.vocab_size)
        self.cost = tf.reduce_sum(loss) / args.batch_size
        _ = tf.scalar_summary('cost', self.cost)

        # Evaluate accuracy
        correct_pred = tf.equal(tf.cast(tf.argmax(self.logits, 1), tf.int32), tf.reshape(self.targets, [-1]))
        self.accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
        _ = tf.scalar_summary('accuracy', self.accuracy)

        self.final_state = states[-1]
        self.lr = tf.Variable(0.0, trainable=False)
        tvars = tf.trainable_variables()
        grads, _ = tf.clip_by_global_norm(tf.gradients(self.cost, tvars),
                args.grad_clip)
        optimizer = tf.train.AdamOptimizer(self.lr)
        self.train_op = optimizer.apply_gradients(zip(grads, tvars))

    # def sample(self, sess, chars, vocab, num=200, prime='The '):
    #     state = self.cell.zero_state(1, tf.float32).eval()
    #     for char in prime[:-1]:
    #         x = np.zeros((1, 1))
    #         x[0, 0] = vocab[char]
    #         feed = {self.input_data: x, self.initial_state:state}
    #         [state] = sess.run([self.final_state], feed)
    #
    #     def weighted_pick(weights):
    #         t = np.cumsum(weights)
    #         s = np.sum(weights)
    #         return(int(np.searchsorted(t, np.random.rand(1)*s)))
    #
    #     ret = prime
    #     char = prime[-1]
    #     for n in xrange(num):
    #         x = np.zeros((1, 1))
    #         x[0, 0] = vocab[char]
    #         feed = {self.input_data: x, self.initial_state:state}
    #         [probs, state] = sess.run([self.probs, self.final_state], feed)
    #         p = probs[0]
    #         # sample = int(np.random.choice(len(p), p=p))
    #         sample = weighted_pick(p)
    #         pred = chars[sample]
    #         ret += pred
    #         char = pred
    #     return ret


