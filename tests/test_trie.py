#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from huhu_seg.trie import TrieAC

t = TrieAC()
t.add('BBCD')
t.add('BBE')
t.add('BBZ')
t.add('BCD')
t.add('BE')
t.add('BEE')
t.add('BG')
t.add('BXD')
t.add('B')
t.add('CD')
t.add('EE')
t.add('FB')
t.add('XD')
t.add('Y')
t.gen_failure()
print(t.output)
print(t.tree)
print(t.goto)
print(t.failure)
print(t.search('BCDFCDBE'))

