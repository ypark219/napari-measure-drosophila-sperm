import numpy as np
import skimage

# converts color images to grey, and returns original if already grey
# returns array of floats
def greyize(data):
    if len(data.shape) == 3:
        return skimage.color.rgb2gray(data)
    else:
        return data
    