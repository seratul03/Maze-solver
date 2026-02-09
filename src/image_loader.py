import cv2
import os


def load_image(image_path: str):
    """
    Load a maze image from disk and convert it to grayscale.

    Args:
        image_path (str): Path to the maze image

    Returns:
        gray_img (np.ndarray): Grayscale image
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at: {image_path}")

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Failed to load image. Unsupported or corrupted file.")

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img