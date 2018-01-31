#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from huhu_seg import Segmentor

class IdfDict:

    def __init__(self) :
        self.path_name = os.path.join(os.path.dirname(__file__), os.pardir, 
                'lexicon', 'wiki_idf_986891')
        self.dict = dict()
        self.load()

    def load(self) :
        with open(self.path_name) as f :
            for line in f.readlines() :
                word, freq = line.split(' ')
                freq = float(freq.strip())
                self.dict[word] = freq
    
    def get(self, word) :
        item = self.dict.get(word)
        return item
 
class KeywordsEx:

    idf = IdfDict()

    def __init__(self, passage) :
        self.passage = passage
        self.segmentor = Segmentor(passage)
        self.keywords = dict()
        self.freqs = dict()
        self.word_num = 0

    def extract(self, top_n = 5) :
        tokens = self.segmentor.gen_key_tokens()
        for token in tokens :
            if token.word in KeywordsEx.idf.dict :
                self.word_num += 1
                try :
                    self.freqs[token.word] += 1
                except KeyError :
                    self.freqs[token.word] = 1
        for word, freq in iter(self.freqs.items()) :
            self.keywords[word] = float(freq/self.word_num) * KeywordsEx.idf.dict[word]
        top_list = sorted(iter(self.keywords.items()), key = lambda d:d[1], reverse = True)
        return top_list[0 : top_n]


