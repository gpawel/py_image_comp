import pytest
from image_comparison.opencv_image_comparator import OpenCVImageComparator


class BaseTest:

    def compare_using_opencv_method(self, img1, img2, compare_method):
        comparator = OpenCVImageComparator(img1, img2)
        ratio = compare_method(comparator)
        print(f"\nHistogram grayscale comparison ratio is: {ratio}")
        return ratio
