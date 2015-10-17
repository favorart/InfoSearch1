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

#=============================================================================================
# last

#class sekitei(object):
#    """ Description of agorithm:

#        >> Разберём пример иллюстрирующий работу алгоритма секетеи.
#        >> http://kinopoisk.ru/afisha/people_2725199.xml?myafisha=45&ok=True

#        >> afisha/people_2725199.xml?myafisha=45&ok=True
#        >> 1. "2" сегмента
#        >> 2. "2" параметра          X( "myafisha", "ok" )
#        >> 3. "myafisha=45", "ok=True"   - Фича - это пара(ключ-значение)
#        >> 4. (а) (0, "afisha"), (1, "people_2725199.xml")
#        >>    Фичи: "afisha на позиции 0", "people_2725199.xml"
#        >>    (b) (1, "people_\d+\.xml")
#        >>    (c) (1, "[^/]+\.xml")
#        >>    (d) (1, "people_\d+", "\.xml") - это фича  """

#    def __init__(self, urls):
#        self.urls = np.array(urls)
#        self.tags = set(["/segments", "/params"])
#        self.tags_order = []
#        self.re_digit = re.compile('\d')
#        self.n_features = -1

#    def contains_digit(self, string):
#        """ bool """
#        return (self.re_digit.search(string) is not None)

#    def get_features_from_url(self, url):
#        """ Get features from URL
#            :type param url: str
#        """
#        url = re.sub(ur'(^https?://(www.)?)|(/$)', u'', url.lower()).split('?')
#        url, params = url[0], url[1:]

#        features = defaultdict(int)
#        # 1. The quantity of path segments
#        segments = url.split('/')[1:] # throw away the domain
#        print segments, params

#        # features["/segments"] = len(segments)
#        feat = ur'^[^/]+' + ur'/[^/]+' * (len(segments) - 1) + ur'$'
#        print feat
#        features[feat] = 1
#        self.tags.add(feat)

#        # 2. The list of query parametes' names
#        if (params):
#            params = params[0].split('&')
#            # features["/params"] = len(params)
            
#            feat = ur'^[^?&]+[?][^?&]+' + ur'&[^?&]+' * (len(params) - 1) + ur'$'
#            print feat
#            self.tags.add(feat) 
#            features[feat] = 1
                                    
#            # 3. The pair 'name=value' of query parameter's
#            # self.tags.update(params)
#            # features .update({ p:1 for p in params })
#            for i,par in enumerate(params):
#                feat = ur'^[^?&]+[?]' + ur'[^?&]+&' * i + par  + ur'&[^?&]+' * (len(params) - i - 1) + ur'$'
#                print feat
#                self.tags.add(feat)
#                features[feat] = 1
#        else:
#            # features["/params"] = 0
#            feat = ur'^[^?&]+$'
#            print feat
#            self.tags.add(feat)
#            features[feat] = 1

#        # 4. (a) exact string segment
#        for i,seg in enumerate(segments):
#            feat = ur'^' + ur'[^/]+/' * i + seg + ur'.*$'
#            print feat
#            self.tags.add(feat)
#            features[feat] = 1
#            # self.tags.add((i,s))
#            # features[(i,s)] = 1

#        # 4. (b) string accurate within digits
#        # num_iseg = {(i, re.sub(ur'[0-9]+', u'[0-9]+', seg)) : 1  for i,seg in enumerate(segments) if self.contains_digit(seg) }
#        # if (num_iseg):
#        #     self.tags.update(num_iseg.keys())
#        #     features .update(num_iseg)

#        # 4. (b) string accurate within digits
#        for i,seg in enumerate(segments):
#            if self.contains_digit(seg):
#                feat = ur'^' + ur'[^/]+/' * i + re.sub(ur'[0-9]+', u'[0-9]+', seg) + ur'.*$'
#                print feat
#                self.tags.add(feat)
#                features[feat] = 1

#        # 4. (c) .extension
#        match = re.search(ur'.*(\.[a-z]+)$', segments[-1])
#        if match is not None:
#            ext_segment = ( len(segments)-1, ur'[^/]+' + match.group(1) )  # ???
#            self.tags.update(  [ext_segment] )
#            features .update({ ext_segment : 1 })

#        # 4. (d) combination of (b)-(c) points
#        if self.contains_digit(segments[-1]) and match is not None:
#            feat = ( len(segments)-1, re.sub(ur'[0-9]+', u'[0-9]+', segments[-1]), ur'[^/]+'+match.group(1) )  # ???
#            self.tags.update(  [feat]  )
#            features .update({ feat : 1 })

#        return features

#    def fit(self):
#        """ Get features matrix X """
#        all_features = []
#        for url in self.urls:
#            all_features.append( self.get_features_from_url(url) )

#        self.X = np.zeros( (len(self.urls), len(self.tags)) )
#        self.tags_order = np.array(list(self.tags))

#        for i in range(len(self.urls)):            
#            for j,tag in enumerate(self.tags_order):
#                self.X[i][j] = all_features[i][tag]

#    def most_freq_features(self, n_appearances):
#        """ """
#        self.tags_order = self.tags_order.reshape( (len(self.tags), 1) )
#        self.X = np.concatenate( (self.X.T, self.tags_order), axis=1)

#        self.X = np.array(sorted(self.X, key=lambda entry: len([ x for x in entry if type(x) is float and x != 0. ]), reverse=True))
        
#        self.tags_order = self.X[-1]
#        self.X = self.X[:-1]
#        self.X = self.X.T

#        self.n_features = n_features
         
#        return self.X[0::, 0:self.n_features:]

#    def make_P(self, urls):
#        n = self.n_features if self.n_features > 0 else len(self.tags_order)
#        P = np.zeros( (len(urls), n) )

#        for j,tag in enumerate(self.tags_order[:n]):
#            for i,url in enumerate(urls):
#                url = re.sub(ur'(^https?://(www.)?)|(/$)', u'', url).split('?')
#                url, params = url[0], url[1:] # split params
#                segments = url.split('/')[1:] # throw off domains

#                if type(tag) == tuple:
#                    if   len(tag) == 2 and re.search(tag[1], segments[tag[0]]):
#                        P[i][j] == 1
#                    elif len(tag) == 3 and re.search(tag[1], segments[tag[0]]) \
#                                       and re.search(tag[2], segments[tag[0]]):
#                        P[i][j] = 1
#                elif type(tag) == str:
#                    if '/segments':
#                        P[i][j] = len(segments)
#                    else: # '/params'
#                        params = params[0].split('&')
#                        P[i][j] = len(params)
#        return P

#    def get_regexp(self, cluster):
#        """ :type param cluster: matrix """
#        regexp = ''
#        return regexp
