#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
import json
from .segmentor import Segmentor
from .tfidf import TFIDF

class Corpura:

    def __init__(self, corpura = None) :
        if corpura is not None :
            self.dictionary = self.corpura2dict(corpura)
        else :
            self.dictionary = dict()
    
    def load_dict(self, path) :
        with open(path, 'r') as r :
            self.dictionary = json.load(r)

    def save_dict(self, path) :
        with open(path, 'w') as f :
            json.dump(self.dictionary, f)

    def merge_dict(self, other) :
        if len(self.dictionary) == 0 :
            self.dictionary = other.dictionary
        index = len(self.dictionary)
        for key in other.dictionary :
            if key not in self.dictionary :
                self.dictionary[key] = index
                index += 1

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

    def corpura2average_bow(self, corpura) :
        length = sum(1 for corpus in corpura)
        if length == 0 :
            return None
        s = sum(BOW(corpus, self).word_vector for corpus in corpura)
        return s / length

    def passage2bow(self, passage_tfidf) :
        words_list = passage_tfidf.extract_kw(top_n = -1,
                        combine_mode = False)
        vector = numpy.zeros(len(self.dictionary))
        for word, weight in words_list :
            if word in self.dictionary :
                vector[self.dictionary[word]] = weight
        return vector


class BOW:

    def __init__(self, passage = None, corpura_handle = None, vec = None) :
        if passage is not None and corpura_handle is not None :
            self.passage = passage
            self.tfidf = TFIDF(passage)
            self.word_vector = corpura_handle.passage2bow(self.tfidf)
        else :
            self.word_vector = vec

    def similarity(self, other, threshold = 0.8) :
        v_a = self.word_vector
        v_b = other.word_vector
        sim = v_a.dot(v_b)/(numpy.linalg.norm(v_a) * 
                numpy.linalg.norm(v_b))
        print('Similarity is %f' % sim)

        if sim < threshold :
            return False, sim
        else :
            return True, sim

    def weight_similarity(self, self_b, other, weight = 0.6, 
            threshold = 0.8) :
        v_a = self.word_vector
        v_b = self_b.word_vector
        v_c = other.word_vector
        sim_ac = v_a.dot(v_c)/(numpy.linalg.norm(v_a) * 
                numpy.linalg.norm(v_c))
        sim_bc = v_b.dot(v_c)/(numpy.linalg.norm(v_b) * 
                numpy.linalg.norm(v_c))
        sim = sim_ac * (1 - weight) + sim_bc * weight
        print('Similarity is %f' % sim)

        if sim < threshold :
            return False, sim
        else :
            return True, sim


