from sklearn.metrics import normalized_mutual_info_score  # """ ???????????????? ???????? ?????????? """
from sklearn.metrics import f1_score                      # """ F-???? """ ???
# from sklearn.metrics import b


class purity(object):
    """ Calculate the metrics of a quality
        of the clusterization for a site
    """
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


    def urls_quantity(self, k, N, a):        
        N_fact = math.factorial(N)
        return sum( map( lambda i: math.pow(a,i) * math.pow(1-a, N-i) * N_fact / (math.factorial(i) * math.factorial(N-i)), range(k) ))

