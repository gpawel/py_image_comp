import pytest
from image_comparison.opencv_image_comparator import OpenCVImageComparator
from image_comparison.image_hash_comparrison import ImageHashComparison


class BaseTest:

    def compare_using_opencv_method(self, image_path_1, image_path_2, compare_method):
        comparator = OpenCVImageComparator(image_path_1, image_path_2)
        ratio = compare_method(comparator)
        print(f"\nHistogram grayscale comparison ratio is: {ratio}")
        return ratio

    def compare_using_hash_image_method(self, image_path_1, image_path_2, comparator_method):
        comparator = ImageHashComparison(image_path_1, image_path_2)
        diff = comparator_method(comparator)
        print(f"\nImage Hash difference is: {diff}")
        return diff
    