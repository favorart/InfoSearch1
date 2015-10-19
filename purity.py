from sklearn.metrics import normalized_mutual_info_score
from sklearn.metrics import f1_score

from dbscan import dbscan
from sklearn.cluster.dbscan_ import DBSCAN

from collections import defaultdict
import numpy as np
import math
import json
import sys
import io
import os
import re
import random

from sekitei import sekitei



""" Calculate the metrics of a quality
    of the clusterization for a site

    The estimation is the clearence of a cluster
    with bootstrepping (averaging by random selections)
"""
def purity(good_urls, urls, n_urls, n_bootstreping=15, verbose=False):
    estimation = 0.

    y = [1] * n_urls + [0] * n_urls
    for i in xrange(n_bootstreping):
        random.shuffle(good_urls)
        random.shuffle(urls)

        fit_urls = good_urls[:n_urls] + urls[:n_urls]            
        mysekitei = sekitei(fit_urls, alpha=0.01)
        mysekitei.fit()
        X = mysekitei.most_freq_features()

        dbs = DBSCAN() # (eps=1.2)
        py = dbs.fit_predict(X)

        classes = [ 0, 1 ]
        clusters = list(set(py))
        if verbose: print '%d  clusters= %d' % (i, len(clusters))

        count0 = [0] * len(clusters)
        count1 = [0] * len(clusters)

        for i,c in enumerate(clusters):
            for j,p in enumerate(py):
                if p == c:
                    if    j <  n_urls: count0[i] += 1
                    elif  j >= n_urls: count1[i] += 1
                    else: raise ValueError

        estimation += float( sum([ max(c0, c1) for c0,c1 in zip(count0, count1) ]) ) / (2 * n_urls)
        if verbose: print 'estimation= %f\n' % estimation
            
    return  estimation / n_bootstreping


