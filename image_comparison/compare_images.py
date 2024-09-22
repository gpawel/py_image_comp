# image_comparison/compare_images.py
from enum import Enum
import cv2
import numpy as np


class ComparisonMethod(Enum):
    SSIM = 'ssim'
    OPENCV = 'opencv'
    PILLOW = 'pillow'
    SCIKIT = 'scikit'
    MSE = "mse"


class ImageComparison:


    def get_ssim_score(self):
        # Implementation for SSIM
        pass



    def resize_image(self, image, target_size):
        """
        Resize the given image to the target size.

        :param image: The image to resize.
        :param target_size: A tuple representing the target size (width, height).
        :return: Resized image.
        """
        return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)

    def get_mean_squared_error_score(self) -> float:
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

    def get_pillow_score(self):
        # Implementation for Pillow
        pass

    def get_scikit_score(self):
        # Implementation for scikit-image
        pass

    def get_similarity(self, method: ComparisonMethod):
        if method == ComparisonMethod.SSIM:
            return self.get_ssim_score()
        elif method == ComparisonMethod.OPENCV:
            return self.get_mean_squared_error_score()
        elif method == ComparisonMethod.PILLOW:
            return self.get_pillow_score()
        elif method == ComparisonMethod.SCIKIT:
            return self.get_scikit_score()
        else:
            raise ValueError(f"Unknown method: {method}")
