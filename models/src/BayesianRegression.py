# Bello_Maria_Lama_Christopher_DS_project.ipynb
#https://www.geeksforgeeks.org/md5-hash-python/
#https://www.simplilearn.com/tutorials/data-science-tutorial/bayesian-linear-regression#:~:text=What%20does%20Bayesian%20regression%20do,value%20of%20the%20model%20parameters.
# https://towardsdatascience.com/introduction-to-bayesian-linear-regression-e66e60791ea7
#https://towardsdatascience.com/introduction-to-bayesian-linear-regression-e66e60791ea7


import datetime
import hashlib
import json
import os
import sys
import joblib
from sklearn import linear_model
from sklearn.impute import SimpleImputer
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

dataset = sys.argv[1]
target = sys.argv[2]
username = sys.argv[3]
directory = sys.argv[5]

os.chdir(directory)

df = pd.read_csv(dataset)
df = df.dropna()

X = df.drop(columns=[target])
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=38)

BayesianRegression = linear_model.BayesianRidge()
BayesianRegression.fit(X, y)
yPred = BayesianRegression.predict(X_test)

mse = mean_squared_error(y_test, yPred)

recordPath = os.path.join(directory, "models","model_record.json")

with open(recordPath,'r') as f:
    modelRecord = json.load(f)
    f.close()

filename = "BayesianRegression"
serializedFile = "BayesianRegression_" + f"{modelRecord[username][filename]}" + ".pkl"

joblib.dump(BayesianRegression, os.path.join(directory, "models",serializedFile) )


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
    "mse": mse,
    "f1": "none",
    "target": target,
    "dataset": dataset.split("\\")[-1],
    "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
    "md5": hashlib.md5(serializedFile.encode()).hexdigest()
})

with open(logPath, 'w') as file:
    json.dump(logs, file, indent=4)
    file.close()
