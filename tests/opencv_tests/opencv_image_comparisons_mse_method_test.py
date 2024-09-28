import pytest
from tests.base_tests import BaseTest
from tests.conftest import *


# def __compare(img1, img2) -> float:
#     comparator = OpenCVImageComparator(img1, img2)
#     rate = comparator.compare_images_mse()
#     print(f"\ncomparison rate: {rate}")
#     return rate

class TestMSEImageComparison(BaseTest):

    # Unit opencv_tests constructing their own ImageComparison instance
    def test_mse_identical_images(self, get_identical_image_path):
        img1, img2 = get_identical_image_path
        rate = self.compare(img1, img2, lambda comp: comp.compare_images_mse())
        assert rate == 0  # Expecting MSE to be 0 for identical images

    def test_mse_different_images(self, get_different_image_paths):
        img1, img2 = get_different_image_paths
        rate = self.compare(img1, img2, lambda comp: comp.compare_images_mse())
        assert rate > 0  # MSE should be greater than 0 for different images

    def test_original_and_scaled(self, get_same_image_scaled):
        img1, img2 = get_same_image_scaled
        rate = self.compare(img1,img2, lambda comp: comp.compare_images_mse())
        assert 0.0 <= rate <= 150.0 # MSE should be 0 for the same but scaled images

