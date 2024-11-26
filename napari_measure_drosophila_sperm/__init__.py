import napari
from magicgui import magic_factory
import numpy as np
import skimage
from . import threshold,util

@magic_factory
def driver(
    image: "napari.layers.Image", shape: "napari.layers.Shapes"
) -> "napari.types.LayerDataTuple":
    threshed = threshold.thresh(image.data)

    mask = shape.to_labels()
    mask = np.pad(
        mask, ((0, 2048 - mask.shape[0]), (0, 2048 - mask.shape[1])), "constant"
    )
    result = np.bitwise_and(threshed.astype(bool), mask.astype(bool))

    return (result, {"name": "selection"}, "image")

# resize image to half its original size and delete original layer
@magic_factory
def downscale(
    image: "napari.layers.Image",
    aa: bool = True
) -> "napari.types.LayerDataTuple":
    a = skimage.transform.rescale(util.greyize(image.data), 0.5, anti_aliasing=aa)
    napari.current_viewer().layers.remove(image.name)
    return (a, {"name": "scaled"}, "image")
