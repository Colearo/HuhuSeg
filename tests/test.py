#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from huhu_seg.segmentor import Segmentor

# s = Segmentor('小明硕士毕业于中国科学院SAP计算所,后在日本京都大学深造')
# s = Segmentor('李智伟高高兴兴和王晓薇出去玩，后来智伟和晓薇又单独去玩了')
# s = Segmentor('为人民办公益')
# s = Segmentor('杭州西湖风景很好，是旅游胜地！')
# s = Segmentor('张三买了张三角桌')
# s = Segmentor('张三买了部iPhone8手机')
# s = Segmentor('工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作')
# s = Segmentor('这里有关天培的有关事迹')
if __name__ == '__main__' :
    s = Segmentor('李智伟高高兴兴和王晓薇出去玩。后来智伟和晓薇又单独去玩了。')
    tokens = s.gen_tokens_parallel()
    for item in tokens:
        print(str(item))


