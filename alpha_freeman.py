

#
#
# this file is a prototype of the pixel deleation and freeman code computer 
#
#

from matplotlib import pylab as pt
from mnist import MNIST
from numpy import array, uint8
import cv2
import pickle


vis = array( [False] * (28*28) )
vis = vis.reshape([28, 28])

dx4 = [0,1, 0,-1]
dy4 = [1,0,-1, 0]

dx8 = [-1,-1, 0, 1, 1, 1, 0,-1]
dy8 = [ 0, 1, 1, 1, 0,-1,-1,-1]

def check_4_neighbors(x,y,image):
    for z in range(4):
        if x+dx4[z] >= 0 and x+dx4[z] < 28 and y+dy4[z] >= 0 and y+dy4[z] < 28: 
            if image[ x+dx4[z] , y+dy4[z] ] == 255:
                return True
    return False

def dfs(x,y,img):
    global vis
    if vis[x,y] != 0 or img[x,y] == 255:
        return
    vis[x,y] = 1
    
    if check_4_neighbors(x,y,img):
        vis[x,y] = 255

    for z in range(4):
        if x+dx4[z] >= 0 and x+dx4[z] < 28 and y+dy4[z] >= 0 and y+dy4[z] < 28:
            dfs(x+dx4[z],y+dy4[z],img) 
    
def get_boarders(img):
    global vis
    vis = array( [0] * (28*28) )
    vis = vis.reshape([28, 28])
    for i in range(0,28):
        img[i,0] = img[0,i] = img[i,27] = img[27,i] = 0
    dfs(0,0,img)
          
    for i in range(0,28):
        for j in range(0,28):
            if vis[i,j] == 255:
                img[i,j] = 255
            else:
                img[i,j] = 0
    return img

def get_chain(img):
    chain = []
    start_point = (-1,-1)
    for i in range(0,28):
        for j in range(0,28):
            if img[i,j] == 255:
                start_point = (i,j)
                break
        if start_point != (-1,-1):
            break

    current_point = (-1,-1)
    x,y = start_point
    for z in range(8):
        if x+dx8[z] >= 0 and x+dx8[z] < 28 and y+dy8[z] >= 0 and y+dy8[z] < 28: 
            if img[ x+dx8[z] , y+dy8[z] ] == 255: 
                current_point = x+dx8[z] , y+dy8[z]
                chain.append(z)
                break
    
    vis = array( [0] * (28*28) )
    vis = vis.reshape([28, 28])

    vis[current_point] = vis[start_point] = 255
    
    while current_point != start_point:
        print(current_point)
        x,y = current_point
        for z in range(8):
            if x+dx8[z] >= 0 and x+dx8[z] < 28 and y+dy8[z] >= 0 and y+dy8[z] < 28: 
                if img[ x+dx8[z] , y+dy8[z] ] == 255 and vis[ x+dx8[z] , y+dy8[z] ] != 255: 
                    current_point = x+dx8[z] , y+dy8[z]
                    vis[current_point] = 255
                    chain.append(z)
                    break
    
    for i in range(0,28):
        for j in range(0,28):
            if vis[i,j] == 255:
                img[i,j] = 255
            else:
                img[i,j] = 0

    return img, chain


def my_freeman_calc(img):

    img = get_boarders(img)
    pt.imshow(img)
    pt.show()
    img, chain = get_chain(img)

    return img, chain    

def check_point_inside(point):
    x,y = point
    return x >= 0 and x < 28 and y >= 0 and y < 28


def freeman_calc(img):

    vis = array( [False] * (28*28) )
    vis = vis.reshape([28, 28])

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
   
    for i in range(0,28):
        for j in range(0,28):
            if vis[i,j]:
                img[i,j] = 255
            else:
                img[i,j] = 0
    return img, chain

def dfs_count(img,x,y):
    
    if img[x,y] != 255 or vis[x,y]:
        return
    vis[x,y] = True

    for z in range(8):
        if x+dx8[z] >= 0 and x+dx8[z] < 28 and y+dy8[z] >= 0 and y+dy8[z] < 28:
            dfs_count(img,x+dx8[z],y+dy8[z]) 

def count_component(im_bw):
    global vis
    vis = array( [False] * (28*28) )
    vis = vis.reshape([28, 28])
    ret = 0
    for i in range(28):
        for j in range(28):
            if im_bw[i,j] == 255 and not vis[i,j]:
                ret += 1
                dfs_count(im_bw,i,j)
    return ret


def BS_threshold(im_gray):

    f = 1
    l = 127
    ret = 127
    while f<l:
        m = int((f+l)/2)
        (_,im_bw) = cv2.threshold(im_gray, m, 255, cv2.THRESH_BINARY)
        number_component = count_component(im_bw)
        print(number_component,f,m,l)
        if number_component == 0:
            print("number_component == 0 is not false !!")
            exit(2)
        if number_component == 1:
            f = m+1
            ret = m
            return cv2.threshold(im_gray, ret, 255, cv2.THRESH_BINARY)
        else:
            l = m
    
    print("BS did not find a solution!!")
    pt.imshow(im_gray)
    pt.show()
    cv2.imwrite('C:\\Users\\Muaz\\Desktop\\MLDM project\\ML_Project\\badbad.png',im_gray)
    exit(2)
    return cv2.threshold(im_gray, ret, 255, cv2.THRESH_BINARY)
    
if __name__ == "__main__":

    threshold = 100
    mndata = MNIST('C:\\Users\\Muaz\\Desktop\\MLDM project\\ML_Project\\data')
    for coco in range(2):
        itemlist = []
        if coco == 0:
            images, labels = mndata.load_testing()
        else:
            images, labels = mndata.load_training()
        print("read done")
        for i in range(694,len(images)):
            
            print (i)
            im_gray = array(images[i])
            im_gray = im_gray.reshape([28, 28])
            im_gray = im_gray.astype(uint8)
            
           
            #im_bw = cv2.adaptiveThreshold(im_gray, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY ,11,2) 
            (thresh, im_bw) = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY)
            if count_component(im_bw) > 1:
                print("*****")
                (thresh, im_bw) = BS_threshold(im_gray) 

         
            code_bw, code = freeman_calc(im_bw)
         
            
            if len(code) < 20:
                #print("coco")
                #pt.imshow(code_bw)
                #pt.show()
                #pt.imshow(im_gray)
                #pt.show()
                print(thresh)
                (thresh, im_bw) = cv2.threshold(im_gray, threshold, 255, cv2.THRESH_BINARY)
                pt.imshow(im_bw)
                pt.show()

            itemlist.append(code)
            if i % 100 == 0:
                print(i/100)
                
    
        if coco == 0:
            with open('test.data', 'wb') as fp1:
                pickle.dump(itemlist, fp1)
            with open('test_labels.data', 'wb') as fp2:
                pickle.dump(labels, fp2)
        else:
            with open('train.data', 'wb') as fp1:
                pickle.dump(itemlist, fp1)
            with open('train_labels.data', 'wb') as fp2:
                pickle.dump(labels, fp2)
    
    
   
    
