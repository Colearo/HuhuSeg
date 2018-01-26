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
    def __init__(self, freq, tag, length) :
        self.freq = freq
        self.tag = tag
        self.length = length
    def __str__(self) :
        return ('[frequency %d | %s | length %d]' % (self.freq, 
            self.tag.value, self.length))


class WordDict:

    def __init__(self) :
        self.path_name = os.path.join(os.path.dirname(__file__), os.pardir, 
                'lexicon', 'dict.lex')
        self.dict = dict()
        self.max_len = 0
        self.load()

    def load(self) :
        with open(self.path_name) as f :
            for line in f.readlines() :
                word, freq, tag = line.split(' ')
                tag = tag.strip()
                self.dict[word] = Word(int(freq), WordTag[tag], len(word))
                if self.max_len < len(word) :
                    self.max_len = len(word)
    
    def get(self, word) :
        item = self.dict.get(word)
        return item
        

class Chunk:

    def __init__(self, c1, c2 = None, c3 = None) :
        self.items = []
        self.items.append(c1)
        if c2 is not None :
            self.items.append(c2)
        if c3 is not None :
            self.items.append(c3)

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

class Segmentor:

    def __init__(self, text) :
        self.gram = list()
        self.word_dict = WordDict()
        self.text = text
    
    def atomic_gram(self) :
        for i in range(len(self.text)) :
            self.gram.append(self.text[i])
            tmp = self.text[i]
            for j in range(1, self.word_dict.max_len + 1) :
                if i + j >= len(self.text) :
                    break
                tmp += self.text[i + j]
                if tmp in self.word_dict.dict :
                    self.gram[i] = self.gram[i] + '/' + tmp
                else :
                    break

s = Segmentor('小明硕士毕业于中国科学院计算所，后在日本京都大学深造')
s.atomic_gram()
print(s.gram)


