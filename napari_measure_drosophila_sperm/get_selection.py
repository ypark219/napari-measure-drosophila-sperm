import napari
import skimage
import numpy as np
from magicgui import magic_factory

@magic_factory
def get_selection(
    image: "napari.layers.Image",
    shape: "napari.layers.Shapes"
) -> "napari.types.LayerDataTuple":
    data = skimage.color.rgb2gray(image.data > 200) #thresholding can be separated out later

    mask = shape.to_labels()
    mask = np.pad(mask,((0,2048-mask.shape[0]),(0,2048-mask.shape[1])),'constant')
    result = np.bitwise_and(data.astype(int),mask.astype(int))

    return (result, {"name":"selection"}, "image")