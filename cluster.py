from dbscan import dbscan
from sklearn.cluster.dbscan_ import DBSCAN


def find_clusters(X, y, P):
    # clusterization
    make_clusters = dbscan(2, 0.1) # parameters
    make_clstrs = DBSCAN()

    make_clstrs.fit(X,y)
    make_clstrs.fit_predict(P)


    return
