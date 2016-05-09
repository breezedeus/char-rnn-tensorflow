# data set
<pre>
class_threshold = 20
#classes = 79
#train = 5487
#test = 1371
</pre>

# model=lstm, use_lastone=True, lr=0.001
<pre>
10897/10900 (epoch 99), train_loss = 1.730, train_accuracy = 0.500, time/batch = 0.282
10898/10900 (epoch 99), train_loss = 1.729, train_accuracy = 0.500, time/batch = 0.249
10899/10900 (epoch 99), train_loss = 1.529, train_accuracy = 0.580, time/batch = 0.252
(epoch 99), test_loss = 2.965, test_accuracy = 0.331
</pre>

# model=lstm, use_lastone=False, lr=0.001
<pre>
10898/10900 (epoch 99), train_loss = 0.489, train_accuracy = 0.920, time/batch = 0.394
10899/10900 (epoch 99), train_loss = 0.406, train_accuracy = 0.940, time/batch = 0.234
(epoch 99), test_loss = 2.706, test_accuracy = 0.474
</pre>

# model=gru, lr=0.001, rnn_size=128, seq_length=20, num_layers=2
<pre>
2395/10900 (epoch 21), train_loss = 0.705, train_accuracy = 0.880, time/batch = 0.235
2396/10900 (epoch 21), train_loss = 0.565, train_accuracy = 0.920, time/batch = 0.231
2397/10900 (epoch 21), train_loss = 0.626, train_accuracy = 0.900, time/batch = 0.240
(epoch 21), test_loss = 2.028, test_accuracy = 0.572
</pre>

# model=gru, lr=0.001, rnn_size=64
<pre>
10896/10900 (epoch 99), train_loss = 0.850, train_accuracy = 0.780, time/batch = 0.179
10897/10900 (epoch 99), train_loss = 0.607, train_accuracy = 0.860, time/batch = 0.175
10898/10900 (epoch 99), train_loss = 0.675, train_accuracy = 0.860, time/batch = 0.185
10899/10900 (epoch 99), train_loss = 0.553, train_accuracy = 0.880, time/batch = 0.181
(epoch 99), test_loss = 2.481, test_accuracy = 0.516
</pre>

# model=gru, lr=0.001, rnn_size=256
<pre>
2722/10900 (epoch 24), train_loss = 0.220, train_accuracy = 0.940, time/batch = 0.429
2723/10900 (epoch 24), train_loss = 0.162, train_accuracy = 0.980, time/batch = 0.401
2724/10900 (epoch 24), train_loss = 0.237, train_accuracy = 0.940, time/batch = 0.401
(epoch 24), test_loss = 2.149, test_accuracy = 0.579
</pre>

# model=gru, lr=0.001, rnn_size=128, seq_length=15
<pre>
2613/10900 (epoch 23), train_loss = 0.599, train_accuracy = 0.920, time/batch = 0.173
2614/10900 (epoch 23), train_loss = 0.581, train_accuracy = 0.880, time/batch = 0.268
2615/10900 (epoch 23), train_loss = 0.754, train_accuracy = 0.840, time/batch = 0.177
(epoch 23), test_loss = 2.078, test_accuracy = 0.553
</pre>

# model=gru, lr=0.001, rnn_size=128, seq_length=20, use_ori=True
<pre>
2177/10900 (epoch 19), train_loss = 0.834, train_accuracy = 0.800, time/batch = 0.216
2178/10900 (epoch 19), train_loss = 0.937, train_accuracy = 0.800, time/batch = 0.231
2179/10900 (epoch 19), train_loss = 0.732, train_accuracy = 0.800, time/batch = 0.224
(epoch 19), test_loss = 2.020, test_accuracy = 0.561
</pre>

# model=gru, lr=0.001, rnn_size=128, seq_length=30, use_ori=True
<pre>
5229/10900 (epoch 47), train_loss = 0.175, train_accuracy = 0.960, time/batch = 0.358
5230/10900 (epoch 47), train_loss = 0.317, train_accuracy = 0.920, time/batch = 0.375
5231/10900 (epoch 47), train_loss = 0.280, train_accuracy = 0.960, time/batch = 0.407
(epoch 47), test_loss = 2.348, test_accuracy = 0.567
</pre>

# ``[BEST]`` model=gru, lr=0.001, rnn_size=128, seq_length=20, num_layers=1, use_ori=False
<pre>
2286/10900 (epoch 20), train_loss = 0.285, train_accuracy = 0.980, time/batch = 0.134
2287/10900 (epoch 20), train_loss = 0.259, train_accuracy = 0.980, time/batch = 0.121
2288/10900 (epoch 20), train_loss = 0.457, train_accuracy = 0.880, time/batch = 0.124
(epoch 20), test_loss = 1.785, test_accuracy = 0.629
</pre>


# model=rnn, lr=0.003, rnn_size=128, seq_length=20, num_layers=1
<pre>
3921/10900 (epoch 35), train_loss = 0.747, train_accuracy = 0.820, time/batch = 0.056
3922/10900 (epoch 35), train_loss = 0.716, train_accuracy = 0.760, time/batch = 0.054
3923/10900 (epoch 35), train_loss = 0.741, train_accuracy = 0.780, time/batch = 0.057
(epoch 35), test_loss = 2.198, test_accuracy = 0.570
</pre>

# model=lstm, lr=0.001, rnn_size=128, seq_length=20, num_layers=1
<pre>
5556/10900 (epoch 50), train_loss = 0.686, train_accuracy = 0.820, time/batch = 0.117
5557/10900 (epoch 50), train_loss = 0.447, train_accuracy = 0.880, time/batch = 0.117
5558/10900 (epoch 50), train_loss = 0.597, train_accuracy = 0.880, time/batch = 0.116
(epoch 50), test_loss = 2.095, test_accuracy = 0.567
</pre>
