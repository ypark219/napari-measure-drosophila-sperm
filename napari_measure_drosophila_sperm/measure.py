import napari
import numpy as np
import skimage as ski
from magicgui import magic_factory
from napari.utils.notifications import show_info

@magic_factory
def measure(
    image: "napari.layers.Image",
    true_val: float=0.0,
) -> "napari.types.LayerDataTuple":
    length = ski.measure.perimeter(image.data) / 3.06
    #print(image.data.sum())
    #print(np.count_nonzero(image.data))
    # observed = ski.measure.perimeter(image.data) / 3.06
    # print(observed)
    # print((abs(observed - true_val) / true_val) * 100)

    viewer = napari.current_viewer()

    features = {
        'length': np.array([length]),
    }

    text = {
        'string': 'Length is {length:.2f} micrometers',
        'size': 16,
        'color': 'red',
        'translation': np.array([-30, 0]),
    }

    #points_layer = viewer.add_points(
    viewer.add_points(
        # TODO: move this point somewhere else
        np.array([[len(image.data) / 2, len(image.data[0]) / 2]]),
        features=features,
        text=text,
        size=16,
        face_color='black',
    )

    print(length)

    return None
