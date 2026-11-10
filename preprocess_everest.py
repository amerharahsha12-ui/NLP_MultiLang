"""Conservative OCR dataset preprocessing for the EvArEST recognition dataset.

Run: pip install -U datasets pillow pyarrow
     python preprocess_everest.py

Only the first MAX_SAMPLES records of train_real.parquet are processed by default.
"""

import csv
import hashlib
import io
import json
import re
import unicodedata
from pathlib import Path

from datasets import load_dataset
from PIL import Image, ImageOps

DATASET_ID = "Melaraby/EvArEST-dataset-for-Arabic-scene-text-recognition"
PARQUET_FILE = "train_real.parquet"
MAX_SAMPLES = 200          # Start small; set to None to process all rows in this file.
MAX_IMAGE_SIDE = 1600      # Resize only overly large images; never upscale small text.
OUTPUT_DIR = Path("processed_dataset")


def clean_text(text):
    """Conservatively normalize OCR labels without deleting valid characters."""
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\ufeff", "").replace("\u200b", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def open_image(value):
    """Decode an image stored as PIL, raw bytes, or a Hugging Face image mapping."""
    if isinstance(value, Image.Image):
        return ImageOps.exif_transpose(value.copy()).convert("RGB")

    if isinstance(value, dict):
        value = value.get("bytes") or value.get("path")

    if isinstance(value, (bytes, bytearray)):
        source = io.BytesIO(value)
    elif isinstance(value, (str, Path)):
        source = value
    else:
        raise ValueError("Unsupported or missing image value")

    with Image.open(source) as img:
        return ImageOps.exif_transpose(img).convert("RGB")


def preprocess_image(image):
    """Keep visual details; downscale only if image is extremely large."""
    if image.width <= 0 or image.height <= 0:
        raise ValueError("Invalid image size")
    if max(image.size) > MAX_IMAGE_SIDE:
        image.thumbnail((MAX_IMAGE_SIDE, MAX_IMAGE_SIDE), Image.Resampling.LANCZOS)
    return image


def main():
    data_url = f"hf://datasets/{DATASET_ID}/{PARQUET_FILE}"
    dataset = load_dataset(
        "parquet",
        data_files={"train": data_url},
        split="train",
        streaming=True,
    )

    image_dir = OUTPUT_DIR / "images"
    image_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "dataset": DATASET_ID,
        "source_file": PARQUET_FILE,
        "examined": 0,
        "saved": 0,
        "empty_labels": 0,
        "invalid_images": 0,
        "changed_labels": 0,
        "duplicate_images": 0,
        "conflicting_duplicate_labels": 0,
    }
    seen_images = {}
    columns = [
        "record_id", "image_name", "image_path", "original_text",
        "cleaned_text", "width", "height", "duplicate_image",
        "conflicting_label",
    ]

    rows = dataset if MAX_SAMPLES is None else dataset.take(MAX_SAMPLES)
    with (OUTPUT_DIR / "labels.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()

        for idx, row in enumerate(rows):
            report["examined"] += 1
            original = row.get("full_text")
            cleaned = clean_text(original)

            if not cleaned:
                report["empty_labels"] += 1
                continue

            try:
                image = preprocess_image(open_image(row.get("image_bytes")))
            except (OSError, ValueError, TypeError) as exc:
                report["invalid_images"] += 1
                print(f"Skipping row {idx}: {exc}")
                continue

            # Hash the actual pixel data to flag repeated images.
            image_hash = hashlib.sha256(
                f"{image.width}x{image.height}:".encode() + image.tobytes()
            ).hexdigest()
            is_duplicate = image_hash in seen_images
            conflict = is_duplicate and seen_images[image_hash] != cleaned
            if is_duplicate:
                report["duplicate_images"] += 1
            if conflict:
                report["conflicting_duplicate_labels"] += 1
            else:
                seen_images.setdefault(image_hash, cleaned)

            image_path = image_dir / f"sample_{idx:06d}.png"
            image.save(image_path, format="PNG")

            writer.writerow({
                "record_id": idx,
                "image_name": str(row.get("image_name") or ""),
                "image_path": image_path.as_posix(),
                "original_text": original,
                "cleaned_text": cleaned,
                "width": image.width,
                "height": image.height,
                "duplicate_image": is_duplicate,
                "conflicting_label": conflict,
            })
            report["saved"] += 1
            if original != cleaned:
                report["changed_labels"] += 1

    (OUTPUT_DIR / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Processing finished! Summary:")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"Outputs: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
