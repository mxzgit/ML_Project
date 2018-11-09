#
# reduce the number of examples using Condensed nearest neighbors
#

import pickle
import numpy as np
from dp_rolling import dp_rolling_ed
from timeit import default_timer as timer


def condensedNN(X, y):
    m = len(X)
    storage = set()
    storage.add(0)
    dists = -1 * np.ones((m, m)) # memo
    converged = False
    while not converged:
        lastsize = len(storage)
        for i in range(len(X)):
            if i not in storage:
                predindex = -1
                mindist = -1
                
                for j in storage:
                    if dists[i, j] == -1:
                        dists[i, j] = dists[j, i] = dp_rolling_ed(X[i], X[j])
                    if mindist == -1 or mindist > dists[i, j]:
                        predindex = j
                        mindist = dists[i, j]

                if y[i] != y[predindex]:
                    storage.add(i)

        if lastsize == len(storage):
            converged = True

    return storage

if __name__ == "__main__":
    X = pickle.load(open("train.data", "rb"))
    X = np.array(X)

    y = pickle.load(open("train_labels.data", "rb"))
    y = np.array(y)

    size = 1000
    _X = X[:size]
    _y = y[:size]

    print(f"starting with size={size}!")
    start = timer()
    storage = condensedNN(_X, _y)
    print(f"finished with size={len(storage)}")
    print(f"time elapsed: {timer() - start}s")
