#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy

def seqs2index(seqs, tag2index) :
    l = list()
    for o in seqs :
        l.append(tag2index[o])
    return l

def gen_tag2index(tags) :
    tag2index = dict()
    index2tag = dict()
    index = 0
    for tag in tags :
        tag2index[tag] = index
        index2tag[index] = tag
        index += 1
    return tag2index, index2tag

def map2vec(map, tag2index) :
    vec = numpy.zeros(len(map))
    for key in map :
        vec[tag2index[key]] = map[key]
    return vec

def map2matrix(map, tag2index_1, tag2index_2) :
    matrix = numpy.zeros((len(tag2index_1), len(tag2index_2)))
    for row in map :
        for col in map[row] :
            matrix[tag2index_1[row]][tag2index_2[col]] = map[row][col]
    return matrix

class HMM :

    def __init__(self, trans_matrix, emit_matrix, init_vec) :
        self.trans_matrix = trans_matrix
        self.emit_matrix = emit_matrix
        self.init_vec = init_vec

    def viterbi(self, seqs) :
        N = self.trans_matrix.shape[0]
        T = len(seqs)
        prev_states = numpy.zeros((T - 1, N), dtype = int)

        theta = numpy.zeros((N, T))
        theta[:, 0] = self.init_vec * self.emit_matrix[:, seqs[0]]

        for t in range(1, T) :
            for n in range(N) :
                probs = theta[:, t - 1] * self.trans_matrix[:, n] * self.emit_matrix[n, seqs[t]]
                prev_states[t - 1, n] = numpy.argmax(probs)
                theta[n, t] = numpy.max(probs)

        return theta, prev_states

    def state_path(self, observs2index) :
        theta, prev_states = self.viterbi(observs2index)
        last_state = numpy.argmax(theta[:, -1])
        path = list(self.iter_viterbi_path(prev_states, last_state))

        return theta[last_state, -1], list(reversed(path))

    def iter_viterbi_path(self, prev_states, last_state) :
        T = len(prev_states)
        yield(last_state)
        for t in range(T - 1, -1, -1) :
            yield(prev_states[t, last_state])
            last_state = prev_states[t, last_state]

