from sklearn.metrics import normalized_mutual_info_score
from sklearn.metrics import f1_score

from dbscan import dbscan
from sklearn.cluster.dbscan_ import DBSCAN

from collections import defaultdict
import numpy as np
import math
import json
import sys
import re
import random

from sekitei import sekitei


def purity(mysekitei, regexpes, good_urls, urls, n_urls=500,
           n_bootstreping=25, verbose=False):

    """ Calculate the metrics of a quality
        of the clusterization for a site

        The estimation is the clearence of a cluster
        with bootstrepping (averaging by random selections)
    """

    estimation = 0.
    
    classes = [ 0, 1 ]
    clusters = [ v[0] for v in regexpes ]
    clusters.sort()
    if verbose: print 'clusters= %d\n' % len(clusters)

    y = [1] * n_urls + [0] * n_urls
    for step in xrange(n_bootstreping):
        random.shuffle(good_urls)
        random.shuffle(urls)

        fit_urls = good_urls[:n_urls] + urls[:n_urls] 
        new_urls = good_urls[n_urls:2*n_urls] + urls[n_urls:2*n_urls]
        
        P = mysekitei.matrix_of_existing_features(new_urls)
        distrib  = mysekitei.distribute_among_clusters(P, regexpes)

        count0 = [0.] * len(clusters)
        count1 = [0.] * len(clusters)

        for i,c in enumerate(clusters):
            for j,p in enumerate(distrib):
                if p == c:
                    if    j <  n_urls: count0[i] += 1.
                    elif  j >= n_urls: count1[i] += 1.
                    else:  raise ValueError

        estimation += sum([ max(c0, c1) for c0,c1 in zip(count0, count1) ]) / (2 * n_urls)
        if verbose: print '%d  estimation= %f' % (step, estimation)
            
    return  estimation / n_bootstreping


def read_clusters(clusters_filename):
    """ mysekitei, regexpes=[(class, freq_features, their_indices)] """
    mysekitei = sekitei([], alpha=0.01)

    regexpes = []

    c, n = 0, 0
    res, indices = [], []
    with open(clusters_filename, 'r') as file:
        for line in file.readlines():
            if (line[0:3] == '---'):
                ls = line[3:].split()
                c, n = int(ls[0]), int(ls[2])
            elif (n):
                r, i = line.split()
                i = int(i)
                mysekitei.tags.add(r)
                mysekitei.tags_order[i] = r
                res.append(r)
                indices.append(i)
                n -= 1

                if not n:
                    regexpes.append([c, res, indices])
                    res, indices = [], []

            elif len(line) and line.split() and line.split()[0] == 'n_features=':
                mysekitei.n_features = int(line.split()[1])
                mysekitei.tags_order = [''] * mysekitei.n_features

    return mysekitei, regexpes
