import napari
import skimage as ski
from magicgui import magic_factory
# import cv2
import numpy as np
from skimage.morphology import square
from . import util

@magic_factory
def detect_circles(
    image: "napari.layers.Image",
):
    blobs = ski.feature.blob_log(util.greyize(image.data))
    viewer = napari.current_viewer()

    for blob in blobs:
        y, x, sigma = blob

        viewer.add_points(
            np.array([y,x]),
            size=np.sqrt(2)*sigma,
            face_color="red",
        )


# def detect_circles(
#     image: "napari.layers.Image",
#     min_size: int=150,
#     threshold: int=250,
#     dilation_size: int=10,
# ) -> "napari.types.LayerDataTuple":
#     # img = cv2.imread('24708.1_1 at 20X.jpg', cv2.IMREAD_GRAYSCALE)
#     # img = cv2.medianBlur(img, 5)
#     # cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#     # detected_circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1, 20)

#     # img = cv2.imread('24708.1_1 at 20X.jpg', cv2.IMREAD_COLOR)


#     # cv2.waitKey(0)
#     # gray = cv2.cvtColor(image.data, cv2.COLOR_BGR2GRAY)
#     # edged = cv2.Canny(gray, 30, 200)
#     # cv2.waitKey(0)
#     # contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     #print(contours)
#     #print(hierarchy)
#     #print(contours[0])
#     # print(contours[0][0])
#     # print(contours[0][0][0])
#     # print(contours[0][0][0][0])

#     # viewer = napari.current_viewer()

#     # for c in contours:
#     #     poly = []
#     #     for p in c:
#     #         poly.append(p[0])

#     #     viewer.add_shapes(
#     #         poly,
#     #         shape_type='polygon',
#     #         edge_width=5,
#     #         edge_color='coral',
#     #         face_color='purple',
#     #     )


#     # gray = cv2.cvtColor(image.data, cv2.COLOR_BGR2GRAY)

#     # # Blur using 3 * 3 kernel.
#     # #gray_blurred = cv2.blur(gray, (3, 3))

#     # # Apply Hough transform on the blurred image.
#     # detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
#     #     param1=50, param2=30, minRadius=50, maxRadius=60)

#     # print(detected_circles)

#     # viewer = napari.current_viewer()

#     # if detected_circles is not None:
#     #     for circle in detected_circles[0,:]:
#     #         a, b, r = circle[0], circle[1], circle[2]
#     #         ellipse = np.array([[a + r, b + r], [a + r, b - r], [a - r, b - r], [a - r, b + r]])
#     #         viewer.add_shapes(
#     #             ellipse,
#     #             shape_type='ellipse',
#     #             edge_width=5,
#     #             edge_color='coral',
#     #             face_color='purple',
#     #         )


#     data = rgb2gray(image.data > threshold)

#     objects = ski.measure.label(data)
#     large_objects = ski.morphology.remove_small_objects(objects, min_size=min_size)

#     dilated = ski.morphology.dilation(large_objects, square(dilation_size))

#     # new_image = image.data
#     # for i in range(0,len(dilated)):
#     #     for j in range(0,len(dilated[i])):
#     #         #if large_objects[i][j][0] != 0 and large_objects[i][j][1] != 0 and large_objects[i][j][2] != 0:
#     #         if dilated[i][j] != 0:
#     #             new_image[i][j] = [0,0,0]


#     # print(image.data)
#     # data = gray2rgb(rgb2gray(image.data > threshold))
#     # # data = threshed
#     # # for i in range(0,len(threshed)):
#     # #     for j in range(0,len(threshed[i])):
#     # #         if threshed[i][j] == 0:
#     # #             data[i][j] = [[0,0,0]]
#     # #         else:
#     # #             data[i][j] = [[255,255,255]]
#     # print(data)
#     # gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
#     # # Apply Hough transform on the blurred image.
#     # detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
#     #     param1=50, param2=30, minRadius=20, maxRadius=100)

#     # print(detected_circles)

#     # viewer = napari.current_viewer()

#     # if detected_circles is not None:
#     #     for circle in detected_circles[0,:]:
#     #         a, b, r = circle[0], circle[1], circle[2]
#     #         ellipse = np.array([[a + r, b + r], [a + r, b - r], [a - r, b - r], [a - r, b + r]])
#     #         viewer.add_shapes(
#     #             ellipse,
#     #             shape_type='ellipse',
#     #             edge_width=5,
#     #             edge_color='coral',
#     #             face_color='purple',
#     #         )


#     # contours, hierarchy = cv2.findContours(large_objects, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     # print(contours)
#     # print(hierarchy)
#     # print(contours[0])
#     # print(contours[0][0])
#     # print(contours[0][0][0])
#     # print(contours[0][0][0][0])

#     # viewer = napari.current_viewer()

#     # for c in contours:
#     #     poly = []
#     #     for p in c:
#     #         poly.append(p[0])

#     #     viewer.add_shapes(
#     #         poly,
#     #         shape_type='polygon',
#     #         edge_width=5,
#     #         edge_color='coral',
#     #         face_color='purple',
#     #     )

#     return (dilated, {"name":"circles"}, "image")


@magic_factory
def remove_circles(
    threshed_image: "napari.layers.Image",
    original_image: "napari.layers.Image",
    min_size: int = 150,
    threshold: int = 250,
    dilation_size: int = 10,
) -> "napari.types.LayerDataTuple":
    threshed = rgb2gray(original_image.data > threshold)
    objects = ski.measure.label(threshed)
    large_objects = ski.morphology.remove_small_objects(objects, min_size=min_size)
    dilated = ski.morphology.dilation(large_objects, square(dilation_size))

    new_image = threshed_image.data
    for i in range(0, len(dilated)):
        for j in range(0, len(dilated[i])):
            if dilated[i][j] != 0:
                new_image[i][j] = 0

    return (new_image, {"name": "circles removed"}, "image")
