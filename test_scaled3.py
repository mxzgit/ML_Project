import pickle
import numpy as np
from dp_rolling import dp_rolling_ed

from sklearn.neighbors import KNeighborsClassifier

X_train = pickle.load(open("train_code_scaled_half.data", "rb"))
X_train = np.array(X_train)

X_test = pickle.load(open("test_code_scaled_half.data", "rb"))
X_test = np.array(X_test)

m_train = X_train.shape[0]
m_test = X_test.shape[0]

n = max(max([len(line) for line in X_train]),max([len(line) for line in X_test])) 

X_train_array = -1 * np.ones((m_train,n))
X_test_array = -1 * np.ones((m_test,n))

for i in range(m_train):
    for j in range(n):
            if (len(X_train[i]) > j):
                X_train_array[i, j] = X_train[i][j]

for i in range(m_test):
    for j in range(n):
            if (len(X_test[i]) > j):
                X_test_array[i, j] = X_test[i][j]

Y_train = pickle.load(open("train_labels.data", "rb"))
Y_train = np.array(Y_train)

Y_test = pickle.load(open("test_labels.data", "rb"))
Y_test = np.array(Y_test)

ind = []
f = open('res.out', 'r')
for line in f:
      ind.append(int(line))

X_train_reduced = X_train_array[ind]
Y_train_reduced = Y_train[ind]

print(len(X_train_reduced))
print(len(Y_train_reduced))

print(len(X_test_array))
print(len(Y_test))

nnarr = [50,200,1000]
from timeit import default_timer as timer
import sys

for nn in nnarr:
	knn = KNeighborsClassifier(n_neighbors=nn,
						algorithm='brute',
						metric=dp_rolling_ed)
	
	start = timer()
	knn.fit(X_train_reduced, Y_train_reduced)
	mid = timer()
	pred = knn.predict(X_test_array)
	end = timer()
	acuracy = (pred == Y_test).mean() * 100
	print(f'acuracy = {int(acuracy)}%')
	print(f'fit time elapsed = {mid - start}s')
	print(f'predict time elapsed = {end - mid}s')
	sys.stdout.flush()