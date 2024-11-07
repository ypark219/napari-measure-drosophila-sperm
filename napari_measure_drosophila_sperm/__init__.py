from napari.utils.notifications import show_info
import napari
from magicgui import magic_factory

import numpy as np
import skimage
from skimage import data
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square, remove_small_objects
from skimage.color import rgb2gray

# @magic_factory
# #my edited version. it works on images now but doesn't convert to greyscale
# def threshold(
#     image: "napari.layers.Image",
#     threshold: int = 200,
# ) -> "napari.types.LayerDataTuple":
#     #show_info("image rgb: {x}".format(x=image.rgb))
#     data = rgb2gray(image.data > threshold) #`rgb2gray(image.data) > threshold` doesn't work for some reason ㅠㅠ
#     metadata = {"name": "thresholded"} # colormap doesn't seem to take effect. setting "rgb": False breaks things
#     layer_type = "image" # i want to return a Labels layer but setting layer_type to "labels" and changing data to (image > threshold).astype(int) doesn't give a proper output
#     return (data, metadata, layer_type)




# trying with otsu thresholding
@magic_factory
# from https://napari.org/0.5.2/tutorials/segmentation/annotate_segmentation.html#segmentation
def threshold(
    image: "napari.types.ImageData"
    # ,
    # min_size: int=1,
    # conn: int=1
) -> "napari.types.LayerDataTuple":
    grey = rgb2gray(image)
    # apply threshold
    # options: isodata, li, mean, minimum, otsu, triangle, yen, niblack, sauvola

    thresh = skimage.filters.threshold_niblack(grey)
    # bw = closing(grey > thresh, square(4))
    bw=grey>thresh

    # remove artifacts connected to image border
    # cleared = remove_small_objects(clear_border(bw), min_size,conn)

    return (bw, {"name": "segmentation"}, "labels")



# redundant
# viewer = napari.Viewer()  # create new instance of napari
# thresh_widget = threshold()
# viewer.window.add_dock_widget(thresh_widget)  # create widget and attach
