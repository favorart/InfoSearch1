from collections import defaultdict
import numpy as np
import math
import sys
import io
import os
import re
import json


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

    def __init__(self, urls):
        self.urls = np.array(urls)
        self.tags = set(["/segments", "/params"])
        self.tags_order = []
        self.re_digit = re.compile('\d')
        self.n_features = -1

    def contains_digit(self, string):
        return (self.re_digit.search(string) is not None)

    def get_features_from_url(self, url):
        """ Get features from URL
            :type param url: str
        """
        url = re.sub(ur'(^https?://(www.)?)|(/$)', u'', url).split('?')
        url, params = url[0], url[1:]

        features = defaultdict(int)
        # 1. The quantity of path segments
        segments = url.split('/')[1:] # throw away the domain
        features["/segments"] = len(segments)

        # 2. The list of query parametes' names
        if (params):
            params = params[0].split('&')
            features["/params"] = len(params)
                                    
            # 3. The pair 'name=value' of query parameter's
            self.tags.update(params)
            features .update({ p:1 for p in params })
        else: features["/params"] = 0

        # 4. (a) exact string segment
        for i,s in enumerate(segments):
            self.tags.add((i,s))
            features[(i,s)] = 1

        # 4. (b) string accurate within digits
        num_iseg = {(i, re.sub(ur'[0-9]+', u'[0-9]+', seg)) : 1  for i,seg in enumerate(segments) if self.contains_digit(seg) }
        if (num_iseg):
            self.tags.update(num_iseg.keys())
            features .update(num_iseg)

        # 4. (c) .extension
        match = re.search(ur'.*(\..+)$', segments[-1])
        if match is not None:
            ext_segment = ( len(segments)-1, ur'[^/]+' + match.group(1) )  # ???
            self.tags.update(  [ext_segment] )
            features .update({ ext_segment : 1 })

        # 4. (d) combination of (b)-(c) points
        if self.contains_digit(segments[-1]) and match is not None:
            feat = ( len(segments)-1, re.sub(ur'[0-9]+', u'[0-9]+', segments[-1]), ur'[^/]+'+match.group(1) )  # ???
            self.tags.update(  [feat]  )
            features .update({ feat : 1 })

        return features

    def fit(self):
        """ Get features matrix X """
        all_features = []
        for url in self.urls:
            all_features.append( self.get_features_from_url(url) )

        self.X = np.zeros( (len(self.urls), len(self.tags)) )
        self.tags_order = np.array(list(self.tags))

        for i in range(len(self.urls)):            
            for j,tag in enumerate(self.tags_order):
                self.X[i][j] = all_features[i][tag]

    def most_freq_features(self, n_features):
        """ """
        self.tags_order = self.tags_order.reshape( (len(self.tags), 1) )
        self.X = np.concatenate( (self.X.T, self.tags_order), axis=1)

        self.X = np.array(sorted(self.X, key=lambda entry: len([ x for x in entry if type(x) is float and x != 0. ]), reverse=True))
        
        self.tags_order = self.X[-1]
        self.X = self.X[:-1]
        self.X = self.X.T

        self.n_features = n_features
         
        return self.X[0::, 0:self.n_features:]

    def make_P(self, urls):
        n = self.n_features if self.n_features > 0 else len(self.tags_order)
        P = np.zeros( (len(urls), n) )

        for j,tag in enumerate(self.tags_order[:n]):
            for i,url in enumerate(urls):
                url = re.sub(ur'(^https?://(www.)?)|(/$)', u'', url).split('?')
                url, params = url[0], url[1:] # split params
                segments = url.split('/')[1:] # throw off domains

                if type(tag) == tuple:
                    if   len(tag) == 2 and re.search(tag[1], segments[tag[0]]):
                        P[i][j] == 1
                    elif len(tag) == 3 and re.search(tag[1], segments[tag[0]]) \
                                       and re.search(tag[2], segments[tag[0]]):
                        P[i][j] = 1
                elif type(tag) == str:
                    if '/segments':
                        P[i][j] = len(segments)
                    else: # '/params'
                        params = params[0].split('&')
                        P[i][j] = len(params)
        return P

    def get_regexp(self, cluster):
        """ :type param cluster: matrix """
        regexp = ''
        return regexp
