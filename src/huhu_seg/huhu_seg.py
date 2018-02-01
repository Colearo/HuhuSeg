#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import math
from enum import Enum

class WordTag(Enum):
    ag = 'ag'
    a = 'a'
    ad = 'ad'
    an = 'an'
    bg = 'bg'
    b = 'b'
    c = 'c'
    dg = 'dg'
    d = 'd'
    df = 'df'
    e = 'e'
    eng = 'eng'
    f = 'f'
    g = 'g'
    h = 'h'
    i = 'i'
    j = 'j'
    k = 'k'
    l = 'l'
    mg = 'mg'
    m = 'm'
    mq = 'mq'
    ng = 'ng'
    n = 'n'
    nr = 'nr'
    nrfg = 'nrfg'
    nrt = 'nrt'
    ns = 'ns'
    nt = 'nt'
    nx = 'nx'
    nz = 'nz'
    o = 'o'
    p = 'p'
    qg = 'qg'
    q = 'q'
    rg = 'rg'
    r = 'r'
    rr = 'rr'
    rz = 'rz'
    s = 's'
    tg = 'tg'
    t = 't'
    u = 'u'
    ud = 'ud'
    ug = 'ug'
    uj = 'uj'
    ul = 'ul'
    uv = 'uv'
    uz = 'uz'
    un = 'un'
    vg = 'vg'
    v = 'v'
    vd = 'vd'
    vi = 'vi'
    vq = 'vq'
    vn = 'vn'
    w = 'w'
    wkz = 'wkz'
    wky = 'wky'
    wy = 'wy'
    wyz = 'wyz'
    wyy = 'wyy'
    wj = 'wj'
    ww = 'ww'
    wt = 'wt'
    wd = 'wd'
    wf = 'wf'
    wn = 'wn'
    wm = 'wm'
    ws = 'ws'
    wp = 'wp'
    wb = 'wb'
    wh = 'wh'
    x = 'x'
    yg = 'yg'
    y = 'y'
    z = 'z'
    zg = 'zg'
    email = 'email'
    tel = 'tel'
    ip = 'ip'
    url = 'url'


class Word:
    def __init__(self, freq, tag, length, word) :
        self.freq = freq
        self.tag = tag
        self.length = length
        self.word = word
    def __str__(self) :
        return ('[frequency %d | %s | length %d] %s' % (self.freq, 
            self.tag.value, self.length, self.word))


class WordDict:

    def __init__(self) :
        self.path_name = os.path.join(os.path.dirname(__file__), 
                'lexicon', 'dict.segd')
        self.dict = dict()
        self.max_len = 0
        self.load()

    def load(self) :
        with open(self.path_name) as f :
            for line in f.readlines() :
                word, freq, tag = line.split(' ')
                tag = tag.strip()
                self.dict[word] = Word(int(freq), WordTag[tag], len(word), word)
                if self.max_len < len(word) :
                    self.max_len = len(word)
    
    def get(self, word) :
        item = self.dict.get(word)
        return item
        

class TreeNode:
    
    def __init__(self, value) :
        self.value = value
        self.children = []

    def add_child(self, child) :
        self.children.append(child)

    def wfs(self, level) :
        print(level, ' ', self.value)
        for child in self.children :
            child.wfs(level + 1)


class Chunk:

    def __init__(self, index_next, c1, c2 = None, c3 = None) :
        self.items = []
        self.items.append(c1)
        if c2 is not None :
            self.items.append(c2)
        if c3 is not None :
            self.items.append(c3)
        self.index_next = index_next

    def total_length(self) :
        length = 0
        for item in self.items :
            length += item.length
        return length

    def average_length(self) :
        return float(self.total_length()) / float(len(self.items))

    def variance(self) :
        av = self.average_length()
        sum = 0.0
        for item in self.items :
            var = float(item.length - av)
            sum += var * var
        return sum

    def free_mor_degree(self) :
        sum = 0.0
        for item in self.items :
            sum += math.log(item.freq)
        return sum


