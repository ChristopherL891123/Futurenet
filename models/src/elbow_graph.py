#https://stackoverflow.com/questions/76452322/how-to-dump-label-encoder-values-for-multiple-columns-in-a-dataframe
#https://www.geeksforgeeks.org/ml-label-encoding-of-datasets-in-python/
#https://medium.com/@kattilaxman4/a-practical-guide-for-python-label-encoding-with-python-fb0b0e7079c5
#https://codinginfinite.com/elbow-method-in-python-for-k-means-and-k-modes-clustering/
#https://www.geeksforgeeks.org/elbow-method-for-optimal-value-of-k-in-kmeans/
#https://juanitorduz.github.io/spectral_clustering/
#https://stats.stackexchange.com/questions/309402/how-to-find-the-optimal-number-of-clusters-for-spectral-clustering-using-similar
#https://towardsdatascience.com/spectral-graph-clustering-and-optimal-number-of-clusters-estimation-32704189afbe
#https://medium.com/@guava1427/optimal-number-of-clusters-for-spectral-clustering-67037cf8a348

import json
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import LabelEncoder
from kmodes.kmodes import KModes
import pandas as pd
import os



dataset = sys.argv[1]
model = sys.argv[2]
username = sys.argv[3]
directory = sys.argv[4] # in this file, it is 4 not 5

os.chdir(os.path.join(directory,"models","src"))


df = pd.read_csv(dataset)
K = list(range(1,5))
if model == "KMeans":
    inertiaList = []
    for i in K:
        KMeans = KMeans(n_clusters=i)
        KMeans.fit(df)
        inertiaList.append(KMeans.inertia_)

    plt.plot(K, inertiaList, marker='o')
    plt.title("Elbow Method for KMeans")
    plt.xlabel("Clusters")
    plt.ylabel("Cost")
    plt.grid(True)
    plt.savefig("KMeans_elbow.png")
    plt.close()

if model == "KModes":
    
    labelEncoders = {}
    for column in df.columns:
        labelEncoders[column] = LabelEncoder()
        df[column] = labelEncoders[column].fit_transform(df[column])

    cost = []
    for i in K:
        KModes = KModes(n_clusters=i)
        KModes.fit_predict(df)
        cost.append(KModes.cost_)
    
    plt.plot(K, cost, '-o', marker='o')
    plt.title("Elbow Method For KModes")
    plt.xlabel("Clusters")
    plt.ylabel("Cost")
    plt.grid(True)
    plt.savefig("KModes_elbow.png")
    plt.close()

if model == "SpectralClustering":
    silhouetteScores = []
    K = list(range(2,11))
    for i in K:
        spectral = SpectralClustering(n_clusters=i)
        labels = spectral.fit_predict(df)
        silhouetteAvg = silhouette_score(df, labels)
        silhouetteScores.append(silhouetteAvg)

    plt.plot(K, silhouetteScores, marker='o')
    plt.title("Elbow Method for Spectral Clustering")
    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Score")
    plt.savefig("SpectralClustering_elbow.png")
    plt.close()
