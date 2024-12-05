import napari
import skimage
import numpy as np
from magicgui import magic_factory
from . import util


@magic_factory
def get_selection_plugin(
    image: "napari.layers.Image", shape: "napari.layers.Shapes"
) -> "napari.types.LayerDataTuple":
    viewer = napari.current_viewer()
    viewer.layers.remove(image.name)
    viewer.layers.remove(shape.name)
    return (get_selection(image.data, shape), {"name": image.name}, "image")

@magic_factory
def remove_selection_plugin(
    image: "napari.layers.Image", shape: "napari.layers.Shapes"
) -> "napari.types.LayerDataTuple":
    viewer = napari.current_viewer()
    viewer.layers.remove(image.name)
    viewer.layers.remove(shape.name)
    return (remove_selection(image.data, shape), {"name": image.name}, "image")


def selection_helper(data, shape):
    grey = util.greyize(data)
    img_x, img_y = grey.shape

    mask = shape.to_labels()
    mask_x, mask_y = mask.shape

    # disregard parts of the mask outside img bounds
    mask_x = mask_x if mask_x <= img_x else img_x
    mask_y = mask_y if mask_y <= img_y else img_y

    mask = np.pad(
        mask,
        ((0, img_x - mask_x), (0, img_y - mask_y)),
        "constant",
    )
    return grey, mask


def get_selection(data, shape):
    grey, mask = selection_helper(data, shape)
    return np.where(mask == 1, grey, 0)


def remove_selection(data, shape):
    (grey, mask) = selection_helper(data, shape)

    return np.where(mask == 1, 0, grey)
