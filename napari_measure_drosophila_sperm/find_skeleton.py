import napari
import skimage as ski
from magicgui import magic_factory
from skimage.morphology import skeletonize
from itertools import chain

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

    labelled = ski.measure.label(image.data)
    flattened = list(chain.from_iterable(labelled))
    occurences = [0] * (max(flattened)+1)
    for i in flattened:
        occurences[i] += 1
    occurences[0] = 0 # ignore black pixels (background will usually be largest connected component)
    largest_object_val = occurences.index(max(occurences))

    # only keep largest object
    for i in range(0,len(labelled)):
        for j in range(0,len(labelled[i])):
            if labelled[i][j] != largest_object_val:
                labelled[i][j] = 0

    # perform skeletonization
    skeleton = skeletonize(labelled.astype(bool), method='zhang')

    #largest = ski.morphology.remove_small_objects(skeleton, min_size=min_size, connectivity=2)

    return (skeleton, {"name":"skeleton"}, "image")
