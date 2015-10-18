import numpy as np
import random
import math
import sys
import io
import os
import re

from matplotlib import pyplot
import matplotlib as plt

from sklearn.manifold import TSNE
from sklearn.cluster.dbscan_ import DBSCAN
from dbscan import dbscan

from sekitei import sekitei
from purity import estimate
from som import som_create, som_save

# np.set_printoptions(threshold=np.nan, precision=2)

def get_clusters(good_urls, urls, n_urls=500):
    random.shuffle(good_urls)
    random.shuffle(urls)

    fit_urls = good_urls[:n_urls] + urls[:n_urls]
    predict_urls = good_urls[n_urls:2*n_urls:] + urls[n_urls:2*n_urls:]

    mysekitei = sekitei(fit_urls, alpha=0.01)
    # mysekitei.get_features_from_url('http://kinopoisk.ru/community/cf_user/398867/page/1/r7.php?p=17', verbose=True)
    mysekitei.fit()

    X = mysekitei.most_freq_features()
    print  mysekitei.n_features, '\n'
    print '\n'.join(mysekitei.tags_order[:mysekitei.n_features]), '\n\n'
    
    P = mysekitei.matrix_of_existing_features(predict_urls)

    dbs = DBSCAN(eps=1.2)
    y = [1] * n_urls + [0] * n_urls
    dbs.fit(X,y)
    py = dbs.fit_predict(P)

    # dbs1 = dbscan(epsilon=1.2)
    # py = dbs1.fit_predict(P)

    clusters = list(set(py))
    with open('data/clusters_fill.txt', 'w') as f:
        
        print >>f,  mysekitei.n_features
        print >>f, '\n\n\n', '\n'.join(mysekitei.tags_order[:mysekitei.n_features]), '\n\n'

        hist = []
        for c in clusters:
            hist.append(len([p for p in py if p == c]))
            print c, ':', hist[-1]
            print >>f, c, ':', hist[-1]

    regexpes = mysekitei.get_regexp(X,py)

    for k,v in regexpes.items():
        print k, len(v) # regexpes

    with open('data/clusters_selected_features.txt', 'w') as f:
        for k,v in regexpes.items():       
            print >>f, k, '='
            print >>f, '\n'.join(v)
            print >>f, '\n'

    with open('data/reg_expes.txt', 'w') as f:
        for k,v in regexpes.items():
            rex = '^'
            for r in v:
                rex += '(?=%s)' % r.strip('^').rstrip('$')
            rex += '$'
            print >>f, k, '=', rex

    return None


def vizualize_clusters(X, y, py, P=None, hist=None):
    model = TSNE(n_components=2, random_state=0)

    fig = model.fit_transform(X,y)

    if (P is not None):
        fig1 = model.fit_transform(P,py)
    else:
        fig1 = model.fit_transform(X,py)

    pyplot.figure(figsize=(8, 8))
    pyplot.subplot(121)
    classes = list(set(y))
    for c,color in zip(classes, matplotlib.colors.cnames.iteritems()):
        indeces = [ i for i,p in enumerate(y) if p == c ] 
        pyplot.scatter(fig[indeces, 0], fig[indeces, 1], marker='o', c=color[0])

    pyplot.subplot(122)
    classes = list(set(py))
    for c,color in zip(classes, matplotlib.colors.cnames.iteritems()):
        indeces = [ i for i,p in enumerate(py) if p == c ] 
        pyplot.scatter(fig1[indeces, 0], fig1[indeces, 1], marker='o', c=color[0])
    pyplot.show()

    if hist is not None:
        pyplot.figure(figsize=(8, 8))
        classes = list(set(py))
        pyplot.hist(classes, hist)
        pyplot.show()


if __name__ == "__main__":

    with open('data/urls.kinopoisk.examined.txt', 'r') as f:
        good_urls = f.readlines()

    with open('data/urls.kinopoisk.general.txt', 'r') as f:
        urls = f.readlines()

    good_urls = [ re.sub(ur'\r?\n', u'', url.lower()) for url in good_urls ]
    urls      = [ re.sub(ur'\r?\n', u'', url.lower()) for url in urls ]

    if sys.argv[1] == '-p':
        myestimate = estimate(15)
        res = myestimate.purity(good_urls, urls, 500, verbose=True)
        print res
        with open('data/purity.txt', 'w') as out:
            out.write(str(res) + '\n')
    
    if sys.argv[1] == '-s':
        som_create(good_urls, urls)
    
    if sys.argv[1] == '-c':
        get_clusters(good_urls, urls, 100)

