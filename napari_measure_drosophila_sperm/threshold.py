import napari
import skimage
from magicgui import magic_factory
from . import util, measure


# thresholds and denoises an image
# returns: binary image (int)
def thresh(data, thresh):
    grey = util.greyize(data)
    tophat = skimage.morphology.white_tophat(grey, skimage.morphology.disk(1))

    filtered = skimage.filters.meijering(grey - tophat, range(1, 2), black_ridges=False)

    median = skimage.filters.median(filtered)
    return skimage.util.img_as_ubyte(median) > thresh


@magic_factory
def clean_widget(
    image: "napari.layers.Image", min_size: int = 50, and_measure: bool = True
) -> "napari.types.LayerDataTuple":
    result = skimage.morphology.remove_small_objects(
        image.data.astype(bool), min_size, connectivity=2
    )
    napari.current_viewer().layers.remove(image.name)
    if and_measure:
        measure.measure_manual(result)
    return (result, {"name": image.name}, "image")
