from PIL import Image
import numpy as np


def filter_mean(path, bloc_size):
    img = Image.open(path)
    img = img.convert("RGB")
    newimg = Image.new(img.mode, img.size)
    border = int(bloc_size/2)
    members = [(0, 0)]*((1+border*2)**2)
    for i in range(border, img.size[0]-border):
        k = 0
        for j in range(border, img.size[1]-border):
            for k in range((1+border*2)**2):

                members[k] = img.getpixel(
                    (i-border+int(k/bloc_size), j-border+int(k % bloc_size)))

            newimg.putpixel((i, j), tuple(np.int_(np.median(members, axis=0))))

    newimg.show()


if __name__ == "__main__":
    path = "img.png"
    filter_mean(path, 3)
