from image_comparison.opencv_image_comparator import *
import cv2
import numpy as np
from image_comparison.abstract_image_comparator import *
from skimage.metrics import structural_similarity as ssim
from skimage.util import img_as_float


def convert_image_to_float(img: np.ndarray) -> float:
    return img_as_float(img)


class SciKitImageComparator(AbstractImageComparison):

    def __init__(self, img_path_1: str, img_path_2: str):
        super().__init__(img_path_1, img_path_2)

    def compare_grayscale_images_ssim(self) -> tuple:
        img1 = load_image_greyscale(self.image_path_1)
        img2 = load_image_greyscale(self.image_path_2)
        similarity, diff = ssim(img1, img2, full=True)
        mean_diff = np.mean(diff) # Assuming 'diff' is the output from the SSIM function
        # mean_diff closer to 0 indicates greater difference
        return similarity, mean_diff

    def compare_coloured_images_ssim(self) -> tuple:
        img1 = load_image_colored(self.image_path_1)
        img2 = load_image_colored(self.image_path_2)
        img1_float = convert_image_to_float(img1)
        img2_float = convert_image_to_float(img2)
        similarity, diff = ssim(img1_float, img2_float, full=True,
                                multichannel=True)  # Use multichannel=True for color
        mean_diff = np.mean(diff)  # Assuming 'diff' is the output from the SSIM function
        # mean_diff closer to 0 indicates greater difference
        return similarity, mean_diff
