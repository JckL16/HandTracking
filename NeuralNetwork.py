
from keras import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv('Data.csv')

X = pd.DataFrame(dataset.iloc[:, 2:].values) # Ignorerar vilken han ändra
# X = pd.DataFrame(dataset.iloc[:, 1:].values) # Använder även vilken han det är om detta blir relevant
y = dataset.iloc[:, 0].values



from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)




n_features = X_train.shape[1]

print(X_train.shape)
print(y_train)

model = models.Sequential(layers=[
    ### hidden layer 1
    layers.Dense(input_dim=n_features,
                 units=int(round((n_features+1)/2)),
                 activation='softmax'),
    layers.Dropout(rate=0.2),

    ### layer output
    layers.Dense(units=1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(X_train, y_train, epochs=1000)
