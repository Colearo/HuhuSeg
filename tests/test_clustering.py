#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
import time
import re
import json
from huhu_seg.clustering import Cluster

r = redis.Redis(host = 'localhost', port = 6379, decode_responses = True)

start = time.time()
data = list()
for i in r.sscan_iter('news_content') :
    d = eval(i)
    content = d.get('Content')
    if content is None or content.strip() == '':
        continue
    date = d.get('Date')
    if date is None or time.strptime(date, '%Y/%m/%d %H:%M') < time.strptime('2018/03/01 00:00', '%Y/%m/%d %H:%M') :
        continue
    data.append(d)
    print('[%s] %s' % (d['Title'], date))

c = Cluster(data, 'Content', 'BOW', 0.8)
list = c.centroid_cluster(False)
cluster = []

for item in list :
    if len(item) >= 3 :
        print('Cluster: ', len(item))
        print(item)
        cluster.append(item)

with open('./cluster.json', 'w') as w :
    json.dump(cluster, w)

with open('./cluster.json', 'r') as r :
    cluster = json.load(r)

corpura = []
for c in cluster :
    corpura.append(c[0])

c = Cluster(corpura, 'Content', 'BOW', 0.15)
l = c.centroid_cluster(True, 'Title', 0.5)

index = 0
for item in l :
    print('Cluster %d' % index)
    for i in item :
        print('[%s]' % i['Title'])
    index += 1

duration = time.time() - start
print('Runs %.2f s' % duration)

