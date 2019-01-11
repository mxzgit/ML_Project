
import pickle
import numpy as np
from pylmnn import LargeMarginNearestNeighbor as LMNN

csv = np.genfromtxt("data/numerical_train.csv", delimiter=',')
n, d = csv.shape

X_train = csv[:,:d-1]
y_train = csv[:,-1]

k_train, n_components, max_iter = 7, d, 180

lmnn = LMNN(n_neighbors=k_train, max_iter=max_iter, n_components=n_components)

print('learning the metric...')

# Train the metric learner
lmnn.fit(X_train, y_train)

X_train_transformed = lmnn.transform(X_train)

pickle.dump(X_train_transformed, open("data/numerical_train_transformed.pkl", 'wb'))
pickle.dump(y_train, open("data/numerical_train_labels.pkl", 'wb'))

print('done!')