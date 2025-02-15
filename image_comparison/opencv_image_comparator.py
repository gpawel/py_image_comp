import cv2
import numpy as np
from image_comparison.abstract_image_comparator import *
from skimage.metrics import structural_similarity as ssim


# THIS MODULE CONTAINS UTILITIES TO COMPARE IMAGES
# USING OPENCV AND SKIIMAGE LIBRARIES
def load_image_colored(image_path) -> np.ndarray:
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
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
    """
    Load image using grayscale mode

    :param image_path: File path to the image to load.
    :return: image loaded as the np.ndarray
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return check_image_loaded(img, image_path)


def resize_grayscale_to_smaller_images_by_path(image_path_1, image_path_2) -> tuple[np.ndarray, np.ndarray]:
    """
    This method re-sizes grayscale images to the smallest image dimensions
    Before re-sizing, the method loads images using grayscale mode
    :param image_path1: File path to the first image
    :param image_path2: File path to the second image
    :return: tuple with images resized to the smaller image
    """
    img1 = load_image_greyscale(image_path_1)
    img2 = load_image_greyscale(image_path_2)
    return resize_to_smaller_image(img1, img2)


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


def abs_diff_images(image1, image2) -> tuple:
    '''
    This method returns total and mean differences between image 1 and image2 as tuple
    :param image1: np.ndarray representation of the first image
    :param image2: np.ndarray representation of the second image
    :return:total and mean differences of the images.
    '''
    if image1.shape != image2.shape:
        raise ValueError("Error: Images must be of the same size and type.")
    abs_diff = cv2.absdiff(image1, image2)
    # Calculate the sum of all absolute differences
    total_diff = np.sum(abs_diff)

    # Optionally, calculate the mean difference (average)
    mean_diff = np.mean(abs_diff)

    # cv2.imshow("Difference", abs_diff)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return total_diff, mean_diff


class OpenCVImageComparator(AbstractImageComparison):
    """
    Thsi class contains methods to calculate image differences, using variety of methods
    provided by OpenCV library.
    """
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

    def compare_images_histograms_correlation_grayscale(self) -> float:
        """
        Correlation (cv2.HISTCMP_CORREL):
        Interpretation: Higher values indicate more similarity.
        :return:  Range: -1 to 1 (1 indicates perfect correlation, 0 indicates no correlation, -1 indicates perfect negative correlation).
        """
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
        """
        Correlation (cv2.HISTCMP_CORREL):
        Interpretation: Higher values indicate more similarity.
        :return:  Range: -1 to 1 (1 indicates perfect correlation, 0 indicates no correlation, -1 indicates perfect negative correlation).
        """
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

    def absolute_difference_greyscale(self) -> tuple:
        """
        Compares two images by using abs_diff method from opencv library.
        This method loads provided images using grayscale loading.
        :return The method will return two numbers:
            1. Total Difference (total_diff):
            0 means the two images are identical, i.e., there are no differences.
            The higher the total difference, the more the images differ.
            The value is the sum of all pixel-wise absolute differences across all channels (for color images) or intensity differences (for grayscale images).

            2. Mean Difference (mean_diff):
            0 means the images are identical.
            A higher mean difference indicates a larger average pixel difference between the two images.
            For 8-bit images, the mean difference is typically in the range of 0 to 255, where 0 means identical and 255 would indicate maximum possible difference for every pixel (which is rare).
        """
        img1 = load_image_greyscale(self.image_path_1)
        img2 = load_image_greyscale(self.image_path_2)
        return abs_diff_images(img1, img2)

    def absolute_difference_coloured(self) -> tuple:
        """
        Compares two images by using abs_diff method from opencv library.
        This method loads provided images using coloured loading.
        :return The method will return two numbers:
            1. Total Difference (total_diff):
            0 means the two images are identical, i.e., there are no differences.
            The higher the total difference, the more the images differ.
            The value is the sum of all pixel-wise absolute differences across all channels (for color images) or intensity differences (for grayscale images).

            2. Mean Difference (mean_diff):
            0 means the images are identical.
            A higher mean difference indicates a larger average pixel difference between the two images.
            For 8-bit images, the mean difference is typically in the range of 0 to 255, where 0 means identical and 255 would indicate maximum possible difference for every pixel (which is rare).
        """
        img1 = load_image_colored(self.image_path_1)
        img2 = load_image_colored(self.image_path_2)
        return abs_diff_images(img1, img2)

    def compare_images_ssim_gray(self):
        """
        This method calculates a score representing images differences.
        This method is loading images using grayscale mode
        :return: image differences as a score value
        """
        # Load the images from the given file paths
        image1 = load_image_greyscale(self.image_path_1)
        image2 = load_image_greyscale(self.image_path_2)

        # Calculate SSIM between the two images
        score, diff = ssim(image1, image2, full=True)
        diff = (diff * 255).astype("uint8")

        print(f"SSIM Score (Grayscale): {score}")

        # Display the difference image
        # cv2.imshow("Difference Image (Grayscale)", diff)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return score

    def compare_images_ssim_colored(self):
        """
        This method calculates a score representing images differences.
        This method is loading images using coloured mode
        :return: image differences as a score value
        """


        # Load the images from the given file paths
        image1 = load_image_colored(self.image_path_1)
        image2 = load_image_colored(self.image_path_2)

        # Convert images to RGB
        image1_rgb = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        image2_rgb = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

        # Calculate SSIM between the two images channel-wise and take the average
        score_r, _ = ssim(image1_rgb[:, :, 0], image2_rgb[:, :, 0], full=True)
        score_g, _ = ssim(image1_rgb[:, :, 1], image2_rgb[:, :, 1], full=True)
        score_b, _ = ssim(image1_rgb[:, :, 2], image2_rgb[:, :, 2], full=True)
        score = (score_r + score_g + score_b) / 3

        print(f"SSIM Score (Colored): {score}")

        return score



