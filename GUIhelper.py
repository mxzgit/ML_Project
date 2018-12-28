import numpy as np
import cv2
from freeman_computer import *

import os

def bmp2freeman(bmppath):
	im_gray = cv2.imread(bmppath, 0)
	im_gray = im_gray.astype(np.uint8)
	im_gray = 255 - im_gray
	(thresh, im_bw) = cv2.threshold(im_gray, 30, 255, cv2.THRESH_BINARY)
	while count_component(im_bw) > 1:
		im_bw = inflate_component(im_bw)
	code = []
	code_bw, code = freeman_calc(im_bw)
	return code


X_train = np.genfromtxt('data/reduced_train.txt', dtype=str)
y_train = np.genfromtxt('data/reduced_train_label.txt', dtype='uint8')

def predict(code, k=7):
	command = './coco ' + str(code).replace(' ','').replace('[','').replace(']','').replace(',','')
	#print(os.system(command))
	os.system(command)
	text_file = open("distance_res.txt", "r")
	lines = text_file.read().split(' ')
	dist = np.array([float(c) for c in lines])
	#print(str(dist))
	#print('size ' + str(len(dist)))
	sortedind = dist.argsort(axis=0)
	knearest = sortedind[:k]
	y_pred = np.bincount(y_train[knearest]).argmax()
	return y_pred


if __name__ == "__main__":
	code = bmp2freeman('tmp/export.bmp')
	print(code)
	print("result:")
	print(predict(code))
