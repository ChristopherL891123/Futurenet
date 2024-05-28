import datetime
import hashlib
import sys
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score
import os

dataset = sys.argv[1]
target = sys.argv[2]
username = sys.argv[3]
directory = sys.argv[5]

os.chdir(directory)

print(dataset)

df = pd.read_csv(dataset)

X = df.drop(columns=[target])
y = df[target]

labelEncoders = {}
for column in X.select_dtypes(include=["object"]).columns:
    labelEncoders[column] = LabelEncoder()
    X[column] = labelEncoders[column].fit_transform(X[column])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

NaiveBayesClassifier = CategoricalNB()

NaiveBayesClassifier.fit(X_train, y_train)

yPred = NaiveBayesClassifier.predict(X_test)

f1 = f1_score(y_test, yPred)

accuracy = accuracy_score(y_test, yPred)
print("Accuracy:", accuracy)

#serialize and deserialize using pickle(makes a pickle binary file)
recordPath = os.path.join(directory, "models","model_record.json")

with open(recordPath,'r') as f:
    modelRecord = json.load(f)
    f.close()

filename = "NaiveBayesClassifier"
serializedFile = "NaiveBayesClassifier_" + f"{modelRecord[username][filename]}" + ".pkl"

joblib.dump(NaiveBayesClassifier, os.path.join(directory, "models",serializedFile)) 


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
