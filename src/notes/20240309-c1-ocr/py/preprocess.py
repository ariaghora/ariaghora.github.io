from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage.measure import label


def preprocess(gray_image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    gray_image = cv2.GaussianBlur(gray_image, (3, 3), 0)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(11, 11))
    equalized = clahe.apply(gray_image)

    thresholded = cv2.adaptiveThreshold(
        equalized,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        15,
        15,
    )

    thresholded = cv2.erode(thresholded, np.ones((2, 2)), iterations=1)
    thresholded = cv2.dilate(thresholded, np.ones((2, 2)), iterations=2)

    return thresholded, equalized


def component_rect(labeled_img: np.ndarray, label: int) -> Tuple[int, int, int, int]:
    xs = np.argwhere(labeled_img == label)[:, 0]
    ys = np.argwhere(labeled_img == label)[:, 1]

    row_min, row_max = xs.min(), xs.max()
    col_min, col_max = ys.min(), ys.max()
    h = row_max - row_min + 1
    w = col_max - col_min + 1
    return row_min, col_min, h, w


def get_main_component(binary_img: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    labeled_image, n_labels = label(binary_img, connectivity=2, return_num=True)  # type: ignore

    valid = []
    height, width = binary_img.shape[:2]
    for i in range(1, n_labels + 1):
        _, _, h, w = component_rect(labeled_image, i)
        if h > int(float(height) * (2.0 / 5.0)) and w > width // 2:
            valid.append(i)
            break

    img = np.zeros((height, width))
    img[labeled_image == valid[0]] = 255  # Take only the valid component

    return img, labeled_image


def find_closest_pixel_to_point(pixel_coordiates, reference_point):
    min_idx = ((pixel_coordiates - reference_point) ** 2).sum(1).argmin(0)
    return pixel_coordiates[min_idx]


def get_corners(component) -> np.ndarray:
    """
    Find 4 pixel coordinates closest to each corner
    """
    height, width = component.shape[:2]

    # top-left
    tl_coords = np.argwhere(component[: height // 2, : width // 2] == 255)
    tl_point = find_closest_pixel_to_point(tl_coords, np.array([0, 0]))

    # top-right
    tr_coords = np.argwhere(component[: height // 2, width // 2 :] == 255)
    tr_point = find_closest_pixel_to_point(tr_coords, np.array([0, width])) + np.array(
        [0, width // 2]
    )

    # bottom-left
    bl_coords = np.argwhere(component[height // 2 :, : width // 2] == 255)
    bl_point = find_closest_pixel_to_point(bl_coords, np.array([height, 0])) + np.array(
        [height // 2, 0]
    )

    # bottom-right
    br_coords = np.argwhere(component[height // 2 :, width // 2 :] == 255)
    br_point = find_closest_pixel_to_point(
        br_coords, np.array([height, width])
    ) + np.array([height // 2, width // 2])

    corners = np.array([tl_point, bl_point, tr_point, br_point])
    return corners


def deskew(
    image: np.ndarray, src_coords: np.ndarray, dst_height: int, dst_width: int
) -> np.ndarray:
    # target deskewing corners
    dst_coords = np.array(
        [[0, 0], [0, dst_height], [dst_width, 0], [dst_width, dst_height]]
    ).astype(np.float32)

    mat = cv2.getPerspectiveTransform(src_coords, dst_coords)
    result = cv2.warpPerspective(image, mat, (dst_width, dst_height))
    return result


def end_to_end_preprocess(input_path: str) -> np.ndarray:
    img = cv2.imread(input_path)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    thresholded, equalized = preprocess(gray)

    # get main component
    component, labeled = get_main_component(thresholded)

    # corners
    corners = get_corners(component).astype(np.float32)[:, ::-1]
    deskewed = deskew(equalized, corners, 600, 500)

    return deskewed


if __name__ == "__main__":
    deskewed1 = end_to_end_preprocess("images/train/1.jpeg")
    deskewed2 = end_to_end_preprocess("images/train/2.jpeg")
    deskewed3 = end_to_end_preprocess("images/train/3.jpeg")
    deskewed4 = end_to_end_preprocess("images/train/4.jpeg")
    deskewed5 = end_to_end_preprocess("images/train/5.jpeg")
    deskewed6 = end_to_end_preprocess("images/train/6.jpeg")

    # cv2.imwrite("component.jpeg", component)

    pattern = """
    abc
    def
    """
    fig, ax = plt.subplot_mosaic(pattern, figsize=(8, 8), sharex=True, sharey=True)
    ax["a"].imshow(deskewed1, cmap="gray")
    ax["b"].imshow(deskewed2, cmap="gray")
    ax["c"].imshow(deskewed3, cmap="gray")
    ax["d"].imshow(deskewed4, cmap="gray")
    ax["e"].imshow(deskewed5, cmap="gray")
    ax["f"].imshow(deskewed6, cmap="gray")
    fig.subplots_adjust(wspace=0.1, hspace=0.1)
    plt.show()
    # fig.savefig("../img/main-component-extraction.png")
    # cv2.imwrite("../img/deskewed.jpeg", deskewed)
