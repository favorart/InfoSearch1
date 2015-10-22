from sklearn.manifold import TSNE
from matplotlib import pyplot

import matplotlib as plt
import numpy as np
import sys


def vizualize_clusters(X, y, py, hist=None):
    """ Using T-SNE to visualize the site clusters.
        Plot and save the scatter (and the histogramm).
    """
    model = TSNE(n_components=2, random_state=0)
    
    fig  = model.fit_transform(X,y)
    fig1 = model.fit_transform(X,py)

    pyplot.figure(figsize=(16, 8))
    pyplot.subplot(121)

    classes = list(set(y))
    for c,color in zip(classes, plt.colors.cnames.iteritems()):
        indeces = [ i for i,p in enumerate(y) if p == c ] 
        pyplot.scatter(fig[indeces, 0], fig[indeces, 1], marker='o', c=color[0])

    pyplot.subplot(122)

    clusters = list(set(py))
    for c,color in zip(clusters, plt.colors.cnames.iteritems()):
        indeces = [ i for i,p in enumerate(py) if p == c ] 
        pyplot.scatter(fig1[indeces, 0], fig1[indeces, 1], marker='o', c=color[0])

    # pyplot.show()
    pyplot.savefig('clusters' + '_scatter.png')

    if hist is not None:
        pyplot.figure(figsize=(4, 4))
        pyplot.xticks(clusters)

        pyplot.bar(clusters, hist, align='center')
        # pyplot.show()
        pyplot.savefig('clusters' + '_hist.png')

    print 'plot done'

