import napari
from magicgui import magic_factory
import numpy as np
import skimage
from . import util


# returns: binary image (int)
def thresh(data, filter_maxrange, clean_minsize):
    grey = util.greyize(data)

    # filtered = skimage.filters.hessian(
    #     grey, range(1, filter_maxrange), black_ridges=True
    # )
    filtered = skimage.filters.meijering(
        grey, range(1, filter_maxrange), black_ridges=False
    )
    # opened = skimage.morphology.opening(filtered)
    # labelled = skimage.measure.label(opened)

    # cleaned = skimage.morphology.remove_small_objects(labelled, min_size=clean_minsize)
    # closed = skimage.morphology.diameter_closing(cleaned, 10, connectivity=1)
    

    # final = skimage.morphology.binary_closing(closed)
    #realfinal = final.astype(bool).astype(int)  # converts to binary image
    median = skimage.filters.median(filtered)
    denoised = skimage.restoration.denoise_wavelet(median, rescale_sigma=True)
    return denoised


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
    
    threshed = thresh(image.data, filter_maxrange, clean_minsize)

    # grey = skimage.color.rgb2gray(image)

    # # apply threshold
    # # options: isodata, li, mean, minimum, otsu, triangle, yen, niblack, sauvola
    # # ridge-specific options (slower): https://scikit-image.org/docs/dev/auto_examples/edges/plot_ridge_filter.html#sphx-glr-auto-examples-edges-plot-ridge-filter-py

    # # blurred=skimage.filters.gaussian(grey,truncate=2)
    # # filtered = skimage.filters.threshold_sauvola(grey)
    # filtered = skimage.filters.hessian(
    #     grey, range(1, filter_maxrange), black_ridges=True
    # )
    # opened = skimage.morphology.opening(
    #     filtered
    # )  # apparently binary_opening is faster but it won't work at all for me
    # labelled = skimage.measure.label(opened)
    # cleaned = skimage.morphology.remove_small_objects(labelled, min_size=clean_minsize)
    # # closed = skimage.morphology.closing(cleaned)
    # closed = skimage.morphology.diameter_closing(cleaned, 10, connectivity=1)
    # # bw = closing(grey > thresh, square(4))
    # # bw=grey>thresh

    # # remove artifacts connected to image border
    # # cleared = remove_small_objects(clear_border(bw), min_size,conn)
    if dilate:
        final = skimage.morphology.binary_dilation(
            threshed, skimage.morphology.diamond(3)
        )
    else:
        final = threshed

    # final3 = skimage.morphology.binary_closing(final)
    # final2 = final3.astype(bool).astype(int)  # converts to binary image
    return (final, {"name": "threshold result"}, "image")
