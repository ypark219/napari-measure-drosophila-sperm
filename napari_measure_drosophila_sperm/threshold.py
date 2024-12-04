import napari
from magicgui import magic_factory
import numpy as np
import skimage
from . import util


# returns: binary image (int)
def thresh(data, filter_maxrange, clean_minsize):
    grey = util.greyize(data)

    filtered = skimage.filters.hessian(
        grey, range(1, filter_maxrange), black_ridges=True
    )
    return filtered


def thresh2(data, filter_maxrange):
    grey = util.greyize(data)

    filtered = skimage.filters.meijering(
        grey, range(1, filter_maxrange), black_ridges=False
    )

    median = skimage.filters.median(filtered)
    denoised = skimage.restoration.denoise_wavelet(median, rescale_sigma=True)
    return skimage.filters.threshold_otsu(denoised).astype(bool).astype(int)


@magic_factory
# from https://napari.org/0.5.2/tutorials/segmentation/annotate_segmentation.html#segmentation
def threshold_plugin(
    image: "napari.layers.Image",
    filter_maxrange: int = 2,
    clean_minsize: int = 100,
    dilate: bool = False,
    # min_size: int=1,
    # conn: int=1
) -> "napari.types.LayerDataTuple":

    threshed = thresh2(image.data, filter_maxrange)

    final = (
        skimage.morphology.binary_dilation(threshed, skimage.morphology.diamond(3))
        if dilate
        else threshed
    )

    return (final, {"name": "threshold result"}, "image")
