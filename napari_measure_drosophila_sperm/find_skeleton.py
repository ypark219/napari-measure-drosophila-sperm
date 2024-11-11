import napari
import skimage as ski
from magicgui import magic_factory
from skimage.morphology import skeletonize

@magic_factory
def find_skeleton(
    image: "napari.layers.Image",
    closing_iterations: int=1,
    min_size: int=10,
) -> "napari.types.LayerDataTuple":
    # perform closing
    # closed = image.data
    # for i in range(closing_iterations):
    #     closed = ski.morphology.binary_closing(closed)

    # closed1 = ski.morphology.binary_closing(image.data)
    # print(closed1)
    # closed2 = ski.morphology.binary_closing(closed1)

    # perform skeletonization
    skeleton = skeletonize(image.data, method='zhang')

    largest = ski.morphology.remove_small_objects(skeleton, min_size=min_size, connectivity=2)

    return (largest, {"name":"skeleton"}, "image")
