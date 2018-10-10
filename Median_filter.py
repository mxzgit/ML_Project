from PIL import Image
import numpy as np


scale = 5
border = int(scale/2)

members = [(0,0)]*scale*scale

iterations = 50
newimg = Image.open("noise_bzef.png")
newimg.show()

img = Image.new("RGB",newimg.size,"white")
img = newimg

for iteration in range(iterations):
    print("iteration %.0f of 5"%iteration)
    for i in range(border,img.size[0]-border):
        for j in range(border,img.size[1]-border):
            members[0] = img.getpixel((i-2,j-2))
            members[1] = img.getpixel((i-2,j-1))
            members[2] = img.getpixel((i-2,j))
            members[3] = img.getpixel((i-2,j+1))
            members[4] = img.getpixel((i-2,j+2))
            members[5] = img.getpixel((i-1,j-2))
            members[6] = img.getpixel((i-1,j-1))
            members[7] = img.getpixel((i-1,j))
            members[8] = img.getpixel((i-1,j+1))
            members[9] = img.getpixel((i-1,j+2))
            members[10] =img.getpixel((i,j-2))
            members[11] =img.getpixel((i,j-1))
            members[12] =img.getpixel((i,j))
            members[13] =img.getpixel((i,j+1))
            members[14] =img.getpixel((i,j+2))
            members[15] =img.getpixel((i+1,j-2))
            members[16] =img.getpixel((i+1,j-1))
            members[17] =img.getpixel((i+1,j))
            members[18] =img.getpixel((i+1,j+1))
            members[19] =img.getpixel((i+1,j+2))
            members[20] =img.getpixel((i+2,j-2))
            members[21] =img.getpixel((i+2,j-1))
            members[22] =img.getpixel((i+2,j))
            members[23] =img.getpixel((i+2,j+1))
            members[24] =img.getpixel((i+2,j+2))
            #print(members)
            #print(tuple(np.int_(np.sum(members, axis=0)/9)))
            img.putpixel((i, j), tuple(np.int_(np.median(members,axis=0))))
    
    if iteration%5==0:
        img.show()
    
    

        


