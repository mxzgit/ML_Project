import pickle
import numpy as np
from dp_rolling import dp_rolling_ed

from sklearn.neighbors import KNeighborsClassifier

X = pickle.load(open("train.data", "rb"))
X = np.array(X)

m = X.shape[0]
n = max([len(line) for line in X])

XX = -1 * np.ones((m,n))
for i in range(m):
    for j in range(n):
            if (len(X[i]) > j):
                XX[i, j] = X[i][j]


y = pickle.load(open("train_labels.data", "rb"))
y = np.array(y)

XX = XX[:600, :]
y = y[: 600]

knn = KNeighborsClassifier(n_neighbors=1,
                    algorithm='auto',
                    metric=dp_rolling_ed)

knn.fit(XX, y)
