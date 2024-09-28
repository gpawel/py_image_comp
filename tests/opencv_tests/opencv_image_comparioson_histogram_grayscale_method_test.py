from tests.base_tests import BaseTest
from tests.conftest import *

class TestHistogramGrayscaleCompare(BaseTest):

    def test_histogram_greyscale_correlation_identical_image(self, get_identical_image_path):
        img1, img2 = get_identical_image_path
        ratio = self.compare_using_opencv_method(img1, img2, lambda comp: comp.compare_images_histograms_correlation_grayscale())
        assert ratio == 1.0

    def test_histogram_greyscale_correlation_different_images(self, get_different_image_paths):
        img1, img2 = get_different_image_paths
        ratio = self.compare_using_opencv_method(img1, img2, lambda comp: comp.compare_images_histograms_correlation_grayscale())
        assert 0.48 <= ratio <= 0.5

    def test_histogram_greyscale_correlation_scaled_images(self, get_same_image_scaled):
        img1, img2 = get_same_image_scaled
        ratio = self.compare_using_opencv_method(img1, img2, lambda comp: comp.compare_images_histograms_correlation_grayscale())
        assert 0.9 <= ratio <= 1.0
