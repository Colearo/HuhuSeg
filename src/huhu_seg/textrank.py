#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
from .segmentor import Segmentor

class TextRank :

    def __init__(self, passage, window_width = 3, weight = 0.8) :
        self.passage = passage
        self.window_width = window_width
        self.segmentor = Segmentor(passage)
        self.co_groups = dict()
        self.weight = weight

    def gen_co_groups(self) :
        tokens = self.segmentor.gen_key_tokens(pos = False)
        index = 0
        for token in tokens :
            next_vectors = list()
            for i in range(1, self.window_width + 1) :
                if index - i >= 0 :
                    next_vectors.append(tokens[index - i])
                if index + i < len(tokens) :
                    next_vectors.append(tokens[index + i])
            try :
                vectors = self.co_groups[token.word] 
            except KeyError :
                self.co_groups[token.word] = next_vectors
            else :
                for v in next_vectors :
                    if v not in vectors :
                        self.co_groups[token.word].append(v)
            index += 1

    def gen_gram(self) :
        self.trans_matrix = numpy.zeros((len(self.co_groups), len(self.co_groups)), 
            dtype = numpy.float64)
        index_dict = dict()
        index = 0
        for key in iter(self.co_groups.keys()) :
            index_dict[key] = index
            index += 1
        init_rank = float(1.0/len(self.co_groups))
        for word, vectors in iter(self.co_groups.items()) :
            out_vec = float(len(vectors))
            for v in vectors :
                self.trans_matrix[index_dict[v.word], 
                        index_dict[word]] = float(1.0/out_vec) * self.weight

        self.vec_matrix = numpy.zeros((len(self.co_groups), 1), 
            dtype = numpy.float64)
        for i in range(len(self.co_groups)) :
            self.vec_matrix[i, 0] = init_rank

        self.teleport_matrix = numpy.zeros((len(self.co_groups), 1), 
            dtype = numpy.float64)
        for i in range(len(self.co_groups)) :
            self.teleport_matrix[i, 0] = 1 - self.weight

        self.thr_matrix = numpy.zeros((len(self.co_groups), 1), 
            dtype = numpy.float64)
        for i in range(len(self.co_groups)) :
            self.thr_matrix[i, 0] = 0.0001

    def power_iteration(self) :
        self.gen_co_groups()
        self.gen_gram()
        max_iter = 1000
        times = 0
        while times < max_iter :
            last_vec = self.vec_matrix
            self.vec_matrix = numpy.dot(self.trans_matrix, self.vec_matrix) + self.teleport_matrix
            diff = abs(last_vec - self.vec_matrix)
            if (diff < self.thr_matrix).any() :
                break
            times += 1

    def extract_kw(self, top_n = 5) :
        self.power_iteration()
        self.top_n = dict()
        index = 0
        for key in iter(self.co_groups.keys()) :
            self.top_n[key] = self.vec_matrix[index, 0]
            index += 1
        top_list_candidate = sorted(iter(self.top_n.items()), key = lambda d:d[1], reverse = True)
        top_list_candidate = top_list_candidate[0 : top_n * 2]
        top_list = dict(top_list_candidate)
        word_couples = self.segmentor.gen_word_couples()
        for word_a, word_b in word_couples :
            if (word_a + word_b not in top_list.keys() and 
                    word_a in top_list.keys() and word_b in top_list.keys()) :
                top_list[word_a + word_b] = top_list[word_a] + top_list[word_b]
                try :
                    top_list.pop(word_a)
                    top_list.pop(word_b)
                except :
                    pass

        top_list = sorted(iter(top_list.items()), key = lambda d:d[1], reverse = True)
            
        return top_list[0 : top_n]
    
    def print_co_groups(self) :
        for key, value in iter(self.co_groups.items()) :
            print('%s :' % key, end = ' ')
            for i in value :
                print(i.word, end = ' ')
            print(' ')

