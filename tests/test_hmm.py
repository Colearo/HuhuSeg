#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import huhu_seg.hmm as hmm

states = ('Healthy', 'Fever')
observs = ('normal', 'cold', 'dizzy')
init_probs = {'Healthy':0.6, 'Fever':0.4}
trans_probs = {
        'Healthy': {'Healthy': 0.7, 'Fever': 0.3},
        'Fever': {'Healthy': 0.4, 'Fever': 0.6},
        }
emit_probs = {
        'Healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
        'Fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6},
        }

states2index, index2states = hmm.gen_tag2index(states)
observs2index, index2observs = hmm.gen_tag2index(observs)

trans_matrix = hmm.map2matrix(trans_probs, states2index, states2index)
emit_matrix = hmm.map2matrix(emit_probs, states2index, observs2index)
init_vec = hmm.map2vec(init_probs, states2index)

obs_seq = ['normal', 'cold', 'dizzy', 'cold', 'dizzy']
obs_seq = hmm.seqs2index(obs_seq, observs2index)
h = hmm.HMM(trans_matrix, emit_matrix, init_vec)
theta, prev_states = h.viterbi(obs_seq)
print(" " * 7, " ".join(("%10s" % index2observs[i]) for i in obs_seq))
for s in range(len(states2index)) :
    print('%7s: ' % index2states[s] + ''.join('%10s' % ('%f' % v) for v in theta[s]))

prob, path = h.state_path(obs_seq)
for s in path :
    print(index2states[s])
print(prob)


