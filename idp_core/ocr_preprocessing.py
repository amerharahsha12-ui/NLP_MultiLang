from os import PathLike

import cv2
import numpy as np
from PIL import Image


def preprocess_ocr_image(image_path_or_obj):
    """
    Prepare an image using grayscale, mild denoising, and CLAHE.

    Accept a path, a PIL image, or a uint8 NumPy array in grayscale,
    BGR, or BGRA order (OpenCV convention). Composite alpha on white.
    Return a two-dimensional uint8 array without modifying the input.
    OCR accuracy improvements must be evaluated on actual documents.
    """
    if isinstance(image_path_or_obj, (str, PathLike)):
        try:
            with Image.open(image_path_or_obj) as image:
                return preprocess_ocr_image(image)
        except OSError as exc:
            raise ValueError("Could not load image from the given path") from exc
    elif isinstance(image_path_or_obj, Image.Image):
        image = image_path_or_obj.convert("RGBA")
        background = Image.new("RGBA", image.size, "white")
        img = np.array(Image.alpha_composite(background, image).convert("RGB"))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    elif isinstance(image_path_or_obj, np.ndarray):
        img = image_path_or_obj
    else:
        raise TypeError("Expected an image path, PIL image, or NumPy array")

    if img.size == 0:
        raise ValueError("Image must not be empty")
    if img.dtype != np.uint8:
        raise ValueError("Image array must have dtype uint8")
    if img.ndim == 2:
        gray = img
    elif img.ndim == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif img.ndim == 3 and img.shape[2] == 4:
        alpha = img[:, :, 3:4].astype(np.float32) / 255
        bgr = np.rint(img[:, :, :3] * alpha + 255 * (1 - alpha))
        gray = cv2.cvtColor(bgr.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    else:
        raise ValueError("Expected grayscale, BGR, or BGRA image array")

    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)

    return enhanced
