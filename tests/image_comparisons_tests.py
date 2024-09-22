# tests/test_comparison.py
import pytest
from image_comparison.compare_images import ImageComparison, ComparisonMethod

IMAGE_1 = '../etc/images/test_image_1.jpg'
IMAGE_2 = '../etc/images/test_image_2.jpg'


# Fixtures that provide image paths for the tests
@pytest.fixture
def identical_image_paths():
    return IMAGE_1, IMAGE_1


@pytest.fixture
def different_image_paths():
    return IMAGE_1, IMAGE_2


# Unit tests constructing their own ImageComparison instance
def test_mse_identical_images(identical_image_paths):
    image1_path, image2_path = identical_image_paths
    comparator = ImageComparison(image1_path, image2_path)
    assert comparator.get_mean_squared_error_score() == 0  # Expecting MSE to be 0 for identical images


def test_mse_different_images(different_image_paths):
    image1_path, image2_path = different_image_paths
    comparator = ImageComparison(image1_path, image2_path)
    mse_value = comparator.get_mean_squared_error_score()
    assert mse_value > 0  # MSE should be greater than 0 for different images