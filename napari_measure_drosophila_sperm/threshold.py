import napari
from magicgui import magic_factory
import numpy as np
import skimage
from . import util


# returns: binary image (int)
def thresh(data, filter_maxrange):
    grey = util.greyize(data)

    filtered = skimage.filters.hessian(
        grey, range(1, filter_maxrange), black_ridges=True
    )
    return filtered


def thresh2(data, filter_maxrange, thresh):
    grey = util.greyize(data)
    tophat = skimage.morphology.white_tophat(grey, skimage.morphology.disk(1))

    filtered = skimage.filters.meijering(
        grey - tophat, range(1, filter_maxrange), black_ridges=False
    )

    median = skimage.filters.median(filtered)
    # denoised = skimage.restoration.denoise_wavelet(median, rescale_sigma=True)
    return skimage.util.img_as_ubyte(median) > thresh


def thresh3(data):
    grey = util.greyize(data)
    thresh = skimage.filters.threshold_local(grey, 35,offset=101)
    return grey > thresh


@magic_factory
# from https://napari.org/0.5.2/tutorials/segmentation/annotate_segmentation.html#segmentation
def threshold_plugin(
    image: "napari.layers.Image",
    # filter_maxrange: int = 2,
    thresh: int = 2,
    dilate: bool = False,
) -> "napari.types.LayerDataTuple":
    filter_maxrange=2
    # threshed = thresh2(image.data, filter_maxrange, thresh)
    threshed = thresh3(image.data)

    final = (
        skimage.morphology.binary_dilation(threshed, skimage.morphology.diamond(3))
        if dilate
        else threshed
    )

    return (final, {"name": "threshold result"}, "image")
