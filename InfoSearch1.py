import numpy as np
import random
import math
import sys
import re

from collections import defaultdict
from sklearn.cluster.dbscan_ import DBSCAN
from dbscan import dbscan

from vizualize import vizualize_clusters
from sekitei import sekitei
from purity import purity
from som import som_create_and_save


# np.set_printoptions(threshold=np.nan, precision=2)


def get_clusters(good_urls, urls, n_urls=500):
    random.shuffle(good_urls)
    random.shuffle(urls)

    fit_urls = good_urls[:n_urls] + urls[:n_urls]
    new_urls = good_urls[n_urls:2*n_urls:] + urls[n_urls:2*n_urls:]

    mysekitei = sekitei(fit_urls, alpha=0.01)
    # mysekitei.get_features_from_url('http://kinopoisk.ru/community/cf_user/398867/page/1/r7.php?p=17', verbose=True)
    mysekitei.fit()

    X = mysekitei.most_freq_features()
    print  mysekitei.n_features, '\n\n', # '\n'.join(mysekitei.tags_order[:mysekitei.n_features]), '\n\n'    
    
    py = DBSCAN().fit_predict(X)
    # py = dbscan().fit_predict(X)

    hist = []
    clusters = list(set(py))
    with open('data/clusters_features.txt', 'w') as f:
        
        print >>f,  mysekitei.n_features
        print >>f, '\n\n\n', '\n'.join(mysekitei.tags_order[:mysekitei.n_features]), '\n\n'

        for c in clusters:
            hist.append(len([p for p in py if p == c]))
            # print c, ':', hist[-1]
            # print >>f, c, ':', hist[-1]

    vizualize_clusters(X, ([1] * n_urls + [0] * n_urls), py, hist)
    
    P = mysekitei.matrix_of_existing_features(new_urls)
    regexpes = mysekitei.get_clusters_regexpes(X, py)

    with open('data/clusters_freq_features.txt', 'w') as file:
        for c,f,i in regexpes[:-1]:
            print '---', c, '=', str(len(f))
            print '\n'.join([fi + '\t\t\t: ' + str(ii) for fi,ii in zip(f,i)]), '\n'
            print >>file, '---', c, '=', str(len(f))
            print >>file, '\n'.join([fi + '\t\t\t: ' + str(ii) for fi,ii in zip(f,i)]), '\n'

    with open('data/united_regexpes.txt', 'w') as file:
        for k,f,i in regexpes[:-1]:
            rex = '^'
            for r in f[:-1]:
                rex += '(?=%s)' % r.strip('^').rstrip('$')
            rex += '%s' % f[-1].strip('^')
            print >>file, k, '=', rex

    return None


if __name__ == "__main__":

    with open('data/urls.kinopoisk.examined.txt', 'r') as f:
        good_urls = f.readlines()

    with open('data/urls.kinopoisk.general.txt', 'r') as f:
        urls = f.readlines()

    good_urls = [ re.sub(ur'\r?\n', u'', url.lower()) for url in good_urls ]
    urls      = [ re.sub(ur'\r?\n', u'', url.lower()) for url in urls ]

    if sys.argv[1] == '-p':
        res = purity(good_urls, urls, 500, 25, verbose=True)
        print res
        with open('data/purity.txt', 'w') as out:
            out.write(str(res) + '\n')

    if sys.argv[1] == '-c':
        get_clusters(good_urls, urls)
    
    if sys.argv[1] == '-s':
        som_create_and_save(good_urls, urls)
