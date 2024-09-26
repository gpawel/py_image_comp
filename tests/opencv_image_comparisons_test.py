import pytest
from image_comparison.opencv_image_comparator import OpenCVImageComparator

IMAGE_1 = '../etc/images/test_image_1.jpg'
IMAGE_2 = '../etc/images/test_image_2.jpg'

IMAGE_3 = '../etc/images/selection_1.png'
IMAGE_3_LARGER = '../etc/images/selection_1_large.png'


# Fixtures that provide image paths for the tests
@pytest.fixture
def identical_image_paths():
    return IMAGE_1, IMAGE_1


@pytest.fixture
def different_image_paths():
    return IMAGE_1, IMAGE_2

@pytest.fixture()
def same_image_scaled():
    return IMAGE_3, IMAGE_3_LARGER


# Unit tests constructing their own ImageComparison instance
def test_mse_identical_images(identical_image_paths):
    image1_path, image2_path = identical_image_paths
    comparator = OpenCVImageComparator(image1_path, image2_path)
    rate = comparator.compare_images_mse()
    print(f"\ncomparison rate: {rate}")
    assert rate == 0  # Expecting MSE to be 0 for identical images


def test_mse_different_images(different_image_paths):
    image1_path, image2_path = different_image_paths
    comparator = OpenCVImageComparator(image1_path, image2_path)
    rate = comparator.compare_images_mse()
    print(f"\ncomparison rate: {rate}")
    assert rate > 0  # MSE should be greater than 0 for different images


def test_original_and_scaled(same_image_scaled):
    image1_path, image2_path = same_image_scaled
    comparator = OpenCVImageComparator(image1_path, image2_path)
    rate = comparator.compare_images_mse()
    print(f"\ncomparison rate: {rate}")
    assert rate == 0  # MSE should be 0 for the same but scaled images

