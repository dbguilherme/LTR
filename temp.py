from sklearn.cluster import KMeans
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances_argmin_min
X = np.array([[1, 2], [1, 4], [4, 2], [4, 4]])

#clustering = AgglomerativeClustering(n_clusters=1)

#clustering.fit(X)


kmeans = KMeans(n_clusters=1, random_state=0).fit(X)
kmeans.fit(X)
#print(clustering.labels_)
closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
print(kmeans.cluster_centers_)
print(X[closest])
