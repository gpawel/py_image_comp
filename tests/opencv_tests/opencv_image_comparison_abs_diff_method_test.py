from tests.base_tests import BaseTest
from tests.conftest import *

class TestOpenCVAbsDiff(BaseTest):

    def test_abs_diff_identical_images(self, get_identical_image_path):
        img1, img2 = get_identical_image_path
        ratio = self.compare_using_opencv_method(img1, img2, lambda comp: comp.absolute_difference_greyscale())
        abs_diff, mean_diff = ratio
        print(f"abs_dif: {abs_diff}\nmean_diff: {mean_diff}")
        assert abs_diff == 0
        assert mean_diff == 0

    def test_abs_diff_small_changed_images(self, get_same_shape_mages_with_small_change):
        img1, img2 = get_same_shape_mages_with_small_change
        ratio = self.compare_using_opencv_method(img1, img2, lambda comp: comp.absolute_difference_greyscale())
        abs_diff, mean_diff = ratio
        print(f"abs_dif: {abs_diff}\nmean_diff: {mean_diff}")
        assert abs_diff >= 100
        assert 0 <= mean_diff <= 1

    def test_abs_diff_shape_images(self, get_same_image_scaled):
        img1, img2 = get_same_image_scaled
        with pytest.raises(ValueError) as exc_info:
            self.compare_using_opencv_method(img1, img2, lambda comp: comp.absolute_difference_greyscale())

        # Assert the exception message
        assert str(exc_info.value) == "Error: Images must be of the same size and type."

