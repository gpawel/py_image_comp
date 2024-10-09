import pytest
import os.path

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CURRENT_DIR)
IMAGES_PATH = os.path.join(ROOT, 'etc', 'images')

IMAGE_1 = os.path.join(IMAGES_PATH, 'test_image_1.jpg')
IMAGE_2 = os.path.join(IMAGES_PATH, 'test_image_2.jpg')

IMAGE_3 = os.path.join(IMAGES_PATH, 'selection_1.png')
IMAGE_3_LARGER = os.path.join(IMAGES_PATH, 'selection_1_large.png')
IMAGE_3_LARGER_SMALL_CHANGE = os.path.join(IMAGES_PATH, 'selection_1_large_with_small_change.png')


@pytest.fixture()
def get_identical_image_path():
    return IMAGE_1, IMAGE_1


@pytest.fixture()
def get_different_image_paths():
    return IMAGE_1, IMAGE_2


@pytest.fixture()
def get_same_image_scaled():
    return IMAGE_3, IMAGE_3_LARGER


@pytest.fixture()
def get_same_shape_mages_with_small_change():
    return IMAGE_3_LARGER, IMAGE_3_LARGER_SMALL_CHANGE
