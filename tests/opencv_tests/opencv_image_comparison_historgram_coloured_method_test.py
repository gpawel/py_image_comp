from tests.base_tests import BaseTest
from tests.conftest import *


class TestHistogramColouredComparison(BaseTest):

    def test_histogram_coloured_identical_image(self, get_identical_image_path):
        img1, img2 = get_identical_image_path
        ratio = self.compare(img1, img2, lambda comp: comp.compare_images_histograms_correlation_colored())
        assert ratio == 1.0

    def test_histogram_coloured_different_image(self, get_different_image_paths):
        img1, img2 = get_different_image_paths
        ratio = self.compare(img1, img2, lambda comp: comp.compare_images_histograms_correlation_colored())
        assert 0.5 <= ratio <= 0.6

    def test_histogram_coloured_same_scaled_image(self, get_same_image_scaled):
        img1, img2 = get_same_image_scaled
        ratio = self.compare(img1, img2, lambda comp: comp.compare_images_histograms_correlation_colored())
        assert 0.99 <= ratio <= 1.0
