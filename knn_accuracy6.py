""" compute knn accuracy """

import sys
import pickle
import numpy as np

y_test = np.array(pickle.load(open('data/test_labels.data', 'rb')))

# reduced
#dist1 = np.genfromtxt('dis/train_test_dis_array.txt', delimiter=',')
#y_train1 = np.genfromtxt('data/reduced_train_label.txt', dtype='uint8')

# GAN_no_reduce
dist1 = np.genfromtxt('dis/train_test_dis_array_GANs_no_reduce.txt', delimiter=',')
y_train1 = np.genfromtxt('data/train_labels_with_GANs.txt', dtype='uint8')


# reduced scaled
#dist2 = np.genfromtxt('dis/train_test_dis_array_scaled.txt', delimiter=',')
#y_train2 = np.genfromtxt('data/reduced_train_label_scaled.txt', dtype='uint8')

# scaled
#dist3 = np.genfromtxt('dis/train_test_dis_array_scaled_no_reduce.txt', delimiter=',')
#y_train3 = np.genfromtxt('data/train_labels.txt', dtype='uint8')


def knn_accuracy(y_train, y_test, dist, ks):
    sortedind = dist.argsort(axis=0)
    # majority vote
    for k in ks:
        count = 0
        for i in range(y_test.size):
            knearest = sortedind[:k, i]
            y_pred = np.bincount(y_train[knearest]).argmax()
            if y_pred == y_test[i]:
                count += 1
        print("k={0}, accuracy={1}%".format(k, count/y_test.size))
        sys.stdout.flush()

if __name__ == '__main__':
    ks = [i for i in range(1, 21)]

    print("GAN No Reduce:")
    knn_accuracy(y_train1, y_test, dist1, ks)
