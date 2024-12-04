import napari
import skimage
import numpy as np
from magicgui import magic_factory
from . import util


@magic_factory
def get_selection_plugin(
    image: "napari.layers.Image", shape: "napari.layers.Shapes"
) -> "napari.types.LayerDataTuple":
    return (get_selection(image.data, shape), {"name": "selection"}, "image")


def get_selection(data, shape):
    grey = util.greyize(data).astype(int)
    img_x, img_y = data.shape

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

    return np.where(mask == 1, grey, 0)
