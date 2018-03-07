#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
from .simhash import SimHash
from .bow import BOW, Corpura

class Cluster:

    def __init__(self, corpura, corpura_attr, sim_mode , sim_threshold) :
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

    def centroid_cluster_simhash(self) :
        self.clusters = list()
        self.centroids = list()
        for corpus in self.corpura :
            sim_hash = SimHash(corpus[self.corpura_attr])

            index = 0
            is_sim = False

            for centroid in self.centroids :
                is_sim = sim_hash.similarity(self.centroid, 
                        self.sim_threshold)
                if is_sim is True :
                    self.clusters[index].append(corpus)
                    break
                index += 1

            if is_sim is False or len(self.centroids) == 0 :
                self.centroids.append(sim_hash)
                self.clusters.append([corpus,])

        return self.clusters

    def centroid_cluster_bow(self, weight_mode, weight_atrr, weight) :
        self.clusters = list()
        self.centroids = list()
        for corpus in self.corpura :
            vector = BOW(corpus[self.corpura_attr], 
                    self.corpura_handle)

            index = 0
            is_sim = False

            for centroid in self.centroids :
                if weight_mode is True:
                    vector_b = BOW(corpus[weight_atrr],
                            self.corpura_handle)
                    is_sim = vector.weight_similarity(vector_b, centroid, weight, self.sim_threshold)
                else :
                    is_sim = vector.similarity(centroid, 
                            self.sim_threshold)

                if is_sim is True :
                    self.clusters[index].append(corpus)
                    self.centroids[index].word_vector = (self.centroids[index].word_vector * (len(self.clusters[index]) - 1) + vector.word_vector) / len(self.clusters[index])
                    break

                index += 1

            if is_sim is False or len(self.centroids) == 0 :
                self.centroids.append(vector)
                self.clusters.append([corpus,])
        return self.clusters

    def centroid_cluster(self, weight_mode = False, weight_atrr = None, weight = 0.0) :
        if self.sim_mode == 0 :
            return self.centroid_cluster_bow(weight_mode, weight_atrr, weight)
        elif self.sim_mode == 1 :
            return self.centroid_cluster_simhash()
    
    def hierachical_cluster(self, h_threshold) :
        pass



