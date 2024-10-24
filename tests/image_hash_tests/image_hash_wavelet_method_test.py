from tests.base_tests import BaseTest
from tests.conftest import *


class TestImageHashWaveMethod(BaseTest):

    def test_image_hash_wave_identical_images(self, get_identical_image_path):
        img1, img2 = get_identical_image_path
        diff = self.compare_using_hash_image_method(img1, img2, lambda comp: comp.compare_images_wavelet_hash())
        assert diff == 0
