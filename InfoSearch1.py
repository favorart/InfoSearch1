import numpy as np
import random
import math
import sys
import io
import os
import re

from sekitei import sekitei
from cluster import find_clusters

def run1(good_urls, urls, n_urls=500, n_features=15):
    # random.shuffle(good_urls)
    # random.shuffle(urls)

    fit_urls = good_urls[:n_urls] + urls[:n_urls]
    # random.shuffle(fit_urls)

    mysekitei = sekitei(fit_urls)
    y = [1] * n_urls + [0] * n_urls
    print len(y), y
    mysekitei.fit()    
    X = mysekitei.most_freq_features(n_features)
    # P = 

    # find_clusters(X,y,P)

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

    re_s = run1(good_urls, urls, 10)

    with open('data/reg_expressions.txt', 'w') as out:
        out.write('\n'.join(re_s))

    # run2(good_urls, urls, re_s)