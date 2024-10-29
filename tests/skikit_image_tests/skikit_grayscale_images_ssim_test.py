from tests.base_tests import BaseTest
from tests.conftest import *
from image_comparison.opencv_image_comparator import *


class TestSkiKitGrayscaleImageComparison(BaseTest):

    def test_scikit_ssim_comparison_identical_images(self, get_identical_image_path):
        img1, img2 = get_identical_image_path
        similarity, diff = self.compare_using_scikit_grayscale_ssim_method(img1, img2, lambda comp: comp.compare_grayscale_images_ssim())
        assert similarity == 1.0
        assert diff == 1.0

    def test_scikit_ssim_comparison_scaled_images(self, get_same_image_scaled):
        img1, img2 = get_same_image_scaled
        with pytest.raises(ValueError) as exc_info:
            self.compare_using_scikit_grayscale_ssim_method(img1, img2, lambda comp: comp.compare_grayscale_images_ssim())
        assert str(exc_info.value) == "Input images must have the same dimensions."

    def test_scikit_ssim_comparison_resized_scaled_images(self, get_same_image_scaled):
        img1_p, img2_p = get_same_image_scaled
        img1, img2 = resize_grayscale_to_smaller_images_by_path(img1_p, img2_p)
        similarity, diff_mean = self.compare_using_scikit_grayscale_ssim_method(img1, img2, lambda comp: comp.compare_grayscale_images_ssim())
