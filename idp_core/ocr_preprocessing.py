from pathlib import Path
import cv2
import numpy as np
from PIL import Image


def preprocess_ocr_image(image_path_or_obj, denoise=False, enhance_contrast=False,
                         denoise_strength=7, array_color_space="RGB", output_rgb=False):

    if array_color_space not in ("RGB", "BGR"):
        raise ValueError("array_color_space must be RGB or BGR")

    if isinstance(denoise_strength, bool) or not isinstance(denoise_strength, (int, float)) or not 0 < denoise_strength <= 30:
        raise ValueError("Invalid denoise strength")

    if isinstance(image_path_or_obj, (str, Path)):
        img = cv2.imread(str(image_path_or_obj), cv2.IMREAD_UNCHANGED)
        color_space = "BGR"
    elif isinstance(image_path_or_obj, Image.Image):
        img = np.array(image_path_or_obj.convert("RGB"))
        color_space = "RGB"
    elif isinstance(image_path_or_obj, np.ndarray):
        img = image_path_or_obj
        color_space = array_color_space
    else:
        raise TypeError("Unsupported image input")

    if img is None or img.size == 0 or img.dtype != np.uint8:
        raise ValueError("Invalid image")

    if img.ndim == 2:
        gray = img.copy()
    elif img.ndim == 3 and img.shape[2] == 1:
        gray = img[:, :, 0].copy()
    elif img.ndim == 3 and img.shape[2] in (3, 4):
        conversion = {
            ("RGB", 3): cv2.COLOR_RGB2GRAY,
            ("BGR", 3): cv2.COLOR_BGR2GRAY,
            ("RGB", 4): cv2.COLOR_RGBA2GRAY,
            ("BGR", 4): cv2.COLOR_BGRA2GRAY,
        }
        gray = cv2.cvtColor(img, conversion[(color_space, img.shape[2])])
    else:
        raise ValueError("Unsupported image shape")

    if denoise:
        gray = cv2.fastNlMeansDenoising(gray, h=float(denoise_strength))

    if enhance_contrast:
        gray = cv2.createCLAHE(
            clipLimit=2.0, tileGridSize=(8, 8)
        ).apply(gray)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB) if output_rgb else gray
