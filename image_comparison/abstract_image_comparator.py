import numpy as np


def check_image_loaded(img, image_path) -> np.ndarray:
    if img is None:
        raise ValueError("Error loading image from: " + image_path)
    return img


class AbstractImageComparison:
    def __init__(self, image_path_1, image_path_2):
        self.image_path_1 = image_path_1
        self.image_path_2 = image_path_2

