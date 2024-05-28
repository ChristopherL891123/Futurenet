# https://www.geeksforgeeks.org/saving-a-machine-learning-model/
import joblib 
import numpy as np 
from joblib import Parallel, delayed 
from sklearn.datasets import load_iris 
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier 

irisDataSet = load_iris() 
X = irisDataSet.data 
y = irisDataSet.target 
  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2024) 
  
knn = KNeighborsClassifier(n_neighbors=6) 
knn.fit(X_train, y_train) 

#serialize and deserialize using pickle(makes a pickle binary file)
joblib.dump(knn, 'serialize_test.pkl') 
serializedModel = joblib.load('serialize_test.pkl') 
print(serializedModel.predict(X_test))