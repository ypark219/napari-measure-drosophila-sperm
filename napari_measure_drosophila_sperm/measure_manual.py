import napari
import numpy as np
from magicgui import magic_factory


@magic_factory
def measure_manual(image: "napari.layers.Image"):
    straight = 0
    diagonal = 0
    data = image.data

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

                # not pretty but it works...i think!
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
    # print(straight)
    # print(diagonal)
    result = (straight / 2) + (np.sqrt(2) / 2 * diagonal) # each 2-pixel connection is counted twice
    print(result)
    print(result / 3.06)
