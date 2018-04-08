#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from huhu_seg.segmentor import Segmentor
from huhu_seg.textrank import TextRank
import huhu_seg.hmm as hmm

class Topic :
    
    def __init__(self) :
        self.topic_title = None

    def gen_topic(self, content, title) :
        title = title.strip().split(' ')
        title = title[0]
        s = Segmentor(title, hmm_config = True)
        title_tokens = s.gen_tokens()
        if len(title_tokens) <= 4 :
            keywords = TextRank(content, hmm_config = True).extract_kw()
            return title, keywords

        keywords = TextRank(content, hmm_config = True).extract_kw(20, False)
        keywords = dict(keywords)
        min_value = min(keywords.values())
        states = ('Branch', 'Leaf')
        trans_probs = {
                'Branch': {'Branch': 0.7, 'Leaf': 0.3}, 
                'Leaf': {'Leaf': 0.6, 'Branch': 0.4},
                    }
        init_probs = {'Branch': 0.45, 'Leaf': 0.55}
        emit_probs = dict()
        for state in states :
            emit_probs[state] = dict()
        seqs = list()
        for token in title_tokens :
            word = str(token.word)
            if word == '，' or word == ',' :
                break
            seqs.append(word)
            if word in keywords :
                emit_probs['Branch'][word] = keywords[word] 
                if token.tag.value == 'nr' or token.tag.value[0] == 'v':
                    emit_probs['Branch'][word] *= 1.5
            else :
                emit_probs['Leaf'][word] = min_value
                if token.tag.value == 'nr' or token.tag.value[0] == 'v':
                    emit_probs['Branch'][word] = 5 * min_value
                if len(token.word) == 1 :
                    emit_probs['Leaf'][word] *= 10

        observs = set(seqs)
        states2index, index2states = hmm.gen_tag2index(states)
        observs2index, index2observs = hmm.gen_tag2index(observs)
        trans_matrix = hmm.map2matrix(trans_probs, states2index, states2index)
        emit_matrix = hmm.map2matrix(emit_probs, states2index, observs2index)
        init_vec = hmm.map2vec(init_probs, states2index)
        obs_seqs = hmm.seqs2index(seqs, observs2index)
        h = hmm.HMM(trans_matrix, emit_matrix, init_vec)
        prob, path = h.state_path(obs_seqs)

        topic = ''
        symbol_flag = False
        for i in range(len(path)) :
            if symbol_flag is True and (seqs[i] == '"' or seqs[i] == '”' or seqs[i] == '》') :
                symbol_flag = False
            if seqs[i] not in topic and (index2states[path[i]] == 'Branch' or symbol_flag is True) :
                topic += seqs[i]
            if seqs[i] == '"' or seqs[i] == '“' or seqs[i] == '《':
                symbol_flag = True
        if len(topic) < 4 :
            topic = ''.join(seqs)

        keywords = TextRank(content, hmm_config = True).extract_kw()
        return topic, keywords


