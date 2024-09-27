import cv2
import numpy as np
from image_comparison.abstract_image_comparator import AbstractImageComparison


def check_image_loaded(img, image_path) -> np.ndarray:
    if img is None:
        raise ValueError("Error loading image from: " + image_path)
    return img


def load_image_colored (image_path) -> np.ndarray:
    img = cv2.imread(image_path)
    return check_image_loaded(img, image_path)


def resize_image_keep_aspect_ratio(image: np.ndarray, new_width=None, new_height=None) -> np.ndarray:
    """
    Resizes an image (ndarray) while keeping the aspect ratio.

    :param image: The image as a numpy ndarray.
    :param new_width: Desired width (optional).
    :param new_height: Desired height (optional).
    :return: Resized image with aspect ratio preserved.
    """
    if image is None or not isinstance(image, np.ndarray):
        raise ValueError("Invalid image provided. Ensure it is a valid numpy ndarray.")

    # Get original dimensions
    original_height, original_width = image.shape[:2]

    # If neither width nor height is specified, return the original image
    if new_width is None and new_height is None:
        return image

    # Calculate aspect ratio
    aspect_ratio = original_width / original_height

    # If only new width is provided
    if new_width and not new_height:
        new_height = int(new_width / aspect_ratio)

    # If only new height is provided
    elif new_height and not new_width:
        new_width = int(new_height * aspect_ratio)

    # Resize the image with the new dimensions
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized_image


def load_image_greyscale(image_path) -> np.ndarray:
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return check_image_loaded(img, image_path)


def resize_to_smaller_image(image_1: np.ndarray, image_2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Resize the larger image to match the exact dimensions of the smaller image.
    If both images are the same size, return them unchanged.

    :param image_1: image one as ndarray
    :param image_2: another image as ndarray
    :return: Tuple of resized (or original) images
    """

    # Get dimensions of the images
    height1, width1 = image_1.shape[:2]
    height2, width2 = image_2.shape[:2]

    # Check if images are the same size
    if (width1, height1) == (width2, height2):
        return image_1, image_2

    # Resize one of the images to match the dimensions of the other
    if width1 > width2 or height1 > height2:
        img1_resized = resize_image_keep_aspect_ratio(image_1, width2, height2)
        return img1_resized, image_2
    else:
        img2_resized = resize_image_keep_aspect_ratio(image_2, width1, height1)
        return image_1, img2_resized


class OpenCVImageComparator(AbstractImageComparison):
    def __init__(self, image_path_1, image_path_2):
        super().__init__(image_path_1,image_path_2)

    def compare_images_mse(self) -> float:
        """
        Calculate the Mean Squared Error (MSE) between two images.
        :return: MSE value representing the similarity between the images. Lower values mean more similar.
        """
        # Read the images
        image1 = load_image_greyscale(self.image_path_1)
        image2 = load_image_greyscale(self.image_path_2)

        image1, image2 = resize_to_smaller_image(image1, image2)
        # Compute the MSE
        mse_value = float(np.mean((image1.astype("float") - image2.astype("float")) ** 2))
        return mse_value

    # def compare_images_ssim(self) -> float:
    #     # Load images
    #     image_1 = load_image_greyscale(self.image_path_1)
    #     image_2 = load_image_greyscale(self.image_path_2)
    #     # Resize the images to the smaller one
    #     image_1, image_2 = resize_to_smaller_image(image_1, image_2)
    #     # Example implementation: using Structural Similarity Index (SSIM)
    #     score, _ = ssim(image1, image2, full=True)
    #     print(f"Comparison score: {score}")
    #     return score

    def compare_images_histograms_correlation_grayscale(self) -> float:
        '''
        Correlation (cv2.HISTCMP_CORREL):
        Interpretation: Higher values indicate more similarity.
        :return:  Range: -1 to 1 (1 indicates perfect correlation, 0 indicates no correlation, -1 indicates perfect negative correlation).
        '''
        # Load images as grayscale
        image_1 = load_image_greyscale(self.image_path_1)
        image_2 = load_image_greyscale(self.image_path_2)

        # Resize the images to the smaller one
        image_1, image_2 = resize_to_smaller_image(image_1, image_2)
        # Calculate histograms
        hist1 = cv2.calcHist([image_1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([image_2], [0], None, [256], [0, 256])

        # Normalize histograms
        hist1 = cv2.normalize(hist1, hist1).flatten()
        hist2 = cv2.normalize(hist2, hist2).flatten()

        # Compare histograms using Correlation method
        correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        print(f"Correlation Score (Grayscale): {correlation}")
        return correlation

    def compare_images_histograms_correlation_colored(self) -> float:
        '''
        Correlation (cv2.HISTCMP_CORREL):
        Interpretation: Higher values indicate more similarity.
        :return:  Range: -1 to 1 (1 indicates perfect correlation, 0 indicates no correlation, -1 indicates perfect negative correlation).
        '''
        # Load images as colored (BGR)
        image_1 = load_image_colored(self.image_path_1)
        image_2 = load_image_colored(self.image_path_2)

        # Resize the images to the smaller one
        image_1, image_2 = resize_to_smaller_image(image_1, image_2)

        # Calculate histograms for each BGR channel
        hist1_b = cv2.calcHist([image_1], [0], None, [256], [0, 256])
        hist1_g = cv2.calcHist([image_1], [1], None, [256], [0, 256])
        hist1_r = cv2.calcHist([image_1], [2], None, [256], [0, 256])

        hist2_b = cv2.calcHist([image_2], [0], None, [256], [0, 256])
        hist2_g = cv2.calcHist([image_2], [1], None, [256], [0, 256])
        hist2_r = cv2.calcHist([image_2], [2], None, [256], [0, 256])

        # Normalize histograms
        hist1_b = cv2.normalize(hist1_b, hist1_b).flatten()
        hist1_g = cv2.normalize(hist1_g, hist1_g).flatten()
        hist1_r = cv2.normalize(hist1_r, hist1_r).flatten()

        hist2_b = cv2.normalize(hist2_b, hist2_b).flatten()
        hist2_g = cv2.normalize(hist2_g, hist2_g).flatten()
        hist2_r = cv2.normalize(hist2_r, hist2_r).flatten()

        # Compare histograms for each channel using Correlation method
        correlation_b = cv2.compareHist(hist1_b, hist2_b, cv2.HISTCMP_CORREL)
        correlation_g = cv2.compareHist(hist1_g, hist2_g, cv2.HISTCMP_CORREL)
        correlation_r = cv2.compareHist(hist1_r, hist2_r, cv2.HISTCMP_CORREL)

        # Average correlation score across all channels
        average_correlation = (correlation_b + correlation_g + correlation_r) / 3
        print(f"Correlation Score (Colored): {average_correlation}")
        return average_correlation

