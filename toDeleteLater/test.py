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

_XX = XX[:60, :]
_y = y[: 60]

knn = KNeighborsClassifier(n_neighbors=1,
                    algorithm='brute',
                    metric=dp_rolling_ed)
from timeit import default_timer as timer

start = timer()

knn.fit(_XX, _y)

mid = timer()

pred = knn.predict(XX[-60:, :])

end = timer()

acuracy = (pred == y[-60:]).mean() * 100
print(f'acuracy = {int(acuracy)}%')
print(f'fit time elapsed = {mid - start}s')
print(f'predict time elapsed = {end - mid}s')
