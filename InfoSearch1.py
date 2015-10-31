import numpy as np
import random
import math
import sys
import re
import os

from collections import defaultdict
from sklearn.cluster.dbscan_ import DBSCAN
from dbscan import dbscan

from vizualize import vizualize_clusters
from sekitei import sekitei
from purity import purity, read_clusters
from som import som_create_and_save


# np.set_printoptions(threshold=np.nan, precision=2)


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

    hist = []
    clusters = list( set(py) )
    with open('data/clusters_features.txt', 'w') as file:
        
        print >>file,  mysekitei.n_features
        print >>file, '\n\n\n', '\n'.join(mysekitei.tags_order[:mysekitei.n_features]), '\n\n'

        for c in clusters:
            hist.append(len([p for p in py if p == c]))
            # print >>f, c, ':', hist[-1]

    vizualize_clusters(X, ([1] * n_urls + [0] * n_urls), py, hist)
    
    regexpes = mysekitei.get_clusters_regexpes(X, py)

    with open('data/clusters_freq_features.txt', 'w') as file:
        print  'n_features=', mysekitei.n_features, '\n\n'
        print >>file, 'n_features=', mysekitei.n_features, '\n\n'
        for c,f,i in regexpes:
            print '---', c, '=', str(len(f))
            print '\n'.join([fi + '\t\t\t ' + str(ii) for fi,ii in zip(f,i)]), '\n'
            print >>file, '---', c, '=', str(len(f))
            print >>file, '\n'.join([fi + '\t\t\t ' + str(ii) for fi,ii in zip(f,i)]), '\n'

    with open('data/united_regexpes.txt', 'w') as file:
        for k,f,i in regexpes:
            rex = '^'
            for r in f[:-1]:
                rex += '(?=%s)' % r.strip('^').rstrip('$')
            rex += '%s' % f[-1].strip('^')
            print >>file, k, '=', rex

    return mysekitei, regexpes


if __name__ == "__main__":

    # python <module 1>.py ../urls/urls.kinopoisk.general ../urls/urls.kinopoisk.examined  >clusters_regulars.txt
    # python <module_2>.py ../urls/urls.kinopoisk.general ../urls/urls.kinopoisk.examined clusters_regulars.txt

    if not os.path.exists('data'):
        os.makedirs('data')

    if len(sys.argv) > 2:
        file_exm = sys.argv[2]
        file_gen = sys.argv[1]
    else:
        raise ValueError
        
    with open(file_exm, 'r') as f:
        good_urls = f.readlines()

    with open(file_gen, 'r') as f:
        urls = f.readlines()

    good_urls = [ re.sub(ur'\r?\n', u'', url.lower()) for url in good_urls ]
    urls      = [ re.sub(ur'\r?\n', u'', url.lower()) for url in urls ]

    if len(sys.argv) > 3:
        # clusters_filename='data/clusters_freq_features.txt'
        mysekitei, regexpes = read_clusters(sys.argv[3])
        res = purity(mysekitei, regexpes, good_urls, urls, 500, 25)

        print res
        with open('data/purity.txt', 'w') as file:
            print >>file, res      
    else:
        mysekitei, regexpes = get_clusters(good_urls, urls)
        som_create_and_save(mysekitei, regexpes, good_urls, urls)

