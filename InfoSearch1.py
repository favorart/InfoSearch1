import numpy as np
import math
import sys
import io
import os
import re

from dbscan import dbscan
from sklearn.cluster.dbscan_ import DBSCAN
from sklearn.metrics import normalized_mutual_info_score  # """ ���������������? �������� ���������� """
from sklearn.metrics import f1_score                      # """ F-���� """ ???
# from sklearn.metrics import b


class purity(object):
    """ The estimation is the clearence of a cluster
        with bootstrepping (averaging by random selections)
    """
    def __init__(self, n_bootstreping):
        self.n_bootstreping = n_bootstreping
        self.tags = set()

    def calc(self, clusters, classes):
        result = 0.
        for i in xrange(self.n_bootstreping):
            result += [ max(len(clr in cls)) for clr,cls in clusters, clusses ]
            result *= 1. / len(clusters)
        return  1. / n_bootstreping * result


class sekitei(object):
    """ Calculate the metrics of a quality
        of the clusterization for a site
    """
    def __init__(self, clusters, classes):
        self.clusters = clusters
        self.classes = classes

    def urls_quantity(self, k, N, a):        
        N_fact = math.factorial(N)
        return sum( map( lambda i: math.pow(a,i) * math.pow(1-a, N-i) * N_fact / (math.factorial(i) * math.factorial(N-i)), range(k) ))

    def get_features(self, url):
        """
        :param url:
        :type url: str
        """
        url = url.replace('https?://','').replace('www.','').lower()
        
        features = []
        # 1. The quantity of path segments
        segments = url.split('\\')[1:]
        features.append(len(segments))
        
        # 2. The list of query parametes' names
        params = url.split('?')[1].split('&')
        features.append(len(params))
        # names = params.split('=')[::2]
        # features.append(names)
                        
        # 3. The pair 'name=value' of query parameter's
        features.append(params)
        set(self.tags).add(params)

        # 4. (a) exact string segment
        features.append(segments)
        set(self.tags).add(segments)

        # 4. (b) string accurate within digits
        num_segments = [ re.sub(r'[0-9]+', '[0-9]+', s) for s in segments if s.isdigit() ]
        features.append(num_segments)
        set(self.tags).add(num_segments)

        # 4. (c) .extension
        ext_segments = [ "[^/]+\\" + s[s.rfind('.'):] for s in segments if s.rfind('.') != -1 ]
        features.append(ext_segments)
        set(self.tags).add(ext_segments)

        # 4. (d) (b)-(c) combination
        # features.append() # ???
        # set(self.tags).add(ext_segments)
        return features

        def get_regexp(self, features):
            """
            :param features:
            :type features: list
            """
            regexp = ""
            return regexp

        def get_X(self, all_features):

            X = np.array()
            for features in all_features:
                sample = np.array([] * len(tags))

                for i,tag in enumerate(tags):
                    if tag in features[2] + features[3] + features[4]:
                        sample[i] += 1
                sample += [features[0], features[1]]  # len segments and len params
                X.append(sample)
            return


def find_clusters(X,y):
    # clusterization
    make_clusters = dbscan(2, 0.1) # parameters
    make_clstrs = DBSCAN()
    return


def run1(good_urls, urls):
    filter = sekitei()
    print good_urls[:10]

    features = filter.get_features("url")
    regexp = filter.get_regexp(features)

    re_s = []

    return re_s

def run2(good_urls, urls, re_s):
    # quality of clusterization
    pass


if __name__ == "__main__":
    with io.open("data/urls.kinopoisk.examined.txt") as input:
        good_urls = input.readlines()

    with io.open("data/urls.kinopoisk.general.txt") as input:
        urls = input.readlines()

    re_s = run1(good_urls, urls)

    with io.open("data/reg_expressions.txt") as output:
        output.write("\n".join(re_s))

    # run2(good_urls, urls, re_s)