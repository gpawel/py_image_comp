import pytest

IMAGE_1 = '../../etc/images/test_image_1.jpg'
IMAGE_2 = '../../etc/images/test_image_2.jpg'

IMAGE_3 = '../../etc/images/selection_1.png'
IMAGE_3_LARGER = '../../etc/images/selection_1_large.png'


@pytest.fixture()
def get_identical_image_path():
    return IMAGE_1, IMAGE_1


@pytest.fixture()
def get_different_image_paths():
    return IMAGE_1, IMAGE_2


@pytest.fixture()
def get_same_image_scaled():
    return IMAGE_3, IMAGE_3_LARGER
