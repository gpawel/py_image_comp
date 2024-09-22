import cv2
import numpy as np
from abstract_image_comparator import AbstractImageComparison


class OpenCVImageComparator(AbstractImageComparison):
    def __init__(self, image_path_1, image_path_2):
        super().__init__(image_path_1,image_path_2)

    def compare_images_MSE(self) -> float:
        """
                        Calculate the Mean Squared Error (MSE) between two images.

                        :param image1_path: Path to the first image.
                        :param image2_path: Path to the second image.
                        :return: MSE value representing the similarity between the images. Lower values mean more similar.
                        """
        # Read the images

        image1 = cv2.imread(self.image_path_1, cv2.IMREAD_GRAYSCALE)
        image2 = cv2.imread(self.image_path_2, cv2.IMREAD_GRAYSCALE)

        # Check if images are of the same size
        if image1.shape != image2.shape:
            raise ValueError("Images must have the same dimensions for MSE comparison.")

        # Compute the MSE
        mse_value = float(np.mean((image1.astype("float") - image2.astype("float")) ** 2))
        return mse_value

    def compare_ssim(self) -> float:
        image_1 = cv2.imread(self.image_path_1, cv2.IMREAD_GRAYSCALE)
        image_2 = cv2.imread(self.image_path_2, cv2.IMREAD_GRAYSCALE)
        # Example implementation: using Structural Similarity Index (SSIM)
        score, _ = cv2.compareHist(image_1, image_2, cv2.HISTCMP_CORREL)
        print(f"Comparison score: {score}")
        return score

    import cv2

    def compare_histograms_correlation_grayscale(self):
        # Load images as grayscale
        img1 = self.load_image_greyscale(self.image_path_1)
        img2 = self.load_image_greyscale(self.image_path_2)

        # Check if images are loaded properly
        if img1 is None or img2 is None:
            raise ValueError("Error loading images. Check the file paths.")

        # Calculate histograms
        hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])

        # Normalize histograms
        hist1 = cv2.normalize(hist1, hist1).flatten()
        hist2 = cv2.normalize(hist2, hist2).flatten()

        # Compare histograms using Correlation method
        correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        print(f"Correlation Score (Grayscale): {correlation}")
        return correlation

    def load_image_greyscale(self, image_path) -> np.ndarray:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        return self.__check_image_loaded(img)

    def load_image_colored (self, image_path) -> np.ndarray:
        img = cv2.imread(image_path)
        return self.__check_image_loaded(img)

    def __check_image_loaded(self, img) -> np.ndarray:
        if img is None:
            raise ValueError("Error loading image from: " + image_path)
        return img

