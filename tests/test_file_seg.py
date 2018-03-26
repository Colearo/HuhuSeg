#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from huhu_seg.segmentor import Segmentor
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

global words_num
words_num = 0

def tokenize(text) :
    s = Segmentor(text)
    tokens = s.gen_tokens_parallel()
    return tokens

def seg2file(read, write) :
    global words_num
    with ProcessPoolExecutor(max_workers = 4) as executor :
        for tokens in executor.map(tokenize, (str(line) for line in iter(read.readlines()))) :
            string = ''.join([token.word + '  ' for token in tokens])
            words_num += len(tokens)
            write.write(string + '\n')

if __name__ == '__main__' :
    start = time.time()
    with open('./msr_test.utf8', 'r') as f :
        with open('./seg_results', 'w') as w :
            seg2file(f, w)
    duration = time.time() - start
    speed = words_num / duration
    print('Runs %.2f s' % duration)
    print('Speed %.2f words per second' % speed)

