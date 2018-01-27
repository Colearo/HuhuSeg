#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from huhu_seg import Segmentor

# s = Segmentor('小明硕士毕业于中国科学院SAP计算所,后在日本京都大学深造')
# s = Segmentor('李智伟高高兴兴王晓薇出去玩，后来智伟和晓薇又单独去玩了')
s = Segmentor('为人民办公益')
tokens = s.gen_tokens()
for item in tokens:
    print(str(item))


