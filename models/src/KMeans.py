import datetime
import hashlib
import json
import os
import sys
import joblib
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import silhouette_score

dataset = sys.argv[1]
target = sys.argv[2]
username = sys.argv[3]
clusterNumber = int(sys.argv[4])
directory = sys.argv[5]

os.chdir(os.path.join(directory,"models"))

print(dataset)

df = pd.read_csv(dataset)

X = df.dropna()

kmeans = KMeans(n_clusters=clusterNumber)  
kmeans.fit(X)


X["Cluster"] = kmeans.labels_
df["Cluster"] = X["Cluster"]
sihouletteScore = silhouette_score(df, df["Cluster"])


#serialize and deserialize using pickle(makes a pickle binary file)
recordPath = os.path.join(directory, "models","model_record.json")

with open(recordPath,'r') as f:
    modelRecord = json.load(f)
    f.close()

filename = "KMeans"
serializedFile = "KMeans_" + f"{modelRecord[username][filename]}.pkl"
serializedFileImage = "KMeans_" + f"{modelRecord[username][filename]}"

sns.countplot(x="Cluster", data=df)
plt.title("Distribution of Clusters")
plt.xlabel("Cluster")
plt.ylabel("Count")
plt.savefig(serializedFileImage)
plt.close()
joblib.dump(kmeans, os.path.join(directory, "models",serializedFile)) 

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
    "sihouette": sihouletteScore,
    "target": target,
    "dataset":dataset.split("\\")[-1],
    "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    "md5": hashlib.md5(serializedFile.encode()).hexdigest()

})

with open(logPath, 'w') as file:
    json.dump(logs, file, indent=4)