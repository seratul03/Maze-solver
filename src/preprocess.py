import cv2
import numpy as np


def binarize_image(gray_img: np.ndarray, invert: bool = False):
    """
    Convert grayscale maze image to binary (black & white).

    Args:
        gray_img (np.ndarray): Grayscale image
        invert (bool): Whether to invert binary image

    Returns:
        binary_img (np.ndarray): Binary image (0 or 255)
    """
    _, binary_img = cv2.threshold(
        gray_img,
        127,
        255,
        cv2.THRESH_BINARY
    )

    if invert:
        binary_img = cv2.bitwise_not(binary_img)

    return binary_img