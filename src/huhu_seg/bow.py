#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
from .segmentor import Segmentor
from .tfidf import TFIDF

class Corpura:

    def __init__(self, corpura) :
        if not isinstance(corpura, list) :
            print('Para corpura should be a List([str,])')
            return
        self.dictionary = self.corpura2dict(corpura)

    def corpura2dict(self, corpura) :
        index_dict = dict()
        index = 0
        for corpus in corpura :
            segmentor =  Segmentor(corpus)
            tokens = segmentor.gen_key_tokens()
            for token in tokens :
                if token.word not in index_dict :
                    index_dict[token.word] = index
                    index += 1
        print('Find %d unique words' % len(index_dict))
        return index_dict

    def passage2bow(self, passage_tfidf) :
        words_list = passage_tfidf.extract_kw(top_n = -1,
                        combine_mode = False)
        vector = numpy.zeros(len(self.dictionary))
        for word, weight in words_list :
            if word in self.dictionary :
                vector[self.dictionary[word]] = weight
        return vector


class BOW:

    def __init__(self, passage, corpura) :
        self.passage = passage
        self.tfidf = TFIDF(passage)
        self.word_vector = corpura.passage2bow(self.tfidf)

    def similarity(self, other, threshold = 0.8) :
        v_a = self.word_vector
        v_b = other.word_vector
        sim = v_a.dot(v_b)/(numpy.linalg.norm(v_a) * 
                numpy.linalg.norm(v_b))
        print('Similarity is %f' % sim)

        if sim < threshold :
            return False
        else :
            return True


