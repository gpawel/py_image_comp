import pytest
from image_comparison.opencv_image_comparator import OpenCVImageComparator

IMAGE_1 = '../etc/images/test_image_1.jpg'
IMAGE_2 = '../etc/images/test_image_2.jpg'

IMAGE_3 = '../etc/images/selection_1.png'
IMAGE_3_LARGER = '../etc/images/selection_1_large.png'


@pytest.fixture()
def get_identical_image_path():
    return IMAGE_1, IMAGE_1


@pytest.fixture()
def get_different_image_paths():
    return IMAGE_1, IMAGE_2


@pytest.fixture()
def get_same_image_scaled():
    return IMAGE_3, IMAGE_3_LARGER


def test_histogram_greyscale_correlation_identical_image(get_identical_image_path):
    img1, img2 = get_identical_image_path
    comparator = OpenCVImageComparator(img1, img2)
    ratio = comparator.compare_images_histograms_correlation_grayscale()
    print(f"\nHistogram grayscale comparison ratio is: {ratio}")
    assert ratio == 1.0


def test_histogram_greyscale_correlation_different_images(get_different_image_paths):
    img1, img2 = get_different_image_paths
    comparator = OpenCVImageComparator(img1,img2)
    ratio = comparator.compare_images_histograms_correlation_grayscale()
    print(f"\nHistogram grayscale comparison ratio is: {ratio}")
    assert 0.48 <= ratio <= 0.5


def test_histogram_greyscale_correlation_scaled_images(get_same_image_scaled):
    img1, img2 = get_same_image_scaled
    comparator = OpenCVImageComparator(img1,img2)
    ratio = comparator.compare_images_histograms_correlation_grayscale()
    print(f"\nHistogram grayscale comparison ratio is: {ratio}")
    assert 0.9 <= ratio <= 1