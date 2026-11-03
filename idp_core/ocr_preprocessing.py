import cv2
import numpy as np

def preprocess_ocr_image(image_path_or_obj):
    """
    Image preprocessing pipeline to improve OCR accuracy:
    1. Convert image to grayscale.
    2. Remove noise and artifacts (Denoising).
    3. Enhance contrast (CLAHE) to highlight overlapping characters.
    """
    if isinstance(image_path_or_obj, str):
        img = cv2.imread(image_path_or_obj)
    else:
        img = np.array(image_path_or_obj)
        
    if img is None:
        raise ValueError("Could not load image. Check the file path or format.")
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    denoised = cv2.fastNlMeansDenoising(gray, h=30)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(denoised)
    
    return enhanced
