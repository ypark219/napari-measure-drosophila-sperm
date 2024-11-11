import napari
import numpy as np
from magicgui import magic_factory

@magic_factory
def measure(
    image: "napari.layers.Image",
) -> "napari.types.LayerDataTuple":
    print(image.data.sum())
    print(np.count_nonzero(image.data))

    return (image.data, {"name":"skeleton"}, "image")
