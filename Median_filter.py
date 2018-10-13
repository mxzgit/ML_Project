import cv2
import numpy as np


def filter_mean(img, bloc_size):

    newimg = np.zeros(shape=(img.shape[0], img.shape[1]))
    border = int(bloc_size/2)
    members = [(0, 0)]*((1+border*2)**2)
    for i in range(border, img.shape[0]-border):
        k = 0
        for j in range(border, img.shape[1]-border):
            for k in range((1+border*2)**2):

                members[k] = img[
                    (i-border+int(k/bloc_size), j-border+int(k % bloc_size))]

            newimg[i, j] = np.int_(np.median(members, axis=0))
    return newimg


if __name__ == "__main__":

    path = 'noise_bzef.png'
    img = cv2.imread(path, 0)
    newimg = filter_mean(img, 5)
    cv2.imshow('', newimg)
    cv2.waitKey(0)
