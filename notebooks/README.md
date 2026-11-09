# Preprocessing demo

## Environment and installation

Run these commands from `C:\AI-Projects\NLP_MultiLang` using Python 3.12.10:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install -r requirements-preprocessing.txt
```

The standalone requirements cover preprocessing and notebook execution. The
project's original `requirements.txt` remains unchanged. No private datasets,
model downloads, or network calls are needed by the demo after installation.

## Tests and notebook

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe notebooks/execute_notebook.py
```

Open `preprocessing_demo.ipynb` in VS Code or Jupyter to view its saved outputs.
For interactive Run All, select the project's `.venv` interpreter. The runner
uses its current Python executable explicitly, without installing a global
kernel, executes every code cell, validates the notebook, and saves outputs
only after successful execution. It raises an error on a failed cell.

## Behavior and limits

- `clean_text(text)` requires a string. It applies NFC, replaces control
  characters with spaces, collapses whitespace, and preserves multilingual
  letters, diacritics, punctuation, mathematical signs, currency, and joiners.
  It does not preserve paragraph layout; retain the original document.
- `chunk_text(text, chunk_size=300, overlap=50)` keeps the existing word-based
  interface and validation. It does not count model tokens or detect sentences.
- `preprocess_ocr_image(image_path_or_obj)` accepts a string/PathLike file path,
  a PIL image, or a uint8 NumPy grayscale/BGR/BGRA array. NumPy RGB input must
  first be reordered to BGR or wrapped in a PIL image. Alpha is composited on
  white; output is a grayscale uint8 array. Invalid inputs are rejected.
- The image demo uses a deterministic synthetic document. Mild denoising and
  CLAHE are preprocessing heuristics, not evidence of improved OCR accuracy.
  CER/WER measurement, OCR extraction, PDF ingestion, and RAG are outside this
  submission's scope.

See `../tests/TEST_REPORT.md` for actual test results and historical comparisons.
