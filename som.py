import numpy as np
import sys

from sklearn.cluster.dbscan_ import DBSCAN
from dbscan import dbscan
from sekitei import sekitei


def som_save(P, py, full_urls, mysekitei, filename='Title'):
    """ """
    with open(filename + '.vec', 'w') as vec:
        print >>vec, '$XDIM %d\n$YDIM 1\n$VEC_DIM %d' % (len(P), mysekitei.n_features)
        print >>vec, '\n'.join([ ' '.join([str(e) for e in p]) + ' ' + url for (p,url) in zip(P, full_urls) ])

    with open(filename + '.cls', 'w') as cls:
        print >>cls, '\n'.join([ url + '\teval_' + str(c) for url,c in zip(full_urls,py) ])                
    
    with open(filename + '.tv', 'w') as tv:
        print >>tv, '$TYPE template\n$XDIM 2\n$YDIM 200\n$VEC_DIM %d' % (mysekitei.n_features)
        print >>tv, '\n'.join([ str(i) + ' ' + feat for i,feat in enumerate(mysekitei.tags_order[:mysekitei.n_features]) ])


def som_create_and_save(mysekitei, regexpes, good_urls, urls, som_classes_else_clusters=True, verbose=False):
    """ """
    full_urls = good_urls + urls
    if verbose: print  mysekitei.n_features, '\n'

    P = mysekitei.matrix_of_existing_features(full_urls)
    distrib  = mysekitei.distribute_among_clusters(P, regexpes)
    
    y = [1] * len(good_urls) + [0] * len(urls)
    som_save(P, y if som_classes_else_clusters else distrib, full_urls, mysekitei)

    if verbose: print 'som done'
    return
