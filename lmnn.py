
import pickle
import numpy as np
from pylmnn import LargeMarginNearestNeighbor as LMNN

csv = np.genfromtxt("data/numerical_train.csv", delimiter=',')
csv_test = np.genfromtxt("data/numerical_test.csv", delimiter=',')
n, d = csv.shape

X_train = csv[:,:d-1]
y_train = csv[:,-1]


X_test = csv_test[:,:d-1]
y_test = csv_test[:,-1]


k_train, n_components, max_iter = 7, d-1, 180

lmnn = LMNN(n_neighbors=k_train, max_iter=max_iter, n_components=n_components)

print('learning the metric...')

# Train the metric learner
lmnn.fit(X_train, y_train)

X_train_transformed = lmnn.transform(X_train)
X_test_transformed = lmnn.transform(X_test)

pickle.dump(X_train_transformed, open("data/numerical_train_transformed.pkl", 'wb'))
pickle.dump(y_train, open("data/numerical_train_labels.pkl", 'wb'))
pickle.dump(X_test_transformed, open("data/numerical_test_transformed.pkl", 'wb'))
pickle.dump(y_test, open("data/numerical_test_labels.pkl", 'wb'))
pickle.dump(lmnn, open("data/lmnn.pkl", 'wb'))

print('done!')