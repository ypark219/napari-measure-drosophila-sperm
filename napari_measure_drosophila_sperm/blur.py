import napari
import skimage as ski
from magicgui import magic_factory

@magic_factory
def blur(
    image: "napari.layers.Image",
) -> "napari.types.LayerDataTuple":
    blurred = ski.filters.gaussian(image.data, sigma=(3.0, 3.0), truncate=3.5, channel_axis=-1)

    return (blurred, {"name":"blurred"}, "image")