class Alphabeta:

    def __init__(self, string) :
        self.string = string

    def __len__(self) :
        return 1

    def __str__(self) :
        return self.string

    def split(self, sep = None, maxsplit = -1) :
        tmp_list = []
        tmp_list.append(self.string)
        return tmp_list

class AmbiguityRes:

    def __init__(self, chunks) :
        self.chunks = chunks

    def mm_rule(self) :
        max_chunk_len = max(chunk.total_length() for chunk in self.chunks) 
        candidates = list()
        for chunk in self.chunks :
            if chunk.total_length() == max_chunk_len :
                candidates.append(chunk)
        if len(candidates) == 1 :
            return candidates, True
        else :
            return candidates, False

    def lawl_rule(self) :
        max_chunk_av = max(chunk.average_length() for chunk in 
                self.chunks) 
        candidates = list()
        for chunk in self.chunks :
            if chunk.average_length() == max_chunk_av :
                candidates.append(chunk)
        if len(candidates) == 1 :
            return candidates, True
        else :
            return candidates, False

    def svowl_rule(self) :
        min_chunk_var = min(chunk.variance() for chunk in self.chunks)
        candidates = list()
        for chunk in self.chunks :
            if chunk.variance() == min_chunk_var :
                candidates.append(chunk)
        if len(candidates) == 1 :
            return candidates, True
        else :
            return candidates, False

    def lsodomfoow_rule(self) :
        max_chunk_free = max(chunk.free_mor_degree() for chunk in 
                self.chunks)
        candidates = list()
        for chunk in self.chunks :
            if chunk.free_mor_degree() == max_chunk_free :
                candidates.append(chunk)
        if len(candidates) == 1 :
            return candidates, True
        else :
            return candidates, False

    def exec_rules(self) :
        chunks, succ = self.mm_rule()
        if succ is True :
            return chunks[0]
        self.chunks = chunks

        chunks, succ = self.lawl_rule()
        if succ is True :
            return chunks[0]
        self.chunks = chunks

        chunks, succ = self.svowl_rule()
        if succ is True :
            return chunks[0]
        self.chunks = chunks

        chunks, succ = self.lsodomfoow_rule()
        if succ is True :
            return chunks[0]
        self.chunks = chunks

        print('No rule works')
        return self.chunks[0]


