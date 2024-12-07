import skimage


# utility method that converts color images to grey and returns original if already grey
def greyize(data):
    if len(data.shape) == 3:
        return skimage.color.rgb2gray(data)
    else:
        return data
