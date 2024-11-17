import napari
import skimage as ski
from magicgui import magic_factory

@magic_factory
def blur(
    image: "napari.layers.Image",
    sigma: float=3.0,
    truncate: float=3.5,
) -> "napari.types.LayerDataTuple":
    blurred = ski.filters.gaussian(image.data, sigma=(sigma, sigma), truncate=truncate, channel_axis=-1)

    return (blurred, {"name":"blurred"}, "image")
