import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from idp_core.ocr_preprocessing import preprocess_ocr_image


class TestOCRPreprocessing(unittest.TestCase):

    def setUp(self):
        self.gray = np.full((64, 96), 210, dtype=np.uint8)
        cv2.putText(self.gray, "Test", (5, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, 40, 1)
        self.rgb = np.stack((self.gray, self.gray // 2, self.gray // 3), axis=2)

    def test_grayscale_shape_dtype_and_input_unchanged(self):
        original = self.gray.copy()
        result = preprocess_ocr_image(self.gray)
        self.assertEqual(result.shape, self.gray.shape)
        self.assertEqual(result.dtype, np.uint8)
        np.testing.assert_array_equal(self.gray, original)
        self.assertGreater(int(result.max()), int(result.min()))

    def test_pil_rgb_matches_bgr_array(self):
        bgr = self.rgb[:, :, ::-1].copy()
        original = bgr.copy()
        expected = preprocess_ocr_image(bgr)
        actual = preprocess_ocr_image(Image.fromarray(self.rgb))
        np.testing.assert_array_equal(actual, expected)
        np.testing.assert_array_equal(bgr, original)

    def test_pil_grayscale_matches_array(self):
        np.testing.assert_array_equal(
            preprocess_ocr_image(Image.fromarray(self.gray)),
            preprocess_ocr_image(self.gray),
        )

    def test_transparent_images_composite_on_white(self):
        rgba = np.zeros((32, 32, 4), dtype=np.uint8)
        expected = preprocess_ocr_image(np.full((32, 32), 255, np.uint8))
        for image in (rgba, Image.fromarray(rgba)):
            with self.subTest(kind=type(image).__name__):
                np.testing.assert_array_equal(preprocess_ocr_image(image),
                                              expected)

    def test_partial_alpha_matches_pil_and_bgra(self):
        alpha = np.full(self.gray.shape + (1,), 128, np.uint8)
        rgba = np.concatenate((self.rgb, alpha), axis=2)
        bgra = rgba[:, :, [2, 1, 0, 3]]
        np.testing.assert_array_equal(
            preprocess_ocr_image(Image.fromarray(rgba)),
            preprocess_ocr_image(bgra),
        )

    def test_palette_image_matches_rgb(self):
        image = Image.fromarray(self.rgb).convert("P")
        np.testing.assert_array_equal(
            preprocess_ocr_image(image),
            preprocess_ocr_image(image.convert("RGB")),
        )

    def test_unicode_path_and_string_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "صورة_für.png"
            Image.fromarray(self.rgb).save(path)
            expected = preprocess_ocr_image(Image.fromarray(self.rgb))
            for value in (path, str(path)):
                with self.subTest(kind=type(value).__name__):
                    np.testing.assert_array_equal(preprocess_ocr_image(value),
                                                  expected)

    def test_missing_or_invalid_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.png"
            with self.assertRaises(ValueError):
                preprocess_ocr_image(path)
            path.write_bytes(b"not an image")
            with self.assertRaises(ValueError):
                preprocess_ocr_image(path)

    def test_rejects_unsupported_objects(self):
        for value in (None, 42, [[1, 2]]):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    preprocess_ocr_image(value)

    def test_rejects_empty_bad_shape_and_dtype(self):
        for image in (np.empty((0, 3), np.uint8), np.zeros(5, np.uint8),
                      np.zeros((8, 8, 2), np.uint8),
                      np.zeros((8, 8), np.float32),
                      np.zeros((8, 8), np.uint16)):
            with self.subTest(shape=image.shape, dtype=image.dtype):
                with self.assertRaises(ValueError):
                    preprocess_ocr_image(image)

    def test_single_pixel(self):
        result = preprocess_ocr_image(np.array([[100]], np.uint8))
        self.assertEqual(result.shape, (1, 1))
        self.assertEqual(result.dtype, np.uint8)


if __name__ == "__main__":
    unittest.main()
