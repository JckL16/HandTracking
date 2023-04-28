import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import confusion_matrix, accuracy_score


dataset = pd.read_csv('Data.csv')

x = pd.DataFrame(dataset.iloc[:, 1:].values)
y = dataset.iloc[:, 0].values

#print(x)
#print(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

#print(x_train.shape)

classifier = Sequential()

#classifier.add(Dense(output_dim = 6, init = 'uniform', activation = 'relu', input_dim = 23))
classifier.add(Dense(6, activation='relu', kernel_initializer='glorot_uniform',input_dim=23))

#classifier.add(Dense(output_dim = 6, init = 'uniform', activation = 'relu'))
classifier.add(Dense(6, activation='relu', kernel_initializer='glorot_uniform',input_dim=23))


#classifier.add(Dense(output_dim = 1, init = 'uniform', activation = 'sigmoid'))
# classifier.add(Dense(6, output_dim = 1, activation = 'sigmoid'))


classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
classifier.fit(x_train, y_train, batch_size = 10)

y_pred = classifier.predict(x_test)
y_pred = (y_pred > 0.5)

cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test,y_pred)
