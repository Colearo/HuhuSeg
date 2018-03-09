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

    def load_corpura(self, corpura, corpura_attr, sim_mode , sim_threshold) :
        if not isinstance(corpura, list):
            print('Para corpura should be a List([str,])')
            return
        self.corpura = corpura
        self.corpura_attr = corpura_attr
        if sim_mode == 'BOW' :
            self.corpura_handle = Corpura((corpus[corpura_attr] for corpus in corpura))
            self.sim_mode = 0
        elif sim_mode == 'SIMHASH' :
            self.sim_mode = 1
        else :
            print('Para sim_mode cannot be recognized,'
                    'please refer to the help')
            return
        self.sim_threshold = sim_threshold

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

    def centroid_cluster_bow(self, min_size, weight_mode, weight_attr, weight) :
        clusters = list()
        centroids = list()
        for corpus in self.corpura :
            vector = BOW(corpus[self.corpura_attr], 
                    self.corpura_handle)
            index = 0
            is_sim = False

            for centroid in centroids :
                if weight_mode is True:
                    vector_b = BOW(corpus[weight_attr],
                            self.corpura_handle)
                    is_sim, sim = vector.weight_similarity(vector_b, centroid, weight, self.sim_threshold)
                else :
                    is_sim, sim = vector.similarity(centroid, 
                            self.sim_threshold)

                if is_sim is True :
                    clusters[index].append(corpus)
                    centroids[index].word_vector = (centroids[index].word_vector * (len(clusters[index]) - 1) + vector.word_vector) / len(clusters[index])
                    break

                index += 1
                
            if is_sim is False or len(centroids) == 0 :
                centroids.append(vector)
                clusters.append([corpus,])

        self.clusters = list()
        if min_size > 1 :
            for cluster in clusters :
                if len(cluster) >= min_size :
                    self.clusters.append(cluster)
        else :
            self.clusters = clusters

        return self.clusters

    def centroid_cluster(self, min_size, weight_mode = False, weight_attr = None, weight = 0.0) :
        if self.sim_mode == 0 :
            return self.centroid_cluster_bow(min_size, weight_mode, weight_attr, weight)
        elif self.sim_mode == 1 :
            return self.centroid_cluster_simhash(min_size)
    
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


