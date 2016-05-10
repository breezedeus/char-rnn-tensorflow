# 使用说明
支持中文，基于字/词的RNN，代码逻辑来自于[char-rnn](https://github.com/karpathy/char-rnn)，
代码fork自[char-rnn-tensorflow](https://github.com/sherjilozair/char-rnn-tensorflow)，其结构类似下图：

![模型架构图](images/char_rnn.png)

代码可以应用于中文文本，以单字的模式，或者分词的模式。

运行方法见`run.sh`。

输入数据的格式为纯文本格式，如下：

<pre>
跟老公一起睡在床上看糗百。他说，我发的笑话过了。我拿他手机过来看，说才有一个顶。他瞪着我说，那还是老子自己顶的。
夏天来了女孩会买透明肩带 作为一个吃货我刚对着肩带流口水了 因为觉得像宽粉。。。
相亲中，女孩问：有纸吗？男孩问：大便吗？然后当然没有然后了
</pre>



在`cn_char_rnn/train.py`中，除了[char-rnn-tensorflow](https://github.com/sherjilozair/char-rnn-tensorflow)中的各种参数，
还有以下额外的参数可以进行设置：

<pre>
use_ori = 0  # 1：使用未分词的原始句子，每步表示一个汉字；0：系统会自己调用“jieba”进行分词，后续使用分词后的句子，每步表示一个词。
</pre>


