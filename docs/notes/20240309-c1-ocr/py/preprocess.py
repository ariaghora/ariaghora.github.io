from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage.measure import label


def preprocess(gray: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    gray = cv2.cvtColor(gray, cv2.COLOR_RGB2GRAY)
    gray = cv2.medianBlur(gray, 3)
    gray = cv2.blur(gray, (3, 3))
    # gray = (gray * 1.1 - 100).clip(0, 255).astype("uint8")


    clahe = cv2.createCLAHE()
    equalized = clahe.apply(gray)

    thresholded = cv2.adaptiveThreshold(
        equalized,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        25,
        25,
    )

    thresholded = cv2.erode(thresholded, np.ones((3, 3)), iterations=1)
    thresholded = cv2.dilate(thresholded, np.ones((3, 3)), iterations=2)

    return thresholded, equalized


def component_rect(labeled_img: np.ndarray, label: int) -> Tuple[int, int, int, int]:
    xs = np.argwhere(labeled_img == label)[:, 0]
    ys = np.argwhere(labeled_img == label)[:, 1]

    row_min, row_max = xs.min(), xs.max()
    col_min, col_max = ys.min(), ys.max()
    h = row_max - row_min + 1
    w = col_max - col_min + 1
    return row_min, col_min, h, w


def get_main_component(bin_img: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    labeled_image, n_labels = label(thresholded, connectivity=2, return_num=True)  # type: ignore

    valid = []
    height, width = bin_img.shape[:2]
    for i in range(1, n_labels + 1):
        _, _, h, w = component_rect(labeled_image, i)
        if h > int(float(height) * (2.0 / 5.0)) and w > width // 2:
            valid.append(i)
            break

    img = np.zeros((height, width))
    img[labeled_image == valid[0]] = 255  # Take only the valid component

    return img, labeled_image


def find_closest_pixel_to_point(px_coords, pt):
    min_idx = ((px_coords - pt) ** 2).sum(1).argmin(0)
    return px_coords[min_idx]


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


if __name__ == "__main__":
    # Read and preprocess
    img = cv2.imread("images/train/2.jpeg")
    thresholded, equalized = preprocess(img)
    cv2.imwrite("gray.jpeg", img.astype(float).mean(-1).astype("uint8"))
    cv2.imwrite("equalized.jpeg", equalized)
    cv2.imwrite("thresholded.jpeg", thresholded)

    # get main component
    component, labeled = get_main_component(thresholded)

    # corners
    corners = get_corners(component)

    cv2.imwrite("component.jpeg", component)
    print(img)

    fig, ax = plt.subplot_mosaic("abcd", figsize=(14, 7))
    ax["a"].imshow(img.astype(float).mean(-1).astype("uint8"), cmap='gray'); ax["a"].set_title("original gray")
    ax["b"].imshow(equalized, cmap='gray'); ax["b"].set_title("histogram-equalized")
    ax["c"].imshow(labeled, cmap='tab20'); ax["c"].set_title("connected components")
    ax["d"].imshow(component, cmap='gray'); ax["d"].set_title("main component")
    plt.tight_layout()
    # plt.show()
    fig.savefig("../img/main-component-extraction.png")
