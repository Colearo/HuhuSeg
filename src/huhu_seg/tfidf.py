#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from .segmentor import Segmentor

class IdfDict:

    def __init__(self) :
        self.path_name = os.path.join(os.path.dirname(__file__), 
                'lexicon', 'wiki_idf_986891.segd')
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
 
class TFIDF:

    idf = IdfDict()

    def __init__(self, passage) :
        self.passage = passage
        self.segmentor = Segmentor(passage)
        self.keywords = dict()
        self.freqs = dict()
        self.word_num = 0

    def extract_kw(self, top_n = 5, combine_mode = False) :
        tokens = self.segmentor.gen_key_tokens()
        for token in tokens :
            if token.word in TFIDF.idf.dict :
                self.word_num += 1
                try :
                    self.freqs[token.word] += 1
                except KeyError :
                    self.freqs[token.word] = 1
        for word, freq in iter(self.freqs.items()) :
            self.keywords[word] = float(freq/self.word_num) * TFIDF.idf.dict[word]
        top_list_candidate = sorted(iter(self.keywords.items()), key = lambda d:d[1], reverse = True)

        if top_n == -1 :
            top_n = len(top_list_candidate)

        if combine_mode is False :
            return top_list_candidate[0 : top_n]

        if top_n * 2 < len(top_list_candidate) :
            top_list_candidate = top_list_candidate[0 : top_n * 2]
        top_list = dict(top_list_candidate)
        word_couples = self.segmentor.gen_word_couples()
        for word_a, word_b in word_couples :
            if (word_a + word_b not in top_list.keys() and 
                    word_a in top_list.keys() and word_b in top_list.keys()) :
                top_list[word_a + word_b] = top_list[word_a] + top_list[word_b]
                top_list.pop(word_a)
                top_list.pop(word_b)
        top_list = sorted(iter(top_list.items()), key = lambda d:d[1], reverse = True)

        return top_list[0 : top_n]


