

#
#
# this file is a prototype of the pixel deleation and freeman code computer 
#
#

from matplotlib import pylab as pt
from mnist import MNIST
from numpy import array, uint8
import cv2

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

def freeman_calc(img):

    vis = array( [False] * (28*28) )
    vis = vis.reshape([28, 28])

    done = False
    for i, row in enumerate(img):
        for j, value in enumerate(row):
            if value == 255:
                start_point = (i, j)
                #print(start_point, value)
                done = True
                break
            else:
                continue
        if done:
            break
        
    directions = [ 0,  1,  2,
                7,      3,
                6,  5,  4]
    dir2idx = dict(zip(directions, range(len(directions))))

    change_j =   [-1,  0,  1, # x or columns
                -1,      1,
                -1,  0,  1]

    change_i =   [-1, -1, -1, # y or rows
                0,      0,
                1,  1,  1]

    border = []
    chain = []
    curr_point = start_point
    for direction in directions:
        idx = dir2idx[direction]
        new_point = (start_point[0]+change_i[idx], start_point[1]+change_j[idx])
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

if __name__ == "__main__":
    
    read_all_data = False
    if read_all_data:
        mndata = MNIST('C:\\Users\\Muaz\\Desktop\\ML_Project\\data')
        images, labels = mndata.load_training()
        im_gray = array(images[0])
        im_gray = im_gray.reshape([28, 28])
    else:
        im_gray = cv2.imread('C:\\Users\\Muaz\\Desktop\\ML_Project\\img.png',0)

    
    im_gray = im_gray.astype(uint8)
    #cv2.imwrite('C:\\Users\\Muaz\\Desktop\\ML_Project\\img.png',im_gray)

    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    #print(labels[0])
    print(im_bw)
    pt.imshow(im_bw)
    pt.show()
    im_bw, code = freeman_calc(im_bw)
    print(code)
    pt.imshow(im_bw)
    pt.show()
    
