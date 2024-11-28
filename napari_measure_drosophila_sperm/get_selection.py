import napari
import skimage
import numpy as np
from magicgui import magic_factory
from . import util


@magic_factory
def get_selection_plugin(
    image: "napari.layers.Image",
    shape: "napari.layers.Shapes"
) -> "napari.types.LayerDataTuple":
    return (get_selection(image.data, shape), {"name": "selection"}, "image")


def get_selection(data, shape):
    grey = util.greyize(data).astype(int)
    dimensions = data.shape

    mask = shape.to_labels()
    mask = np.pad(
        mask,
        ((0, dimensions[0] - mask.shape[0]), (0, dimensions[1] - mask.shape[1])),
        "constant",
    )

    result = np.bitwise_and(grey.astype(bool), mask.astype(bool))
    return result.astype(int)
