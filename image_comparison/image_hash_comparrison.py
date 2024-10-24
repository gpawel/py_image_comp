from PIL import Image
import imagehash
import numpy as np
from image_comparison.abstract_image_comparator import AbstractImageComparison


def load_image(image_path):
    return Image.open(image_path)


def load_two_images(image_path_1, image_path_2) -> tuple:
    img1 = load_image(image_path_1)
    img2 = load_image(image_path_2)
    return img1, img2


def get_difference(hash1: imagehash.ImageHash, hash2: imagehash.ImageHash):
    diff = hash1 - hash2
    print(f"Hash difference is: {diff}")
    return diff


def get_hashes_difference(image_path_1, image_path_2, comparison_method):
    img1, img2 = load_two_images(image_path_1, image_path_2)
    hash1 = comparison_method(img1)
    hash2 = comparison_method(img2)
    return get_difference(hash1, hash2)


class ImageHashComparison(AbstractImageComparison):

    def __int__(self, img_path_1, img_path_2):
        super().__init__(img_path_1, img_path_2)

    def compare_images_average_hash(self):
        img1, img2 = load_two_images(self.image_path_1, self.image_path_2)
        hash1 = imagehash.average_hash(img1)
        hash2 = imagehash.average_hash(img2)
        return get_difference(hash1, hash2)

    def compare_images_perceptual_hash(self):
        img1, img2 = load_two_images(self.image_path_1, self.image_path_2)
        hash1 = imagehash.phash(img1)
        hash2 = imagehash.phash(img2)
        return get_difference(hash1, hash2)

    def compare_images_difference_hash(self):
        img1, img2 = load_two_images(self.image_path_1, self.image_path_2)
        hash1 = imagehash.dhash(img1)
        hash2 = imagehash.dhash(img2)
        return get_difference(hash1, hash2)

    def compare_images_wavelet_hash(self):
        return get_hashes_difference(self.image_path_1, self.image_path_2, imagehash.whash)