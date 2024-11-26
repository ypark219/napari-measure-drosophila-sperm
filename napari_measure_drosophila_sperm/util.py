import numpy as np
import skimage

# converts color images to grey, and returns original if already grey
def greyize(img):
    if len(img.shape) == 3:
        return skimage.color.rgb2gray(img)
    else:
        return img
    