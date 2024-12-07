import napari
import skimage
from magicgui import magic_factory
import itertools
from . import measure


def get_largest_component(data, items_to_keep):
    labelled = skimage.measure.label(data)
    flattened = list(itertools.chain.from_iterable(labelled))
    occurences = [0] * (max(flattened) + 1)
    largest_object_vals = [0] * items_to_keep

    for i in flattened:
        occurences[i] += 1
    occurences[0] = (
        0  # ignore black pixels (background will usually be largest connected component)
    )

    for i in range(items_to_keep):
        max_count = max(occurences)
        largest_object_vals[i] = occurences.index(max_count)
        occurences[occurences.index(max_count)] = 0

    # only keep largest objects
    for i in range(0, len(labelled)):
        for j in range(0, len(labelled[i])):
            label_matches = False
            for k in largest_object_vals:
                if labelled[i][j] == k:
                    label_matches = True
            if not label_matches:
                labelled[i][j] = 0
    return labelled


@magic_factory
def get_largest_widget(
    image: "napari.layers.Image", and_measure: bool = True
) -> "napari.types.LayerDataTuple":
    comp = get_largest_component(image.data, 1)
    if and_measure:
        measure.measure_manual(comp)
    return (comp, {"name": "largest component"}, "image")


# given a skeleton, draw white circles on its endpoints
# to fix gaps in skeletonized image
@magic_factory
def patch_skeleton_widget(
    skeleton: "napari.layers.Image", rad: int = 8, and_reskeletonize: bool = False
) -> "napari.types.LayerDataTuple":
    dimensions = skeleton.data.shape
    data = skeleton.data
    datanew = skeleton.data.astype(int)

    # iterate through every point and check its number of neighbors
    # if 1 neighbor, mark it as an endpoint
    for i in range(1, dimensions[0] - 2):
        for j in range(1, dimensions[1] - 2):
            curr = data[i][j]
            if curr > 0:
                # get neighboring pixels
                #   a  b  c
                # 1
                # 2    x
                # 3

                a2 = data[i - 1, j]
                b1 = data[i, j - 1]
                b3 = data[i, j + 1]
                c2 = data[i + 1, j]

                a1 = data[i - 1, j - 1]
                a3 = data[i - 1, j + 1]
                c1 = data[i + 1, j - 1]
                c3 = data[i + 1, j + 1]

                # combine into array and sum all entries. if the sum is 1, then there is one neighbor
                arr = [a1, a2, a3, b1, b3, c1, c2, c3]
                if sum(arr) == 1:
                    # draw circle on endpoint
                    ellipse = skimage.draw.ellipse(i, j, rad, rad, dimensions)
                    datanew[ellipse[0], ellipse[1]] = 1

    result = (
        skimage.morphology.skeletonize(datanew.astype(bool), method="zhang")
        if and_reskeletonize
        else datanew
    )
    return (result, {"name": "patched skeleton"}, "image")
