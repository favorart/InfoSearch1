import numpy as np
import random
import math
import sys
import re
import os

from collections import defaultdict
from sklearn.cluster.dbscan_ import DBSCAN
from dbscan import dbscan

from sekitei import sekitei
from purity import purity, read_clusters
from som import som_create_and_save


def get_clusters(good_urls, urls, n_urls=500, my_dbs=False, verbose=False):
    """ """
    random.shuffle(good_urls)
    random.shuffle(urls)

    fit_urls = good_urls[:n_urls] + urls[:n_urls]

    mysekitei = sekitei(fit_urls, alpha=0.01)
    mysekitei.fit()

    X = mysekitei.most_freq_features()
    
    if my_dbs: py = dbscan().fit_predict(X)
    else:      py = DBSCAN().fit_predict(X)
        
    regexpes = mysekitei.get_clusters_regexpes(X, py)

    print  'n_features=', mysekitei.n_features, '\n\n'
    for c,f,i in regexpes:
        print '---', c, '=', str(len(f))
        print '\n'.join([fi + '\t\t\t ' + str(ii) for fi,ii in zip(f,i)]), '\n'

    return mysekitei, regexpes


if __name__ == "__main__":

    if len(sys.argv) > 2:
        file_exm = sys.argv[2]
        file_gen = sys.argv[1]
    else: raise ValueError
        
    with open(file_exm, 'r') as f:
        good_urls = f.readlines()

    with open(file_gen, 'r') as f:
        urls = f.readlines()

    good_urls = [ re.sub(ur'\r?\n', u'', url.lower()) for url in good_urls ]
    urls      = [ re.sub(ur'\r?\n', u'', url.lower()) for url in urls ]

    if len(sys.argv) > 3:
        mysekitei, regexpes = read_clusters(sys.argv[3])
        print purity(mysekitei, regexpes, good_urls, urls, 500, 25)
    else:
        mysekitei, regexpes = get_clusters(good_urls, urls)
        som_create_and_save(mysekitei, regexpes, good_urls, urls)

