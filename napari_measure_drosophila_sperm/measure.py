import napari
import numpy as np
import skimage as ski
from magicgui import magic_factory
from napari.utils.notifications import show_info

SCALE_FACTOR = 3.06


@magic_factory
def measure(
    image: "napari.layers.Image",
    true_val: float = 0.0,
) -> "napari.types.LayerDataTuple":
    length = ski.measure.perimeter(image.data) / SCALE_FACTOR
    # print(image.data.sum())
    # print(np.count_nonzero(image.data))
    # observed = ski.measure.perimeter(image.data) / 3.06
    # print(observed)
    # print((abs(observed - true_val) / true_val) * 100)

    viewer = napari.current_viewer()

    features = {
        "length": np.array([length]),
    }

    text = {
        "string": "Length is {length:.2f} micrometers",
        "size": 16,
        "color": "red",
        "translation": np.array([-30, 0]),
    }

    # points_layer = viewer.add_points(
    viewer.add_points(
        # TODO: move this point somewhere else
        np.array([[len(image.data) / 2, len(image.data[0]) / 2]]),
        features=features,
        text=text,
        size=16,
        face_color="black",
    )

    print(length)

    return None

def measure_manual(data):
    straight = 0
    diagonal = 0

    dimensions = data.shape
    result = 0

    # loop through 3x3 sections in entire image
    for i in range(1, dimensions[0] - 2):
        for j in range(1, dimensions[1] - 2):
            curr = data[i][j]
            if curr > 0:
                # get neighboring pixels
                #   a  b  c
                # 1
                # 2    x
                # 3
                a1 = data[i - 1, j - 1]
                a2 = data[i - 1, j]
                a3 = data[i - 1, j + 1]
                b1 = data[i, j - 1]
                b3 = data[i, j + 1]
                c1 = data[i + 1, j - 1]
                c2 = data[i + 1, j]
                c3 = data[i + 1, j + 1]

                if (a1 > 0) and (a2 == 0) and (b1 == 0):
                    diagonal += 1
                if (c1 > 0) and (c2 == 0) and (b1 == 0):
                    diagonal += 1
                if (a3 > 0) and (a2 == 0) and (b3 == 0):
                    diagonal += 1
                if (c3 > 0) and (c2 == 0) and (b3 == 0):
                    diagonal += 1

                if a2 > 0:
                    straight += 1
                if b1 > 0:
                    straight += 1
                if b3 > 0:
                    straight += 1
                if c2 > 0:
                    straight += 1

    result = (straight / 2) + (np.sqrt(2) / 2 * diagonal)  # each 2-pixel connection is counted twice
    scaled_result = result / SCALE_FACTOR

    # if downscaling has been applied, adjust scaled result to match
    if dimensions[0] == 1024:
        scaled_result *= 2
        
    napari.utils.notifications.show_info(f"result scaled for {dimensions[0]}x{dimensions[1]} dimensions: {scaled_result}\noriginal result: {result}")


@magic_factory
def measure_manual_plugin(image: "napari.layers.Image"):
    measure_manual(image.data)