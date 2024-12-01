from image_comparison.opencv_image_comparator import *
import cv2
import numpy as np
from image_comparison.abstract_image_comparator import *
from skimage.metrics import structural_similarity as ssim
from skimage.util import img_as_float


def get_channel_axis(img) -> int:
    """
    Utlity method to get image's channel value.
    :param img:
    :return: int value presenting channel number.
    """
    # Print shape to inspect
    print("Image shape:", img.shape)
    # Decide channel_axis based on the shape
    if img.shape[-1] == 3:
        return 2  # Last axis holds the color channels
    elif img.shape[0] == 3:
        return 0  # First axis holds the color channels
    else:
        return -1  # Grayscale image, no separate color channels


def get_data_range(img) -> int:
    """
    Utility method to get image's data range for the image.
    :param img:
    :return: int value presnting image's data range.
    """
    min_val, max_val = np.min(img), np.max(img)
    print("Min value:", min_val)
    print("Max value:", max_val)

    # Determine data_range based on min and max values
    if min_val >= 0 and max_val <= 1:
        return 1
    elif min_val >= 0 and max_val <= 255:
        return 255
    elif min_val >= 0 and max_val <= 65535:
        return 65535
    else:
        # Unusual range, set data_range accordingly
        return max_val - min_val  # Custom range


def convert_image_to_float(img: np.ndarray) -> np.ndarray:
    """
    Utility method that converts image into float form.
    :param img:
    :return: returns image in a fload form of the np.ndarray
    """
    return img.astype(np.float32) / 255.0  # Converts to float and scales to 0-1 range


def _compare_coloured_images_using_ssim(img1: np.ndarray, img2: np.ndarray):
    """
    Utility method to compare two images using ssim algorithm.
    :param img1:
    :param img2:
    :return: tuple containing similarity and mean difference.
    """
    channel_axis_1 = get_channel_axis(img1)
    channel_axis_2 = get_channel_axis(img2)

    # Check if both images have the same channel axis
    if channel_axis_1 != channel_axis_2:
        raise ValueError("The two images have different channel axes, cannot compare")

    # Convert images to float after determining channel axis
    img1_float = convert_image_to_float(img1)
    img2_float = convert_image_to_float(img2)

    # Verify that shape is unchanged after conversion (optional)
    if img1_float.shape != img1.shape or img2_float.shape != img2.shape:
        raise ValueError("Image shape changed after conversion to float.")

    data_range_1 = get_data_range(img1)
    data_range_2 = get_data_range(img2)

    if data_range_1 != data_range_2:
        raise ValueError("Data ranges of the images are different")

    similarity, diff = ssim(img1_float, img2_float, full=True,
                            win_size=3, channel_axis=channel_axis_1, data_range=data_range_1)  # Use multichannel=True for color
    mean_diff = np.mean(diff)  # Assuming 'diff' is the output from the SSIM function
    # mean_diff closer to 0 indicates greater difference
    return similarity, mean_diff


class SciKitImageComparator(AbstractImageComparison):
    """
    Class presenting several methods to compare images using SciKit library.
    """
    def __init__(self, img_path_1: str, img_path_2: str):
        super().__init__(img_path_1, img_path_2)

    def compare_grayscale_images_ssim(self) -> tuple:
        """
        This method compares grayscale images using _compare_coloured_images_using_ssim method.
        :return: tuple containing similarity and mean difference.
        """
        img1 = load_image_greyscale(self.image_path_1)
        img2 = load_image_greyscale(self.image_path_2)
        similarity, diff = ssim(img1, img2, full=True)
        mean_diff = np.mean(diff) # Assuming 'diff' is the output from the SSIM function
        # mean_diff closer to 0 indicates greater difference
        return similarity, mean_diff

    def compare_grayscale_resized_images_ssim(self) -> tuple:
        """
        This method compares grayscale images re-sized to the image with the smallest dimensions.
        This method calls _compare_coloured_images_using_ssim.

        :return: tuple containing similarity and mean difference.
        """
        img1 = load_image_greyscale(self.image_path_1)
        img2 = load_image_greyscale(self.image_path_2)

        img1, img2 = resize_to_smaller_image(img1, img2)

        similarity, diff = ssim(img1, img2, full=True)
        mean_diff = np.mean(diff) # Assuming 'diff' is the output from the SSIM function
        # mean_diff closer to 0 indicates greater difference
        return similarity, mean_diff

    def compare_coloured_images_ssim(self) -> tuple:
        """
        This method calls  _compare_coloured_images_using_ssim method for coloured images.
        :return: tuple containing similarity and mean difference.
        """
        img1 = load_image_colored(self.image_path_1)
        img2 = load_image_colored(self.image_path_2)
        return _compare_coloured_images_using_ssim(img1, img2)

    def compare_coloured_resized_images_ssim(self) -> tuple:
        """
        This method calls _compare_coloured_images_using_ssim method for coloured, re-sized images.
        :return: tuple containing similarity and mean difference.
        """
        img1 = load_image_colored(self.image_path_1)
        img2 = load_image_colored(self.image_path_2)
        img1, img2 = resize_to_smaller_image(img1, img2)
        return _compare_coloured_images_using_ssim(img1, img2)
