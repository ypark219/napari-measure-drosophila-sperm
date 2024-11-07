import napari
import skimage
from magicgui import magic_factory
from skimage.morphology import skeletonize

@magic_factory
def find_skeleton(
    image: "napari.layers.Image",
) -> "napari.types.LayerDataTuple":
    # perform skeletonization
    skeleton = skeletonize(image.data)

    return (skeleton, {"name":"skeleton"}, "image")
