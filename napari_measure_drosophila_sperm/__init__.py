import napari
from magicgui import magic_factory
import numpy as np
import skimage
from . import threshold, util, get_selection, blur, measure

# plugin order of operations:
# - "driver"
# - remove small objs
# - skeletonise
# - (opt) get endpoints and re-skeletonise
# - measure

# TODO:
# - post-threshing modifications currently don't remove enough noise so try to break up some of the bigger chunks so they are all removed with remove_small_objs
# - large glare in WT.C.2_20x (medium)
# - poor results on cells with overlapping loops (hard cases)
# otsu min_size? survey all components and try to find a "threshold" for size


# blurs, thresholds, and skeletonises a selection of a downscaled (50%) image
@magic_factory
def driver(
    image: "napari.layers.Image",
    shape: "napari.layers.Shapes",
    blur_bool: bool = False
) -> "napari.types.LayerDataTuple":
    SCALE = 0.5
    viewer = napari.current_viewer()
    
    # rescale image and selection (if Shape exists), and remove originals
    downscaled = skimage.transform.rescale(util.greyize(image.data), SCALE, anti_aliasing=True)
    viewer.layers.remove(image.name)
    # if no shape is given, apply to whole image
    if shape is not None:
        shape_small = shape
        shape_small.scale = shape.scale * SCALE
        shape_small.data = np.multiply(shape.data, SCALE)
        viewer.layers.remove(shape.name)
        selection = get_selection.get_selection(downscaled, shape_small)
    else:
        selection = downscaled

    blurred = blur.blur(selection, 3.0, 3.5) if blur_bool else selection

    threshed = threshold.thresh(blurred, 4)
    opened = skimage.morphology.opening(threshed.astype(int))

    result = opened
    return (result, {"name": "result"}, "image")

@magic_factory
def driver2(
    image: "napari.layers.Image",
    shape: "napari.layers.Shapes"
) -> "napari.types.LayerDataTuple":
    selection = get_selection.get_selection(image.data, shape)

    threshed = threshold.thresh2(selection, 2, 2)
    skel = skimage.morphology.skeletonize(threshed.astype(bool), method="zhang")

    result = skel
    return (result, {"name": "result"}, "image")

# resize image to half its original size and delete original layer
@magic_factory
def downscale(
    image: "napari.layers.Image", aa: bool = True
) -> "napari.types.LayerDataTuple":
    a = skimage.transform.rescale(util.greyize(image.data), 0.5, anti_aliasing=aa)
    napari.current_viewer().layers.remove(image.name)
    return (a, {"name": "scaled"}, "image")


# plugins for manual testing, delete later


@magic_factory
def skeletonise(data: "napari.types.ImageData") -> "napari.types.LayerDataTuple":
    result = skimage.morphology.skeletonize(data.astype(bool), method="zhang")
    return (result, {"name": "skeleton"}, "image")


@magic_factory
def clean(
    data: "napari.types.ImageData", min_size: int = 5
) -> "napari.types.LayerDataTuple":
    result = skimage.morphology.remove_small_objects(
        data.astype(bool), min_size, connectivity=2
    )
    return (result, {"name": "cleaned"}, "image")


@magic_factory()
def morph(
    image: "napari.layers.Image",
    dilate: bool = False,
    erode: bool = True,
    opening: bool = False,
    close: bool = False,
) -> "napari.types.LayerDataTuple":
    if dilate:
        result = skimage.morphology.binary_dilation(image.data)
    elif erode:
        result = skimage.morphology.binary_erosion(image.data)
    elif opening:
        result = skimage.morphology.opening(image.data)
    elif close:
        result = skimage.morphology.closing(image.data)

    return (result, {"name": "morphed"}, "image")


# viewer = napari.current_viewer()
# viewer.window.add_dock_widget(skeletonise(), name="skeletonize")
# viewer.window.add_dock_widget(clean(), name="clean")
# viewer.window.add_dock_widget(measure.measure_manual(), name="measure")