import numpy as np
import random
import math
import sys
import io
import os
import re

from matplotlib import pyplot
import matplotlib
# import matplotlib as plt
from sklearn.manifold import TSNE

from sekitei import sekitei
from cluster import find_clusters

from sklearn.cluster.dbscan_ import DBSCAN

def run1(good_urls, urls, n_urls=500):
    random.shuffle(good_urls)
    random.shuffle(urls)

    full_urls = good_urls + urls
    fit_urls = good_urls[:n_urls] + urls[:n_urls]
    predict_urls = good_urls[n_urls:2*n_urls:] + urls[n_urls:2*n_urls:]
    # random.shuffle(fit_urls)

    mysekitei = sekitei(fit_urls, alpha=0.01)
    # mysekitei.get_features_from_url('http://kinopoisk.ru/community/cf_user/398867/page/1/r7.php?p=17', verbose=True)
    mysekitei.fit()

    X = mysekitei.most_freq_features()
    np.set_printoptions(threshold=np.nan)
    # print '\n'.join(fit_urls[:11])
    # print mysekitei.X[:11,:20], '\n'    
    
    print  mysekitei.n_features, '\n'
    print '\n'.join(mysekitei.tags_order[:mysekitei.n_features]), '\n\n'
    
    # P = mysekitei.matrix_of_existing_features(predict_urls)
        
    dbs = DBSCAN(eps=1.5)
    y = [1] * n_urls + [0] * n_urls
    # dbs.fit(X,y)
    # py = dbs.fit_predict(P)
    py = dbs.fit_predict(X)

    # mysekitei.get_regexp(P,py)
    mysekitei.get_regexp(X,y)

    model = TSNE(n_components=2, random_state=0)

    fig = model.fit_transform(X,y)
    # fig1 = model.fit_transform(P,py)
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

    hist = []
    with open('state1.txt', 'w') as f:
        
        print >>f,  mysekitei.n_features
        print >>f, '\n\n\n', '\n'.join(mysekitei.tags_order[:mysekitei.n_features]), '\n\n'

        for c in classes:
            hist.append(len([p for p in py if p == c]))
            print c, ':', hist[-1]
            print >>f, c, ':', hist[-1]


    # regexp = mysekitei.get_regexp(features)
    re_s = []

    return re_s


def run2(good_urls, urls, re_s):
    # quality of clusterization
    pass




if __name__ == "__main__":

    with open('data/urls.kinopoisk.examined.txt', 'r') as f:
        good_urls = f.readlines()

    with open('data/urls.kinopoisk.general.txt', 'r') as f:
        urls = f.readlines()

    good_urls = [ re.sub(ur'\r?\n', u'', url.lower()) for url in good_urls ]
    urls      = [ re.sub(ur'\r?\n', u'', url.lower()) for url in urls ]

    re_s = run1(good_urls, urls, 2000) # , 10)

    with open('data/reg_expressions.txt', 'w') as out:
        out.write('\n'.join(re_s))

    # run2(good_urls, urls, re_s)