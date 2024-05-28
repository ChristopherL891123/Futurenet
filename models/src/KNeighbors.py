# https://www.geeksforgeeks.org/saving-a-machine-learning-model/
import datetime
import hashlib
import json
import os
import sys
import joblib 
import numpy as np 
from joblib import Parallel, delayed 
import pandas as pd
from sklearn.datasets import load_iris 
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier 

dataset = sys.argv[1]
target = sys.argv[2]
username = sys.argv[3]
directory = sys.argv[5]

os.chdir(directory)

df = pd.read_csv(dataset)
df = df.dropna(axis=1)
X = df.drop(columns=[target])
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2024) 
  
KNeighbors = KNeighborsClassifier(n_neighbors=6) 
KNeighbors.fit(X_train, y_train) 
yPred = KNeighbors.predict(X_test)

f1 = f1_score(y_test, yPred)

#serialize and deserialize using pickle(makes a pickle binary file)
recordPath = os.path.join(directory, "models","model_record.json")

with open(recordPath,'r') as f:
    modelRecord = json.load(f)
    f.close()

filename = "KNeighbors"
serializedFile = "KNeighbors_" + f"{modelRecord[username][filename]}" + ".pkl"

joblib.dump(KNeighbors, os.path.join(directory, "models",serializedFile)) 


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
    "f1":f1,
    "target": target,
    "dataset":dataset.split("\\")[-1],
    "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    "md5": hashlib.md5(serializedFile.encode()).hexdigest()

})

with open(logPath, 'w') as file:
    json.dump(logs, file, indent=4)