#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
import json
from datetime import datetime, timedelta
from .simhash import SimHash
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

    def centroid_cluster_simhash(self, min_size) :
        clusters = list()
        centroids = list()
        for corpus in self.corpura :
            sim_hash = SimHash(corpus[self.corpura_attr])

            index = 0
            is_sim = False

            for centroid in centroids :
                is_sim = sim_hash.similarity(centroid, 
                        self.sim_threshold)
                if is_sim is True :
                    clusters[index].append(corpus)
                    break
                index += 1
            if is_sim is False or len(centroids) == 0 :
                centroids.append(sim_hash)
                clusters.append([corpus,])

        self.clusters = list()
        if min_size > 1 :
            for cluster in clusters :
                if len(cluster) >= min_size :
                    self.clusters.append(cluster)
        else :
            self.clusters = clusters
        
        return self.clusters

    def centroid_cluster_bow(self, min_size) :
        clusters = list()
        centroids = list()
        vectors = list()

        THR_E = 0.75
        THR_N = 0.35

        for corpus in self.corpura :
            vector = BOW(corpus[self.corpura_attr], 
                    self.corpura_handle)
            sums = sum(vector.word_vector)
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
                temp = list()
                for c in cluster :
                    if len(c) >= min_size :
                        temp.append(c)
                if len(temp) > 0 :
                    self.clusters.append(temp)

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

    def hierachical_cluster(self, h_threshold, h_attr, weight_attr, weight , date_attr = 'Date') :
        clusters = list()
        centroids = list()
        for cluster in self.clusters :
            vector = self.corpura_handle.corpura2average_bow(
                    [c[h_attr] for c in cluster])
            vector_b = self.corpura_handle.corpura2average_bow(
                    [c[weight_attr] for c in cluster])
            if vector is None or vector_b is None:
                continue
            vector = BOW(None, None, vector)
            vector_b = BOW(None, None, vector_b)
            index = 0
            is_sim = False
            for centroid in centroids :
                # centroid_b = self.corpura_handle.corpura2average_bow(
                        # [c[weight_attr] for c in sum(clusters[index], [])])
                # if centroid_b is None :
                    # continue
                # centroid_b = BOW(None, None, centroid_b)
                is_sim, sim = vector.similarity(centroid, h_threshold)
                is_sim, sim_b = vector_b.similarity(centroid, h_threshold)
                sim = sim * (1 - weight) + sim_b * weight

                cur_date = datetime.strptime(cluster[0][date_attr], 
                        '%Y/%m/%d %H:%M')
                other_1st_date = datetime.strptime(
                        clusters[index][0][0][date_attr],
                        '%Y/%m/%d %H:%M')
                other_fin_date = datetime.strptime(
                        clusters[index][-1][-1][date_attr], 
                        '%Y/%m/%d %H:%M')
                date_dis = ((cur_date - other_1st_date) + 
                        (cur_date - other_fin_date)) / 2 
                date_dis = abs(date_dis.days)
                sim = sim - date_dis * 0.025
                is_sim = True if sim > h_threshold else False

                if is_sim is True :
                    clusters[index].append(cluster)
                    centroids[index].word_vector = (centroids[index].word_vector * (len(clusters[index]) - 1) + vector.word_vector) / len(clusters[index])
                    # centroids[index].word_vector += vector.word_vector
                    break
                index += 1

            if is_sim is False or len(centroids) == 0 :
                centroids.append(vector)
                clusters.append([cluster,])

        self.clusters = clusters
        
        return self.clusters

    def merge_model(self, other) :
        self.clusters += other.clusters
        self.corpura_handle.merge_dict(other.corpura_handle)

    def merge_models(self, others) :
        for other in others :
            self.merge_model(other)


