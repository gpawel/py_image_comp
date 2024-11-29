from PIL import Image
import imagehash
import numpy as np
from image_comparison.abstract_image_comparator import AbstractImageComparison


###########################
# THIS MODULE CONTAINS IMAGE COMPARISON UTILITY
# BASED ON "IMAGEHASH" LIBRARY
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

    # CLASS CONSTRUCTOR
    def __int__(self, img_path_1, img_path_2):
        super().__init__(img_path_1, img_path_2)

    # COMPARE IMAGES USING AVERAGE HASH
    def compare_images_average_hash(self):
        return get_hashes_difference(self.image_path_1, self.image_path_2, imagehash.average_hash)

    # COMPARE IMAGES USING PERCEPTUAL HASH
    def compare_images_perceptual_hash(self):
        return get_hashes_difference(self.image_path_1, self.image_path_2, imagehash.phash)

    # COMPARE IMAGES USING IMAGES DIFFERENCE HASH
    def compare_images_difference_hash(self):
        return get_hashes_difference(self.image_path_1, self.image_path_2, imagehash.dhash)

    # COMPARE IMAGES BY WAVELET HASH
    def compare_images_wavelet_hash(self):
        return get_hashes_difference(self.image_path_1, self.image_path_2, imagehash.whash)