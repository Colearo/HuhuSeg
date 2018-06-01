#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
import json
from datetime import datetime, timedelta
from .bow import BOW, Corpura

class Cluster:

    def __init__(self) :
        self.clusters = list()
        self.corpura_handle = Corpura()

    def load_corpura(self, corpura, corpura_attr) :
        if not isinstance(corpura, list):
            print('[ERROR]Para corpura should be a List([str,])')
            return
        self.corpura = corpura
        self.corpura_attr = corpura_attr
        self.corpura_handle = Corpura((corpus[corpura_attr] for corpus in corpura))

    def load_model(self, model_path) :
        with open(model_path, 'r') as r :
            self.model = json.load(r)
        self.clusters = self.model['clusters']
        self.corpura_handle = Corpura()
        self.corpura_handle.load_dict(model_path + '.dict')

    def save_model(self, model_path) :
        self.model = dict()
        self.model['clusters'] = self.clusters
        with open(model_path, 'w') as f:
            json.dump(self.model, f)
        self.corpura_handle.save_dict(model_path + '.dict')

    def centroid_cluster_bow(self, min_size) :
        clusters = list()
        centroids = list()
        vectors = list()

        THR_E = 0.75
        THR_N = 0.35

        for corpus in self.corpura :
            vector = BOW(corpus[self.corpura_attr], 
                    self.corpura_handle)
            sums = vector.word_vector.sum()
            vectors.append((corpus, vector, sums))
        vectors.sort(key = lambda d:d[2], reverse = True)

        for corpus, vector, sums in vectors :
            max_sim = 0.0
            max_sim_centroid = None
            max_sim_i = 0
            max_sim_j = 0

            for centroid, i, j in centroids :
                is_sim, sim = vector.similarity(centroid)
                if sim > max_sim :
                    max_sim = sim
                    max_sim_centroid = centroid
                    max_sim_i = i
                    max_sim_j = j

            if len(centroids) == 0 :
                centroids.append((vector, 0, 0))
                clusters.append([[corpus,],])
                continue

            cluster = clusters[max_sim_i][max_sim_j]
            if max_sim > THR_E:
                cluster.append(corpus)
                max_sim_centroid.word_vector = (max_sim_centroid.word_vector * (len(cluster) - 1) + vector.word_vector) / len(cluster)
            elif max_sim <= THR_E and max_sim > THR_N :
                centroids.append((vector, max_sim_i, len(clusters[max_sim_i])))
                clusters[max_sim_i].append([corpus,])
            else :
                centroids.append((vector, len(clusters), 0))
                clusters.append([[corpus,],])

        if min_size > 1 :
            for cluster in clusters :
                total = 0
                for c in cluster :
                    total += len(c)
                if total >= min_size :
                    self.clusters.append(cluster)
        else :
            self.clusters = clusters

        return self.clusters
    
    def print_cluster(self) :
        i = 0
        for cluster in self.clusters :
            j = 0
            print('Topic %d' % i)
            for c in cluster :
                print('Subtopic %d' % j)
                print([item['Title'] for item in c])
                j += 1
            i += 1

    def merge_model(self, other) :
        self.clusters += other.clusters
        self.corpura_handle.merge_dict(other.corpura_handle)

    def merge_models(self, others) :
        for other in others :
            self.merge_model(other)

class Timeline :

    def __init__(self, subtopic_clusters, content_attr) :
        corpura = [corpus[content_attr] for corpus in sum([sub for subtopic_id, sub in subtopic_clusters], [])]
        self.subtopic_clusters = subtopic_clusters
        self.corpura_handle = Corpura(corpura)
        self.content_attr = content_attr
        self.topic_centroids = list()
        self.topics = list()

    def add_subtopic(self, cur_centroid, subtopic, attr) :
        THR = 0.55
        max_sim = 0.0 
        max_sim_index = 0
        max_sim_topic_centroid = None
        for topic_centroid, index in self.topic_centroids :
            is_sim, sim = cur_centroid.similarity(topic_centroid)
            if sim > max_sim :
                max_sim = sim
                max_sim_index = index
                max_sim_topic_centroid = topic_centroid

        if len(self.topic_centroids) == 0 or max_sim < THR :
            topic_centroid = (cur_centroid, len(self.topic_centroids))
            self.topic_centroids.append(topic_centroid)
            self.topics.append([(attr, subtopic),])
            return

        if max_sim >= THR :
            self.topics[max_sim_index].append((attr, subtopic))
            max_sim_topic_centroid.word_vector = (max_sim_topic_centroid.word_vector * (len(self.topics[max_sim_index]) - 1) + cur_centroid.word_vector) / len(self.topics[max_sim_index])

    def timeline_topics(self) :
        for attr, sub in self.subtopic_clusters :
            cur_centroid = self.corpura_handle.corpura2total_bow([item[self.content_attr] for item in sub])
            self.add_subtopic(cur_centroid, sub, attr)


