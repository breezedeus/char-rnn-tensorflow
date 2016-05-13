# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Makes helper libraries available in the translate package."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import jieba

def get_logger(name):
    import logging
    logger = logging.getLogger(name)
    myhandler = logging.StreamHandler()
    myformatter = logging.Formatter(fmt='%(asctime)s-%(levelname)s: %(message)s')
    myhandler.setFormatter(myformatter)
    logger.addHandler(myhandler)
    logger.setLevel('INFO')
    return logger

LOGGER = get_logger('rnn-translate')


def useori_tokenizer(line):
    data = line.strip().decode('utf8')
    data = ' '.join(data).encode('utf8')
    return data.split(' ')


def cut_line(line):
    token = jieba.cut(line.strip(), cut_all=False)
    token_str = " ".join(token).encode('utf-8')
    return token_str.split(" ")


def cut_tokenizer(line):
    return cut_line(line)


def tokenize_cn(input_file, output_file, sep=' '):
    out_dir = os.path.dirname(output_file)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(output_file, 'w') as out_f:
        with open(input_file, 'r') as in_f:
            for line in in_f:
                seg_list = cut_line(line.strip())
                out_f.write(sep.join(seg_list).encode('utf-8') + '\n')
