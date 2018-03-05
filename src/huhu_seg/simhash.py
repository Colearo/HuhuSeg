#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import numpy
from .tfidf import TFIDF

class SimHash:

    def __init__(self, passage, code_bit = 64) :
        self.passage = passage
        self.code_bit = code_bit
        self.tfidf = TFIDF(self.passage)
        self.tokens = self.tfidf.extract_kw(top_n = 200, combine_mode = False)
        self.simhash = self.sim_hash(self.tokens)

    def __str__(self) :
        return self.simhash

    def string_hash(self, string, code_bit) :
        if string is '' :
            return 0
        hash_code = ord(string[0]) << 7
        magic = 100003
        mask = (1 << code_bit) - 1
        for char in string :
            hash_code = ((hash_code * magic) ^ ord(char)) & mask
        hash_code ^= len(string)
        if hash_code == -1 :
            hash_code = -2
        hash_code = bin(hash_code).replace('0b', '').zfill(code_bit)[-code_bit:]

        return str(hash_code)

    def sim_hash(self, kw) :
        sum_matrix = list()
        for word, weight in kw :
            weights_matrix = list()
            hash_code = self.string_hash(word, self.code_bit)
            for bit in hash_code :
                if bit is '1' :
                    weights_matrix.append(weight)
                else :
                    weights_matrix.append(-weight)
            sum_matrix.append(weights_matrix)

        sum_matrix = numpy.sum(numpy.array(sum_matrix), axis = 0)
        simhash = ''
        for item in sum_matrix :
            if item <= 0 :
                simhash += '0'
            else :
                simhash += '1'
        print(simhash)
        return simhash

    def hamming_distance(self, hash_a, hash_b) :
        tot = 0 
        xor = hash_a ^ hash_b
        while xor != 0 :
            tot += 1
            xor &= xor - 1
        return tot

    def similarity(self, other, threshold = 0.8) :
        hash_a = int('0b' + self.simhash, 2)
        hash_b = int('0b' + other.simhash, 2)

        dis = self.hamming_distance(hash_a, hash_b)
        sim = float(self.code_bit - dis) / self.code_bit 
        print('Hamming Distance is ', dis)
        print('Similarity is %f' % sim)
        if sim < threshold :
            return False
        else :
            return True

