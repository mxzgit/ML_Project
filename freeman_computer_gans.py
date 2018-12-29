import os
#from matplotlib import pylab as pt
from numpy import array, uint8
import cv2
import pickle
import numpy as np
import sys

from cv2 import imread
import numpy as np
#from matplotlib import pylab as pt

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

x_d = 28
y_d = 28
#s
vis = array( [False] * (x_d*y_d) )
vis = vis.reshape([x_d, y_d])

dx4 = [0,1, 0,-1]
dy4 = [1,0,-1, 0]

dx8 = [-1,-1, 0, 1, 1, 1, 0,-1]
dy8 = [ 0, 1, 1, 1, 0,-1,-1,-1]

def in_board(x,y):
	return x >=0 and x < x_d and y >=0 and y < y_d

def check_4_neighbors(x,y,image):
	for z in range(4):
		if in_board(x+dx4[z],y+dy4[z]) : 
			if image[ x+dx4[z] , y+dy4[z] ] == 255:
				return True
	return False

def check_point_inside(point):
	x,y = point
	return x >= 0 and x < x_d and y >= 0 and y < y_d

def freeman_calc(img):

	#cv2.imwrite("input.jpg",img)
	#print(img)
	vis = array( [False] * (x_d*y_d) )
	vis = vis.reshape([x_d, y_d])

	done = False
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i,j] == 255:
				start_point = (i, j)
				img[i+1,j] = 255
				#print(start_point, value)
				done = True
				break
			else:
				continue
		if done:
			break
		
	directions = [0, 1, 2, 3, 4, 5, 6, 7]
	dir2idx = dict(zip(directions, range(len(directions))))
	change_j =  [ 0, 1, 1, 1, 0,-1,-1,-1 ]
	change_i =  [-1,-1, 0,+1,+1,+1, 0,-1 ]
 
	border = []
	chain = []
	curr_point = start_point
	vis[curr_point] = True
	for direction in directions:
		idx = dir2idx[direction]
		new_point = (start_point[0]+change_i[idx], start_point[1]+change_j[idx])
		if not check_point_inside(new_point):
			continue
		if img[new_point] != 0: # if is ROI
			border.append(new_point)
			vis[new_point] = True
			chain.append(direction)
			curr_point = new_point
			break

	count = 0
	while curr_point != start_point:
		#figure direction to start search
		#print(curr_point)
		b_direction = (direction + 5) % 8 
		dirs_1 = range(b_direction, 8)
		dirs_2 = range(0, b_direction)
		dirs = []
		dirs.extend(dirs_1)
		dirs.extend(dirs_2)
		for direction in dirs:
			idx = dir2idx[direction]
			new_point = (curr_point[0]+change_i[idx], curr_point[1]+change_j[idx])
			if not check_point_inside(new_point):
				continue
			if img[new_point] != 0: # if is ROI
				border.append(new_point)
				vis[new_point] = True
				chain.append(direction)
				curr_point = new_point
				break
		if count == 1000: break
		count += 1
   
	for i in range(0,x_d):
		for j in range(0,y_d):
			if vis[i,j]:
				img[i,j] = 255
			else:
				img[i,j] = 0
	#cv2.imwrite("code.jpg",img)
	
	return img, chain

def dfs_count(img,x,y):
	
	if img[x,y] != 255 or vis[x,y]:
		return
	vis[x,y] = True

	for z in range(8):
		if check_point_inside((x+dx8[z],y+dy8[z])):
			dfs_count(img,x+dx8[z],y+dy8[z]) 

def count_component(im_bw):
	global vis
	vis = array( [False] * (x_d*y_d) )
	vis = vis.reshape([x_d, y_d])
	ret = 0
	for i in range(x_d):
		for j in range(y_d):
			if im_bw[i,j] == 255 and not vis[i,j]:
				ret += 1
				dfs_count(im_bw,i,j)
	
	return ret

def fill_8_neighbors(x,y,img):
	for z in range(8):
		xx = x + dx8[z]
		yy = y + dy8[z]
		if in_board(xx,yy):
			img[xx,yy] = 255

def inflate_component(img_bw):
	temp_img = img_bw
	for i in range(x_d):
		for j in range(y_d):
			if img_bw[i,j] == 255:
				fill_8_neighbors(i,j,temp_img)
	return temp_img

if __name__ == "__main__":

	dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data/pics")
	c = 0
	if not os.path.exists(dir_path):
		print("error reading the directory")
		exit(1)
	codes = []
	labels = []
	for subdir, dirs, files in os.walk(dir_path):
		for file in files:
			filepath = subdir + os.sep + file
			#if 'fixed' in filepath:
			#	continue

			if filepath.endswith(".png") or filepath.endswith(".PNG"):
				im_gray = cv2.imread(filepath,0)
				y,x = 15,40
				w = 75
				im_gray = im_gray[y:y+w, x:x+w]
				#cv2.imwrite(str(c)+".jpg",im_gray)
				im_gray = im_gray.astype(uint8)
				im_gray = cv2.resize(im_gray,(int(28),int(28)))
				(thresh, im_bw) = cv2.threshold(im_gray, 30, 255, cv2.THRESH_BINARY)
				#print(im_bw[0])
				while count_component(im_bw) > 1:
					im_bw = inflate_component(im_bw)
				
				code = []
				
				#cv2.imwrite("shit.jpg",im_bw)
				#exit(1)
				code_bw, code = freeman_calc(im_bw)
				codes.append(code)
				if 'zero' in filepath:
					labels.append(0)
				elif 'one' in filepath:
					labels.append(1)
				elif 'two' in filepath:
					labels.append(2)
				elif 'three' in filepath:
					labels.append(3)
				elif 'four' in filepath:
					labels.append(4)
				elif 'five' in filepath:
					labels.append(5)
				elif 'six' in filepath:
					labels.append(6)
				elif 'seven' in filepath:
					labels.append(7)
				elif 'eight' in filepath:
					labels.append(8)
				elif 'nine' in filepath:
					labels.append(9)
				else:
					labels.append(-1)
					exit(1)
				#print(code)
				c += 1
				if c%10 == 0 :
					#print(code)
					print(c)
					sys.stdout.flush()
	
	print(len(codes),len(labels))

	with open('GANs_code.data', 'wb') as fp1:
		pickle.dump(codes, fp1)

	with open('GANs_labels.data', 'wb') as fp1:
		pickle.dump(labels, fp1)
				
				
				
				