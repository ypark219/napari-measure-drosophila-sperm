import napari
import numpy as np
import skimage
from magicgui import magic_factory
from . import util, threshold, skeletonize, get_selection, measure


# thresholds and skeletonises a selection of a downscaled (50%) image
@magic_factory
def driver(
    image: "napari.layers.Image", shape: "napari.layers.Shapes"
) -> "napari.types.LayerDataTuple":
    viewer = napari.current_viewer()

    SCALE = (
        # all test images are 2048x2048 except for one
        1 if image.data.shape[0] == 1024 else 0.5
    )

    # rescale image and selection (if Shape exists), and remove originals
    downscaled = skimage.transform.rescale(
        util.greyize(image.data), SCALE, anti_aliasing=True
    )
    viewer.layers.remove(image.name)
    viewer.add_image(downscaled, name="original image")
    threshed = threshold.thresh(downscaled, 2)

    # if no shape is given, apply to whole image
    if shape is not None:
        shape_small = shape
        shape_small.scale = shape.scale * SCALE
        shape_small.data = np.multiply(shape.data, SCALE)
        viewer.layers.remove(shape.name)
        selection = get_selection.get_selection(threshed, shape_small)
    else:
        selection = threshed

    skeleton = skimage.morphology.skeletonize(selection.astype(bool), method="zhang")

    result = skeleton
    return (result, {"name": image.name}, "image")


# add widgets to dock when 
viewer = napari.current_viewer()

viewer.window.add_dock_widget(threshold.clean_widget(), name="Remove Noise")
viewer.window.add_dock_widget(skeletonize.patch_skeleton_widget(), name="Patch Skeleton")
viewer.window.add_dock_widget(get_selection.remove_selection_widget(), name="Remove Selection", tabify=True) # Patch Skeleton and Remove Selection are optional so in tabs
viewer.window.add_dock_widget(skeletonize.get_largest_widget(), name="Get Largest Component")
viewer.window.add_dock_widget(measure.measure_manual_widget(), name="Measure Only", tabify=True)
