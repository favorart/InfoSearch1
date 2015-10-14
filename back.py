#import numpy as np
#import math
#import sys
#import io
#import os
#import re
#from collections import defaultdict


#def m():
#    a = np.array([[0,0,1.0],[0,0,1,0],[0,1,0,1],[1,1,1,0]]); 
#    a = np.array(sorted(a, key=lambda entry: len([ x for x in entry if x != 0 ]), reverse=True))
#    print  a # [:, :2]


#class sekitei(object):
    #""" Description of agorithm:

    #    >> Разберём пример иллюстрирующий работу алгоритма секетеи.
    #    >> http://kinopoisk.ru/afisha/people_2725199.xml?myafisha=45&ok=True

    #    >> afisha/people_2725199.xml?myafisha=45&ok=True
    #    >> 1. "2" сегмента
    #    >> 2. "2" параметра          X( "myafisha", "ok" )
    #    >> 3. "myafisha=45", "ok=True"   - Фича - это пара(ключ-значение)
    #    >> 4. (а) (0, "afisha"), (1, "people_2725199.xml")
    #    >>    Фичи: "afisha на позиции 0", "people_2725199.xml"
    #    >>    (b) (1, "people_\d+\.xml")
    #    >>    (c) (1, "[^/]+\.xml")
    #    >>    (d) (1, "people_\d+" + "\.xml") - это фича  """ # !!!
#    """
#    def __init__(self, urls):
#        self.urls = np.array(urls)
#        self.tags = set()
#        self.X = np.matrix([])
#        self.tags.add(["/segments", "/params"])
#        self.re_digit = re.compile('\d')

#    def contains_digit(self, string):
#        return self.re_digit.search(string)

#    def get_features_from_url(self, url):
#        """ get_features_from_url
#        :param url:
#        :type url: str
#        """
#        url = url.replace('https?://','').replace('www.','').lower()

#        # features = []
#        features = defaultdict()
#        # 1. The quantity of path segments
#        segments = url.split('/')[1:] # throw away the domain
#        # features.append(len(segments))
#        features["/segments"] = len(segments)
        
#        # 2. The list of query parametes' names
#        params = url.split('?')[1].split('&')
#        # features.append(len(params))
#        features["/params"] = len(params)
#        # names = params.split('=')[::2]
#        # features.append(names)
                        
#        # 3. The pair 'name=value' of query parameter's
#        # features.append(params)
#        self.tags.add(params)
#        for p in params: features[p] += 1        

#        # 4. (a) exact string segment
#        # features.append(segments)
#        for i,s in enumerate(segments):
#            self.tags.add((i,s))
#            features[(i,s)] += 1 

#        # 4. (b) string accurate within digits
#        # [ (i, re.sub(r'[0-9]+', '[0-9]+', s)) for i,seg in enumerate(segments) if any(c.isdigit() for c in seg) ]
#        num_seg_tuples = [ (i, seg) for i,seg in enumerate(segments) if self.contains_digit(seg) ]
#        # features.append(num_seg_tuples)
#        self.tags.add(num_seg_tuples)
#        for tup in num_seg_tuples: features[tup] += 1

#        # 4. (c) .extension
#        ext_segments = [ "[^/]+\\" + s[s.rfind('.'):] for s in segments if s.rfind('.') != -1 ]
#        features.append(ext_segments)
#        self.tags.add(ext_segments)

#        # 4. (d) (b)-(c) combination
#        # features.append() # ???
#        # set(self.tags).add(ext_segments)
#        return features

#        def get_regexp(self, features):
#            """
#            :param features:
#            :type features: list
#            """
#            regexp = ""
#            return regexp

#        def get_X(self, all_features):
#            for features in all_features:
#                sample = np.array([] * len(tags))

#                for i,tag in enumerate(tags):
#                    if tag in features[2] + features[3] + features[4]:
#                        sample[i] += 1
#                sample += [features[0], features[1]]  # len segments and len params
#                self.X.append(sample)
#            return self.X

