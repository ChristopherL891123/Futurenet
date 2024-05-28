import os

print(os.getcwd())

import sys
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

print(os.getcwd())

dataset_path =  sys.argv[1] # "datasets/Thyroid_Diff.csv"
target_feature =  sys.argv[2] # "Risk"

df = pd.read_csv(dataset_path)

X = df.drop(columns=[target_feature])
y = df[target_feature]

label_encoders = {}
for column in X.select_dtypes(include=['object']).columns:
    label_encoders[column] = LabelEncoder()
    X[column] = label_encoders[column].fit_transform(X[column])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

nb_classifier = CategoricalNB()

nb_classifier.fit(X_train, y_train)

y_pred = nb_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

#serialize and deserialize using pickle(makes a pickle binary file)
with open("C:\\Users\\124ch\\Desktop\\CAPSTONE\\s24-capstone-project-ChristopherL891123\\misc\\retrain_test\\model_record.json",'r') as f:
    model_record = json.load(f)
    f.close()

filename = "NaiveBayesClassifier"

joblib.dump(nb_classifier, "C:\\Users\\124ch\\Desktop\\CAPSTONE\\s24-capstone-project-ChristopherL891123\\misc\\retrain_test\\uploads\\NaiveBayesClassifier_" + f"{model_record[filename]}" + ".pkl") 

# add one to that key

model_record[filename] += 1


with open("C:\\Users\\124ch\\Desktop\\CAPSTONE\\s24-capstone-project-ChristopherL891123\\misc\\retrain_test\\model_record.json",'w') as f:
    json.dump(model_record,f)
    f.close()