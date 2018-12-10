""" compute knn accuracy """

import pickle
import numpy as np

y_test = np.array(pickle.load(open('data/test_labels.data', 'rb')))

# reduced
dist1 = np.genfromtxt('dis/train_test_dis_array.txt', delimiter=',')
y_train1 = np.genfromtxt('data/reduced_train_label.txt')

# reduced scaled
dist2 = np.genfromtxt('dis/train_test_dis_array_scaled.txt', delimiter=',')
y_train2 = np.genfromtxt('data/reduced_train_label_scaled.txt')

# scaled
#dist3 = np.genfromtxt('dis/train_test_dis_array_scaled_no_reduce.txt', delimiter=',')
#y_train3 = np.genfromtxt('data/train_labels.txt')


def knn_accuracy(y_train, y_test, dist, ks):
    sortedind = dist1.argsort(axis=0)
    # majority vote
    for k in ks:
        count = 0
        for i in range(y_test.size):
            knearest = sortedind[:k, i]
            y_pred = np.bincount(y_train[knearest]).argmax()
            if y_pred == y_test[i]:
                count += 1
        print("k={0}, accuracy={1}%".format(k, count/y_test.size))

if __name__ == '__main__':
    ks = [1, 3, 5, 10, 30, 50, 100, 300]
    
    print("reduced:")
    knn_accuracy(y_train1, y_test, dist1, ks)