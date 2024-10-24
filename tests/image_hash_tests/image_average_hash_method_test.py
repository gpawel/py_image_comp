from tests.base_tests import BaseTest
from tests.conftest import *


class TestImageAverageHashMethod(BaseTest):

    def test_image_average_hash_identical_images(self, get_identical_image_path):
        img1, img2 = get_identical_image_path
        diff = self.compare_using_hash_image_method(img1, img2, lambda comp: comp.compare_images_average_hash())
        assert diff == 0

    def test_image_average_hash_different_images(self, get_different_image_paths):
        img1, img2 = get_different_image_paths
        diff = self.compare_using_hash_image_method(img1, img2, lambda comp: comp.compare_images_average_hash())
        assert diff == 29

    def test_image_average_hash_scaled_images(self, get_same_image_scaled):
        img1, img2 = get_same_image_scaled
        diff = self.compare_using_hash_image_method(img1, img2, lambda comp: comp.compare_images_average_hash())
        assert diff == 0

    def test_image_average_hash_same_images_with_small_change(self, get_same_shape_mages_with_small_change):
        img1, img2 = get_same_shape_mages_with_small_change
        diff = self.compare_using_hash_image_method(img1, img2, lambda comp: comp.compare_images_average_hash())
        assert diff == 0