class Segmentor:

    word_dict = WordDict()

    def __init__(self, text) :
        self.gram = list()
        self.tokens = list()
        self.text = text
        self.atomic_gram()
    
    def atomic_gram(self) :
        alpha_flag = False
        for i in range(len(self.text)) :
            if self.is_alphabeta(self.text[i]) or self.is_digit(self.text[i]) :
                if alpha_flag is False :
                    tmp = self.text[i]
                    alpha_flag = True
                else :
                    tmp += self.text[i]
                continue
            elif alpha_flag is True :
                alpha_flag = False
                item = Alphabeta(tmp)
                self.gram.append(item)

            tmp = self.text[i]
            item = self.text[i]
            for j in range(1, Segmentor.word_dict.max_len + 1) :
                if i + j >= len(self.text) :
                    break
                tmp += self.text[i + j]
                if tmp in Segmentor.word_dict.dict :
                    item = item + '/' + tmp
            self.gram.append(item)
        
    def gen_gram_chain(self, value, index) :
        tree_node = TreeNode(value)
        if index >= len(self.gram) :
            return tree_node
        candidates = self.gram[index].split('/')
        for candidate in candidates :
            child = self.gen_gram_chain(candidate, index + len(candidate))
            tree_node.add_child(child)
        return tree_node
    
    def gen_chunks(self, index) :
        words_a = self.gram[index].split('/')
        words_b = None
        words_c = None
        chunks = []
        for word_a in words_a :
            word_a_item = Segmentor.word_dict.get(word_a)
            if word_a_item is None :
                word_a_item = Word(1, WordTag.un, 1, word_a)
            index_next_b = index + len(word_a)
            if (index_next_b >= len(self.gram) or 
                    self.is_alsymbol(index_next_b)) :
                chunks.append(Chunk(index_next_b, word_a_item))
                continue
            words_b = self.gram[index_next_b].split('/')
            for word_b in words_b :
                word_b_item = Segmentor.word_dict.get(word_b)
                if word_b_item is None :
                    word_b_item = Word(1, WordTag.un, 1, word_b)
                index_next_c = index_next_b + len(word_b)
                if (index_next_c >= len(self.gram) or 
                        self.is_alsymbol(index_next_c)) :
                    chunks.append(Chunk(index_next_c, word_a_item, 
                        word_b_item))
                    continue
                words_c = self.gram[index_next_c].split('/')
                for word_c in words_c :
                    word_c_item = Segmentor.word_dict.get(word_c)
                    if word_c_item is None :
                        word_c_item = Word(1, WordTag.un, 1, word_c)
                    index_next = index_next_c + len(word_c)
                    chunks.append(Chunk(index_next, word_a_item, 
                        word_b_item, word_c_item))
        return chunks

    def print_chunks(self, chunks) :
        for chunk in chunks :
            for item in chunk.items :
                print(str(item), end = '\t')
            if chunk.index_next >= len(self.gram) :
                index_next = '#end'
            else :
                index_next = self.gram[chunk.index_next]
            print(' next@', chunk.index_next, index_next)

    def gen_tokens(self) :
        index = 0
        while index < len(self.gram) :
            if self.is_alsymbol(index) : 
                token = Segmentor.word_dict.get(self.gram[index])
                if token is None :
                    token = Word(1, WordTag.x, 1, self.gram[index])
                self.tokens.append(token)
                index += 1
                continue
            words = self.gram[index].split('/')
            if len(words) == 1 :
                token = Segmentor.word_dict.get(self.gram[index])
                if token is None :
                    token = Word(1, WordTag.un, 1, self.gram[index])
                self.tokens.append(token)
                index += 1
                continue

            chunks = self.gen_chunks(index)
            if len(chunks) == 1 :
                chunk = chunks[0]
            else :
                rule = AmbiguityRes(chunks)
                chunk = rule.exec_rules()
            for item in chunk.items :
                self.tokens.append(item)
                index = chunk.index_next

        return self.tokens

    def gen_key_tokens(self, pos = False) :
        tokens = self.gen_tokens()
        key_tokens = list()
        index = -1
        for token in tokens :
            index += 1
            if (token.tag == WordTag.p or token.tag == WordTag.x or
                    token.tag.value[0] == 'w' or token.tag == WordTag.r or
                    token.tag == WordTag.c or token.tag == WordTag.m or
                    token.tag.value[0] == 'u' or token.length == 1) :
                continue
            if pos is False :
                key_tokens.append(token)
            else :
                key_tokens.append((token, index))

        return key_tokens

    def gen_word_couples(self) :
        tokens = self.gen_key_tokens(pos = True)
        word_couples = list()
        index = 0
        for token, pos in tokens :
            if pos - 1 >= 0 and index - 1 >= 0 and tokens[index - 1][1] == pos - 1 :
                word = (tokens[index - 1][0].word, tokens[index][0].word)
                word_couples.append(word)
            index += 1
        return word_couples

    def is_alsymbol(self, index) :
        if (isinstance(self.gram[index], Alphabeta) or
        (self.gram[index] in Segmentor.word_dict.dict and 
        Segmentor.word_dict.dict[self.gram[index]].tag.value[0] == 'w')) :
            return True
        else :
            return False

    def is_alphabeta(self, s) :
        if len(s) > 1 :
            return False
        if (ord(s) >= 65 and ord(s) <= 90) or (ord(s) >= 97 and 
                ord(s) <= 122) :
            return True
        else :
            return False

    def is_digit(self, s) :
        if len(s) > 1 :
            return False
        if ord(s) >= 48 and ord(s) <= 57 :
            return True
        else :
            return False



