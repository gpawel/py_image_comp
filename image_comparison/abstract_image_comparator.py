from abc import ABC, abstractmethod
import numpy as np


class AbstractImageComparison:
    def __init__(self, image_path_1, image_path_2):
        self.image_path_1 = image_path_1
        self.image_path_2 = image_path_2

    @abstractmethod
    def get_image_size(self, image) -> tuple:
        """Method to get the size of an image, returning (height, width)."""
        pass

    @abstractmethod
    def resize_image(self, image) -> np.ndarray:
        """Method to resize an image, returning the resized image."""
        pass


    # @abstractmethod
    # def compare_images(self, image_1, image_2) -> float:
    #     """Method to compare images, returning a similarity score as a float."""
    #     pass




