#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import numpy
import math
from .bow import Corpura

class HotSpot :

    def __init__(self, clusters = None, content_attr = 'Content') :
        self.flat = lambda L: sum(map(self.flat,L),[]) if isinstance(L,list) else [L]
        self.clusters = clusters
        self.content_attr = content_attr

    def computing_clusters(self) :
        if not isinstance(self.clusters, collections.Iterable) :
            print('Para corpura should be an iterable object')
            return
        self.corpura_inst = Corpura([corpus[self.content_attr] for corpus in self.flat(self.clusters)])
        doc_freq = list()
        for cluster in self.clusters :
            doc_freq.append(sum([len(c) for c in cluster]))
        doc_freq_array = numpy.array(doc_freq)
        doc_freq_array = doc_freq_array / numpy.linalg.norm(doc_freq_array)

        self.hot_news = list()
        for i in range(len(doc_freq)) :
            percent_doc_freq = float(doc_freq[i]) / float(sum(doc_freq))
            bow = self.corpura_inst.corpura2average_bow([corpus[self.content_attr] for corpus in self.flat(self.clusters[i])])
            total_weights = sum(bow.word_vector)
            hotspot = doc_freq_array[i] * math.exp(percent_doc_freq) * math.log(total_weights)
            self.hot_news.append((self.clusters[i], hotspot))
        self.hot_news.sort(key = lambda d:d[1], reverse = True)
        return self.hot_news

    def computing_keywords(self, keywords_set, days_corpura) :
        keywords_hi = dict()
        for keyword, cooccur_weight in keywords_set :
            hotspot_index = dict()
            for date, corpura in days_corpura :
                term_freq = 0
                doc_freq = 0
                for corpus in corpura :
                    if keyword in corpus[self.content_attr] :
                        term_freq += math.log(1 + corpus[self.content_attr].count(keyword))
                        doc_freq += 1
                hotspot_index[date] = cooccur_weight * term_freq * math.log(len(corpura) / (1 + doc_freq))
            keywords_hi[keyword] = hotspot_index

        return keywords_hi



