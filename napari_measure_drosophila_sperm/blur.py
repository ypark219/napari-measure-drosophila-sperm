import napari
import skimage as ski
from magicgui import magic_factory

@magic_factory
def denoise(
    image: "napari.layers.Image"
) -> "napari.types.LayerDataTuple":
    denoised= ski.restoration.denoise_wavelet(image.data, channel_axis=-1, convert2ycbcr=True, rescale_sigma=True)
    return (denoised, {"name": "denoised"}, "image")

@magic_factory
def blur(
    image: "napari.layers.Image",
    sigma: float=3.0,
    truncate: float=3.5,
) -> "napari.types.LayerDataTuple":
    blurred = ski.filters.gaussian(image.data, sigma=(sigma, sigma), truncate=truncate, channel_axis=-1)

    return (blurred, {"name":"blurred"}, "image")
