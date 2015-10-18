from collections import defaultdict
import numpy as np
import math
import json
import sys
import io
import os
import re
import random


class sekitei(object):
    """ Description of agorithm:

        >> Разберём пример иллюстрирующий работу алгоритма секетеи.
        >> http://kinopoisk.ru/afisha/people_2725199.xml?myafisha=45&ok=True

        >> afisha/people_2725199.xml?myafisha=45&ok=True
        >> 1. "2" сегмента
        >> 2. "2" параметра          X( "myafisha", "ok" )
        >> 3. "myafisha=45", "ok=True"   - Фича - это пара(ключ-значение)
        >> 4. (а) (0, "afisha"), (1, "people_2725199.xml")
        >>    Фичи: "afisha на позиции 0", "people_2725199.xml"
        >>    (b) (1, "people_\d+\.xml")
        >>    (c) (1, "[^/]+\.xml")
        >>    (d) (1, "people_\d+", "\.xml") - это фича  """

    def __init__(self, urls, alpha=0.1):
        """ """
        self.alpha = alpha
        self.N = len(urls)
        self.urls = np.array(urls)
        self.tags = set()
        self.tags_order = []
        self.n_tags = -1
        self.re_digit = re.compile('\d')

    def contains_digit(self, string):
        """ Return  bool """
        return (self.re_digit.search(string) is not None)

    def get_features_from_url(self, url, check=False, verbose=False):
        """ Get features from URL
            :type param url: str
        """
        url = re.sub(ur'(^https?://(www.)?)|(/$)', u'', url.lower())
        myurl = re.escape(url)
        myurl = re.sub(ur'(\\){1,2}([^.*+$|()\\^])', ur'\2', myurl).split('?') # re.sub(ur'([.*+$|()\^])', ur'\\\1', url).split('\?')
        if (verbose): print url
        myurl, params = myurl[0], myurl[1:]

        features = []
        # 1. The quantity of path segments
        segments = myurl.split('/')[1:] # throw away the domain
        if (verbose): print segments, params

        j = (len(segments) - 1)
        feat = ur'^[^/]+' + (ur'(/[^/]+){' + str(j) + ur'}' if j else ur'') + ur'$'
        if (verbose): print feat
        features.append(feat)

        # 2. The list of query parametes' names
        if (params):
            params = params[0].split('&')
            
            j = (len(params) - 1)
            feat = ur'^[^?&]+[?][^?&]+' + (ur'(&[^?&]+){' + str(j) + ur'}' if j else ur'') + ur'$'
            if (verbose): print feat
            features.append(feat)

            if (verbose): print
            for i,par in enumerate(params):
                # position
                # feat = ur'^[^?&]+[?]' + ur'[^?&]+&' * i + par + ur'&[^?&]+' * (len(params) - i - 1) + ur'.*$'
                feat = ur'^[^?&]+[?](.*&)?' + par + ur'(&.*)?$'
                if (verbose): print feat
                features.append(feat)
        else:
            feat = ur'^[^?&]+$'
            if (verbose): print feat
            features.append(feat)

        if (verbose): print
        # 4. (a) exact string segment
        for i,seg in enumerate(segments):
            feat = ur'^' + (ur'([^/]+/){' + str(i) + ur'}' if i else ur'') + seg + ur'.*$'
            if (verbose): print feat
            features.append(feat)

        if (verbose): print
        # 4. (b) string accurate within digits
        for i,seg in enumerate(segments):
            if self.contains_digit(seg):
                feat = ur'^' + (ur'([^/]+/){' + str(i) + ur'}' if i else ur'') + re.sub(ur'[0-9]+', ur'[0-9]+', seg) + ur'.*$'
                if (verbose): print feat
                features.append(feat)

        if (verbose): print '\n', segments[-1]
        # 4. (c) .extension
        match_ext = re.search(ur'.*(\\\.[a-z]+)$', segments[-1])
        if match_ext is not None:
            feat = ur'^[^?&]+' + match_ext.group(1) + ur'([?].+)?$'
            if (verbose): print feat
            features.append(feat)

        if (verbose): print
        # 4. (d) combination of (b)-(c) points
        url_ = '/'.join(segments)
        if self.contains_digit(url_) and match_ext is not None:
            segs = re.sub(ur'[0-9]+', u'[0-9]+', re.sub(ur'[^/0-9]+', ur'[^/]+', url_.split('\\.')[0] ))
            j = (len(segments) - 1)
            feat = ur'^' + segs + match_ext.group(1) + ur'.*$'
            if (verbose): print feat
            features.append(feat)

        if (check):
            # THE CHECK
            url = url.split('/',1)[1] # throw away the domain
            print '\n', url
            for feat in features:
                if re.search(feat, url) is None:
                    print 'ERROR:', feat

        self.tags.update(features)
        return set(features)

    def fit(self):
        """ Get features matrix X """
        all_features = []
        for url in self.urls:
            all_features.append( self.get_features_from_url(url) )

        self.X = np.zeros( (len(self.urls), len(self.tags)), dtype=int)
        self.tags_order = np.array(list(self.tags))

        for i in range(len(self.urls)):            
            for j,tag in enumerate(self.tags_order):
                self.X[i][j] = 1 if (tag in all_features[i]) else 0

    def most_freq_features(self):
        """ Resurm sum-matrix X """
        # self.tags_order = self.tags_order.reshape( (len(self.tags), 1) )
        # self.X = np.concatenate( (self.X.T, self.tags_order), axis=1 )
        Y = [ (x, tag) for x,tag in zip(self.X.T, self.tags_order) ]
        Y = sorted(Y, key=lambda y: sum(y[0]), reverse=True)
        self.X, self.tags_order = np.array([ [ x for x in y[0] ] for y in Y ]).T, [ y[-1] for y in Y ]
        self.n_features = len([ x for x in self.X.sum(axis=0) if x >= (self.alpha * self.N) ])
        return self.X[0::, :self.n_features:]

    def matrix_of_existing_features(self, new_urls):
        """ Return binary matrix X for new urls """
        n = self.n_features if (self.n_features > 0) else len(self.tags_order)
        X = np.zeros( (len(new_urls), n) )

        for j,tag in enumerate(self.tags_order[:n]):
            for i,url in enumerate(new_urls):
                # Throw away the domain and protocol from url
                url = re.sub(ur'(^https?://(www.)?)|(/$)', u'', url).split('/', 1)[1]
                X[i][j] = 1 if (re.search(tag, url) is not None) else 0
        return X

    def get_regexp(self, X, y):
        """ :type param cluster: matrix """
        classes = list(set(y))
        print classes, '\n\n'
        
        feat_all_freq = np.array(X.sum(axis=0), dtype=float)
        indeces = [ [ i for i,res in enumerate(y) if res == c ] for c in classes ]
        feat_cls_freq = np.array([ X[i].sum(axis=0) for i in indeces ], dtype=float)

        print feat_all_freq, '\n'
        print [ feat / feat_all_freq for feat in feat_cls_freq], '\n'
            
        regexpes = {}
        for c,feat in zip(classes, feat_cls_freq):
            regexpes[c] = [ self.tags_order[i] for i,n in enumerate(feat / feat_all_freq) if n > 0. ]
        return regexpes
