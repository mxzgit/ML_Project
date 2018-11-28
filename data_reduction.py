#
# reduce the number of examples using Condensed nearest neighbors
#

import pickle
import numpy as np
from dp_rolling import dp_rolling_ed
from timeit import default_timer as timer

def bayesianReduction(X, y, dists=None):
    m = len(X)
    if dists is None:
        dists = -1 * np.ones((m, m)) #memo

    np.random.seed(27)
    perm = np.random.permutation(m)
    S1 = set(perm[:m//2])
    S2 = set(perm[m//2:])
    converged = False
    while not converged:
        S1_oldsize = len(S1)
        S2_oldsize = len(S2) 

        # 1-NN classify S1 with S2
        for i in S1.copy():
            predindex = -1
            mindist = -1
            
            for j in S2:
                if dists[i, j] == -1:
                    dists[i, j] = dists[j, i] = dp_rolling_ed(X[i], X[j])
                if mindist == -1 or mindist > dists[i, j]:
                    predindex = j
                    mindist = dists[i, j]

            if y[i] != y[predindex]:
                S1.remove(i)
        
        # 1-NN classify S2 with S1
        for i in S2.copy():
            predindex = -1
            mindist = -1
            
            for j in S1:
                if dists[i, j] == -1:
                    dists[i, j] = dists[j, i] = dp_rolling_ed(X[i], X[j])
                if mindist == -1 or mindist > dists[i, j]:
                    predindex = j
                    mindist = dists[i, j]

            if y[i] != y[predindex]:
                S2.remove(i)
        
        if len(S1) == S1_oldsize and len(S2) == S2_oldsize:
            converged = True

    return sorted(S1.union(S2)), dists


def condensedNN(X, y, ind=None, dists=None):
    if ind is None:
        ind = range(len(X))
    m = len(ind)
    storage = set()
    storage.add(ind[0])
    if dists is None:
        dists = -1 * np.ones((m, m)) # memo
    converged = False
    while not converged:
        lastsize = len(storage)
        for i in ind:
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

    return sorted(storage), dists

if __name__ == "__main__":
    X = pickle.load(open("train.data", "rb"))
    X = np.array(X)

    y = pickle.load(open("train_labels.data", "rb"))
    y = np.array(y)

    size = 50
    _X = X[:size]
    _y = y[:size]

    print(f"starting with size={size}!")
    start = timer()
    ind, distMat = bayesianReduction(_X, _y)
    print(f"finished baysianReduction with size={len(ind)}")
    print(f"time elapsed: {timer() - start}s")
    start = timer()
    ind, distMat = condensedNN(_X, _y, ind=ind, dists=distMat)
    print(f"finished CNN with size={len(ind)}")
    print(f"time elapsed: {timer() - start}s")
    print("dumping reducted data...")
    X_reduct = _X[ind]
    y_reduct = _y[ind]
    pickle.dump(ind, open("train_reduct_ind.data", "wb"))
    pickle.dump(X_reduct, open("train_reduct.data", "wb"))
    pickle.dump(y_reduct, open("train_labels_reduct.data", "wb"))
    print("done.!")
