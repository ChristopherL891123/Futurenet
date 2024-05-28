import datetime
import hashlib
import json
import os
import sys
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error

dataset = sys.argv[1]
target = sys.argv[2]
username = sys.argv[3]
directory = sys.argv[5]

os.chdir(directory)

df = pd.read_csv(dataset)
df = df.dropna(axis=1)
y = df[target]
X = df.drop(columns=[target])


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=99)

GradientBoostRegression = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=67)
GradientBoostRegression.fit(X_train, y_train)
predictions = GradientBoostRegression.predict(X_test)

mse = mean_squared_error(y_test, predictions)
print("Mean Squared Error: ", mse)

recordPath = os.path.join(directory, "models","model_record.json")


#serialize and deserialize using pickle(makes a pickle binary file)
with open(recordPath,'r') as f:
    modelRecord = json.load(f)
    f.close()

filename = "GradientBoostRegression"
serializedFile = f"{filename}_" + f"{modelRecord[username][filename]}" + ".pkl"

joblib.dump(GradientBoostRegression, os.path.join(directory, "models",serializedFile) ) 

with open(recordPath,'w') as f:
    json.dump(modelRecord,f)
    f.close()

logPath = os.path.join(directory,"downloadsLog.json")
if os.path.exists(logPath):
    with open(logPath, 'r') as file:
        logs = json.load(file)
else:
    logs = {}

if username not in logs:
    logs[username] = []

logs[username].append({
    "filename": serializedFile,
    "mse": mse,
    "f1":"none",
    "target": target,
    "dataset":dataset.split("\\")[-1],
    "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    "md5": hashlib.md5(serializedFile.encode()).hexdigest()

})

with open(logPath, 'w') as file:
    json.dump(logs, file, indent=4)