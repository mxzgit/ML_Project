import numpy as np
import cv2
from freeman_computer import *
from dp_rolling import dp_rolling_ed


def bmp2freeman(bmppath):
    im_gray = cv2.imread(bmppath, 0)
    im_gray = im_gray.astype(np.uint8)
    (thresh, im_bw) = cv2.threshold(im_gray, 30, 255, cv2.THRESH_BINARY)
    while count_component(im_bw) > 1:
        im_bw = inflate_component(im_bw)
    code = []
    code_bw, code = freeman_calc(im_bw)
    return code


X_train = np.genfromtxt('data/reduced_train.txt', dtype=str)
y_train = np.genfromtxt('data/reduced_train_label.txt', dtype='uint8')

def predict(code, k=7):
    dist = np.array([dp_rolling_ed(c, code) for c in X_train])
    sortedind = dist.argsort(axis=0)
    knearest = sortedind[:k]
    y_pred = np.bincount(y_train[knearest]).argmax()
    return y_pred


if __name__ == "__main__":
    code = bmp2freeman('tmp/export.bmp')
    print(code)
    print(predict(code))