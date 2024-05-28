import datetime
import hashlib
import json
import os
import sys
import joblib
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.cluster import SpectralClustering
from sklearn.manifold import TSNE
from sklearn.metrics import f1_score, pairwise_distances, silhouette_score
from sklearn.preprocessing import LabelEncoder

dataset = sys.argv[1]
target = sys.argv[2]
username = sys.argv[3]
clusterNumber = int(sys.argv[4])
directory = sys.argv[5]

os.chdir(os.path.join(directory,"models"))

df = pd.read_csv(dataset)

labelEncoders = {}
for column in df.columns:
    labelEncoders[column] = LabelEncoder()
    df[column] = labelEncoders[column].fit_transform(df[column])
encodedData = pd.get_dummies(df)

spectralClustering = SpectralClustering(n_clusters=clusterNumber)
clusters = spectralClustering.fit_predict(encodedData)

df["Cluster"] = clusters

sns.countplot(x="Cluster", data=df)
plt.title("Distribution of Clusters")
plt.xlabel("Cluster")
plt.ylabel('Count')

sihouetteScore = silhouette_score(encodedData, df["Cluster"])

#serialize and deserialize using pickle(makes a pickle binary file)
recordPath = os.path.join(directory, "models","model_record.json")

with open(recordPath,'r') as f:
    modelRecord = json.load(f)
    f.close()

filename = "SpectralClustering"
serializedFile = "SpectralClustering_" + f"{modelRecord[username][filename]}.pkl"
serializedFileImage = "SpectralClustering_" + f"{modelRecord[username][filename]}"

plt.savefig(serializedFileImage)
plt.close()

joblib.dump(spectralClustering, os.path.join(directory, "models",serializedFile)) 

with open(recordPath,'w') as f:
    json.dump(modelRecord,f)
    f.close()

logPath = os.path.join(directory, "models","downloadsLog.json")
if os.path.exists(logPath):
    with open(logPath, 'r') as file:
        logs = json.load(file)
else:
    logs = {}

if username not in logs:
    logs[username] = []

logs[username].append({
    "filename": serializedFile,
    "mse": "none",
    "f1":"none",
    "sihouette": sihouetteScore,
    "target": target,
    "dataset":dataset.split("\\")[-1],
    "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    "md5": hashlib.md5(serializedFile.encode()).hexdigest()

})

with open(logPath, 'w') as file:
    json.dump(logs, file, indent=4)