import datetime
import hashlib
import json
import os
import sys
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder


dataset = sys.argv[1]
target = sys.argv[2]
username = sys.argv[3]
directory = sys.argv[5]

os.chdir(os.path.join(directory,"models","src"))

df = pd.read_csv(dataset)
df.dropna(axis=1)

categoricalColumns = []
for column in df.columns:
    if df[column].dtype == "object":
        categoricalColumns.append(column)
df = pd.get_dummies(df, columns=categoricalColumns)

y = df[target]
X = df.drop(columns=[target])

labelEncoder = LabelEncoder()
yEncoded = labelEncoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, labelEncoder, test_size=0.2, random_state=42)

xgbClassifier = XGBClassifier()
xgbClassifier.fit(X_train, y_train)
yPred = xgbClassifier.predict(X_test)

f1 = f1_score(y_test, yPred)


#serialize and deserialize using pickle(makes a pickle binary file)
recordPath = os.path.join(directory, "models","model_record.json")

with open(recordPath,'r') as f:
    modelRecord = json.load(f)
    f.close()

filename = "xgbClassifier"
serializedFile = "xgbClassifier" + f"{modelRecord[username][filename]}" + ".pkl"

joblib.dump(xgbClassifier, os.path.join(directory, "models",serializedFile)) 


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
