from io import BytesIO
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import requests
from PIL import Image
from sklearn.cluster import KMeans


def load_image(path: str) -> np.ndarray:
    if path.startswith(("http://", "https://")):
        response = requests.get(path)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(path)
    return img


def get_palette(
    img: Image, n_colors: int, resize_shape: Tuple[int, int] = (100, 100)
) -> Tuple[np.ndarray, KMeans]:
    img = np.asarray(img.resize(resize_shape)) / 255.0
    h, w, c = img.shape
    img_arr = img.reshape(h * w, c)

    kmeans = KMeans(n_clusters=n_colors, n_init="auto").fit(img_arr)
    palette = (kmeans.cluster_centers_ * 255).astype(int)

    return palette, kmeans


def quantize_image(image: Image, kmeans: KMeans) -> np.ndarray:
    image_np = np.asarray(image) / 255.0
    h, w, c = image_np.shape

    # Petakan masing-masing pixel ke index cluster terdekat
    flatten = image_np.reshape(h * w, c)
    pixel_rgb_clusters = kmeans.predict(flatten)

    # Kemudian kita bisa memetakan balik dari index cluster ke nilai RGB dari centroid
    image_quantized = kmeans.cluster_centers_[pixel_rgb_clusters]

    return image_quantized.reshape(h, w, c)


if __name__ == "__main__":
    url = "https://assets.mubicdn.net/images/artworks/235968/images-original.png?1621568236"
    image = load_image(url)

    num_colors = 8
    color_palette, kmeans = get_palette(image, num_colors)

    print(color_palette)
    print(color_palette.shape)

    """
    Tampilkan palet warna
    """
    # Urutkan warna palet dari yang paling "terang" (yaitu warna dengan nilai grayscale tertinggi)
    color_palette_sorted = np.array(sorted(color_palette, key=lambda x: x.mean())[::-1])

    plt.imshow(color_palette_sorted[np.newaxis, :, :])
    plt.axis("off")
    plt.show()

    """
    Tampilkan hasil kuantifikasi warna pada gambar
    """

    image_labels = "bcd"
    num_colors = [16, 8, 4]

    layout = """
    ab
    cd
    """

    fig, ax = plt.subplot_mosaic(layout, figsize=(12, 7), sharey=True)
    ax["a"].imshow(image)
    ax["a"].set_title("original")
    ax["a"].axis("off")

    for label, num_color in zip(image_labels, num_colors):
        color_palette, kmeans = get_palette(image, num_color)
        image_quantized = quantize_image(image, kmeans)

        ax[label].imshow(image_quantized)
        ax[label].set_title(f"{num_color} warna")
        ax[label].axis("off")

    plt.tight_layout()
    plt.show()
