from cv2 import imread
import numpy as np
from matplotlib import pylab as pt

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

    path = 'badbad.png'
    img = imread(path, 0)
    #cv2.imshow('', img)
    #cv2.waitKey(0)
    pt.imshow(img)
    pt.show()
    newimg = filter_mean(img, 5)
    pt.imshow(newimg)
    pt.show()

    #cv2.imshow('', newimg)
    #cv2.waitKey(0)
