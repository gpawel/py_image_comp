import pytest

from tests.base_tests import BaseTest
from tests.conftest import *
from image_comparison.opencv_image_comparator import *


class TestOpenCVAndSSIMGrayscaleMethod(BaseTest):
    def test_ssim_grayscale_images_comparison(self, get_identical_image_path):
        img1, img2 = get_identical_image_path
        ratio = self.compare_using_opencv_method(img1, img2, lambda comp: comp.compare_images_ssim_gray())
        assert ratio == 1

    def test_ssim_grayscale_same_image_scaled(self, get_same_image_scaled):
        img1, img2 = get_same_image_scaled
        with pytest.raises(ValueError) as exc_info:
            self.compare_using_opencv_method(img1, img2, lambda comp: comp.compare_images_ssim_gray())
            # Assert the exception message
        assert str(exc_info.value) == "Input images must have the same dimensions."

    def test_ssim_greyscale_different_images(self, get_different_image_paths):
        img1, img2 = get_different_image_paths
        with pytest.raises(ValueError) as exc_info:
            self.compare_using_opencv_method(img1, img2, lambda comp: comp.compare_images_ssim_gray())

        assert str(exc_info.value) == "Input images must have the same dimensions."

    def test_ssim_grayscale_same_shame_images_with_small_diff(self, get_same_shape_mages_with_small_change):
        img1, img2 = get_same_shape_mages_with_small_change
        ratio = self.compare_using_opencv_method(img1, img2, lambda comp: comp.compare_images_ssim_gray())
        assert 0.996 <= ratio <= 1

    # =========================

    def test_ssim_coloured_images_comparison(self, get_identical_image_path):
        img1, img2 = get_identical_image_path
        ratio = self.compare_using_opencv_method(img1, img2, lambda comp: comp.compare_images_ssim_colored())
        assert ratio == 1

    def test_ssim_coloured_same_image_scaled(self, get_same_image_scaled):
        img1, img2 = get_same_image_scaled
        with pytest.raises(ValueError) as exc_info:
            self.compare_using_opencv_method(img1, img2, lambda comp: comp.compare_images_ssim_colored())
            # Assert the exception message
        assert str(exc_info.value) == "Input images must have the same dimensions."

    def test_ssim_coloured_different_images(self, get_different_image_paths):
        img1, img2 = get_different_image_paths
        with pytest.raises(ValueError) as exc_info:
            self.compare_using_opencv_method(img1, img2, lambda comp: comp.compare_images_ssim_colored())

        assert str(exc_info.value) == "Input images must have the same dimensions."

    def test_ssim_coloured_same_shame_images_with_small_diff(self, get_same_shape_mages_with_small_change):
        img1, img2 = get_same_shape_mages_with_small_change
        ratio = self.compare_using_opencv_method(img1, img2, lambda comp: comp.compare_images_ssim_colored())
        assert 0.996 <= ratio <= 1




