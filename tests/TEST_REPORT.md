
# Preprocessing Test Report — Text, Chunking, and Images

The latest submission validation is recorded in section 8. Sections 1–7 retain
the earlier chunking evaluation and retest history; their limitations and
file-change statements refer to those earlier tasks.

**Project:** NLP_MultiLang  
**Module:** idp_core/text_preprocessing.py  
**Function:** chunk_text()  
**Testing Framework:** Python unittest  
**Execution Environment:** Python 3.12.10 (verified using Virtual Environment .venv)

## 1. Testing Objective

Evaluate the behavior of `chunk_text()` under normal and invalid inputs without modifying the original implementation.

## 2. Before Fix: Historical Test Results

The following results are preserved from the original report for comparison.
The original execution date and command were not recorded. This historical run
was not repeated against the old implementation during the current retest.

| Test ID | Test Case | Expected Behavior | Actual Behavior | Status |
|---|---|---|---|---|
| TC-001 | Basic Chunking | Correct chunks with overlap | Matches expected chunks | PASS |
| TC-002 | Redundant Chunk | No fully redundant final chunk | Produces 5 chunks instead of 4 | FAIL |
| TC-003 | Zero Chunk Size | Raise ValueError | ValueError raised indirectly by range() | PASS |
| TC-004 | Negative Chunk Size | Raise ValueError | ValueError not raised | FAIL |
| TC-005 | Negative Overlap | Raise ValueError | ValueError not raised | FAIL |

## 3. Before Fix: Historical Test Summary

- Total Tests: 5
- Passed: 2
- Failed: 3
- Test Execution Errors: 0

## 4. Before Fix: Historical Findings

### Finding 1: Redundant Final Chunk

The function produces an additional chunk containing only words already included in the previous chunk.

**Observed:** 5 chunks instead of 4.

**Classification:** Potential design issue. Requires confirmation of expected chunking behavior.

### Finding 2: Missing Validation for Negative Chunk Size

The function does not raise `ValueError` when `chunk_size=-5`.

**Classification:** Input validation defect under the proposed positive-size requirement.

### Finding 3: Missing Validation for Negative Overlap

The function does not raise `ValueError` when `overlap=-2`.

**Classification:** Input validation defect under the proposed nonnegative-overlap requirement.

**Potential impact:** Words may be skipped during document chunking.

## 5. Limitations

These results cover five test cases for one function only. They do not establish the correctness or overall performance of the complete NLP system.

## 6. Original Recommendations

1. Define and enforce valid input constraints.
2. Prevent fully redundant final chunks if this matches project requirements.
3. Repeat all tests after implementing fixes.
4. Extend testing to additional edge cases.

**Source Code Modified:** No  
**Git Commit / Push:** Not performed

## 7. After Fix: Retest Execution

- **Test date:** 2026-11-09 (Asia/Amman)
- **Project directory:** `C:\AI-Projects\NLP_MultiLang`
- **Python executable:** `.\.venv\Scripts\python.exe`
- **Verified Python version:** Python 3.12.10, using `.\.venv\Scripts\python.exe --version`
- **Framework:** Python unittest
- **Command:**

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Actual Results: Before vs. After

| Test ID | Executed Test | Before Fix | After Fix: Actual Result | After Status |
|---|---|---|---|---|
| TC-001 | `test_basic_chunking` | PASS | Expected chunks matched | PASS |
| TC-002 | `test_no_redundant_chunk` | FAIL: 5 chunks instead of 4 | Chunk count equals 4 | PASS |
| TC-003 | `test_invalid_chunk_size` | PASS: indirect ValueError | ValueError raised for chunk_size=0 | PASS |
| TC-004 | `test_negative_chunk_size` | FAIL: no ValueError | ValueError raised for chunk_size=-5 | PASS |
| TC-005 | `test_negative_overlap` | FAIL: no ValueError | ValueError raised for overlap=-2 | PASS |

### Captured Test Output

```text
test_basic_chunking (test_text_preprocessing.TestChunkText.test_basic_chunking) ... ok
test_invalid_chunk_size (test_text_preprocessing.TestChunkText.test_invalid_chunk_size) ... ok
test_negative_chunk_size (test_text_preprocessing.TestChunkText.test_negative_chunk_size) ... ok
test_negative_overlap (test_text_preprocessing.TestChunkText.test_negative_overlap) ... ok
test_no_redundant_chunk (test_text_preprocessing.TestChunkText.test_no_redundant_chunk) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
```

### Retest Summary and Scope

| Metric | Before Fix | After Fix |
|---|---|---|
| Total tests | 5 | 5 |
| Passed | 2 | 5 |
| Failed | 3 | 0 |
| Test execution errors | 0 | 0 |

The retest completed successfully with process exit code **0**. The three
previously failing cases now pass, and both previously passing cases still pass.
This confirms the behavior asserted by these five tests only. The suite does
not cover every requirement or edge case, including non-string input,
non-integer parameters, overlap >= chunk_size, and empty input.

During this retest task, only `tests/TEST_REPORT.md` was edited. No source code
or test files were edited, and no Git commit or push was performed.

## 8. Submission Validation — 2026-11-09 (Asia/Amman)

### Environment and Branch

- Project: `C:\AI-Projects\NLP_MultiLang`
- Verified branch: `feature/wesam-preprocessing`
- Verified interpreter: `.\.venv\Scripts\python.exe`, Python **3.12.10**
- Installed dependencies inside `.venv`; exact direct versions are recorded in
  `requirements-preprocessing.txt`. The original `requirements.txt` is unchanged.
- Original working-tree edits and untracked files were retained. No commit,
  push, reset, or branch switch was performed.

### Changes Implemented

- `clean_text()`: explicit string validation, Unicode NFC normalization,
  control-character replacement, and whitespace collapse. Arabic diacritics,
  English apostrophes, German umlauts/ß, percent/minus signs, currency,
  punctuation, and joiners are retained. Unlike the earlier allowlist, this
  policy does not discard other meaningful Unicode symbols. Line breaks are
  still flattened for compatibility; preserve the source text for layout.
- `chunk_text()`: existing fixes, default parameters, and word-based behavior
  retained; this task adds edge-case coverage without changing its logic.
- `preprocess_ocr_image()`: supports string/PathLike paths, PIL images, and
  uint8 NumPy grayscale/BGR/BGRA arrays. Handles RGB/BGR ordering correctly,
  composites alpha on white, validates inputs, and returns grayscale uint8
  without modifying inputs. Denoising strength is reduced from h=30 to h=10;
  CLAHE settings are retained. This is a heuristic, not a measured OCR gain.
- Added text/chunking and image tests, a multilingual demo notebook, its
  execution helper, and setup/run documentation. Public function signatures
  are unchanged.

### Actual Unit Test Execution

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

| Test Class | Test Method | Actual Result |
|---|---|---|
| TestOCRPreprocessing | test_grayscale_shape_dtype_and_input_unchanged | PASS |
| TestOCRPreprocessing | test_missing_or_invalid_file | PASS |
| TestOCRPreprocessing | test_palette_image_matches_rgb | PASS |
| TestOCRPreprocessing | test_partial_alpha_matches_pil_and_bgra | PASS |
| TestOCRPreprocessing | test_pil_grayscale_matches_array | PASS |
| TestOCRPreprocessing | test_pil_rgb_matches_bgr_array | PASS |
| TestOCRPreprocessing | test_rejects_empty_bad_shape_and_dtype | PASS |
| TestOCRPreprocessing | test_rejects_unsupported_objects | PASS |
| TestOCRPreprocessing | test_single_pixel | PASS |
| TestOCRPreprocessing | test_transparent_images_composite_on_white | PASS |
| TestOCRPreprocessing | test_unicode_path_and_string_path | PASS |
| TestChunkText | test_basic_chunking | PASS |
| TestChunkText | test_invalid_chunk_size | PASS |
| TestChunkText | test_negative_chunk_size | PASS |
| TestChunkText | test_negative_overlap | PASS |
| TestChunkText | test_no_redundant_chunk | PASS |
| TestChunkTextEdgeCases | test_empty_input | PASS |
| TestChunkTextEdgeCases | test_multilingual_word_order | PASS |
| TestChunkTextEdgeCases | test_rejects_non_integer_parameters | PASS |
| TestChunkTextEdgeCases | test_rejects_non_string | PASS |
| TestChunkTextEdgeCases | test_rejects_overlap_at_or_above_size | PASS |
| TestChunkTextEdgeCases | test_short_and_exact_input | PASS |
| TestChunkTextEdgeCases | test_zero_overlap_preserves_all_words | PASS |
| TestCleanText | test_empty_text | PASS |
| TestCleanText | test_idempotent | PASS |
| TestCleanText | test_normalizes_combining_characters | PASS |
| TestCleanText | test_normalizes_whitespace_and_controls | PASS |
| TestCleanText | test_preserves_joiners_and_diacritics | PASS |
| TestCleanText | test_preserves_multilingual_text_and_symbols | PASS |
| TestCleanText | test_rejects_non_string | PASS |
| TestCleanText | test_removes_extra_spaces | PASS |

Captured runner summary:

```text
Ran 31 tests in 0.507s

OK
```

Exit code: **0**. Total: **31 PASS, 0 FAIL, 0 execution errors**.
Parameterized subtests are included within these 31 test methods.

| Stage | Total | PASS | FAIL |
|---|---|---|---|
| Original chunking report (historical) | 5 | 2 | 3 |
| After chunking fixes (historical) | 5 | 5 | 0 |
| After initial whitespace test (previous task) | 6 | 6 | 0 |
| Current submission run | 31 | 31 | 0 |

The previous six tests are included in the current run; 25 methods were added.
Historical results are preserved, not rerun against historical code.

### Scope and Remaining Limitations

This submission implements preprocessing only. It does not include OCR text
extraction, PDF ingestion, deskew, embeddings, or a complete RAG system. Image
examples are synthetic and deterministic. No CER/WER or real-world OCR accuracy
claim is made. Word-based chunks do not enforce model-token limits. Text layout
is flattened, and NumPy image inputs must follow the documented uint8/BGR
contract. These limits do not prevent running the supplied preprocessing demo.

### Actual Notebook Execution and Additional Checks

```powershell
.\.venv\Scripts\python.exe notebooks/execute_notebook.py
```

The first notebook attempt stopped before cell execution because the sandbox
denied creation of the user's IPython configuration directory. After permission
was granted, the same command completed with exit code **0**:

```text
Executed and saved 4 code cells; no errors: C:\AI-Projects\NLP_MultiLang\notebooks\preprocessing_demo.ipynb
```

Independent inspection of the saved notebook confirmed:

- All four code cells executed, with execution counts `[1, 2, 3, 4]`.
- Error outputs: **0**.
- Embedded PNG images: **2** (before and after), both visually inspected.
- Notebook schema validation: successful (`nbformat.validate`).
- The saved environment output identifies Python **3.12.10** and executable
  `C:\AI-Projects\NLP_MultiLang\.venv\Scripts\python.exe`.
- All three language examples, chunking assertions, and PIL/NumPy equivalence
  assertions executed successfully. The synthetic image uses RNG seed 42.

Additional commands executed successfully:

```powershell
.\.venv\Scripts\python.exe -X utf8 main.py
.\.venv\Scripts\python.exe -m pip check
```

The existing entry point completed and produced two multilingual chunks.
Dependency check output: `No broken requirements found.`

### Files Changed or Added in This Stage

| File | Change |
|---|---|
| `idp_core/text_preprocessing.py` | Conservative text normalization and validation; chunking logic retained |
| `idp_core/ocr_preprocessing.py` | Image types, colors, alpha, validation, and milder denoising |
| `tests/test_text_preprocessing.py` | Preserve previous six tests; add text and chunking edge cases |
| `tests/test_ocr_preprocessing.py` | New synthetic image tests |
| `tests/TEST_REPORT.md` | Preserve history; record actual current validation |
| `notebooks/preprocessing_demo.ipynb` | Executed multilingual demo with embedded before/after images |
| `notebooks/execute_notebook.py` | Reproducible execution with the invoking Python interpreter |
| `notebooks/README.md` | Installation, execution, contracts, and limitations |
| `requirements-preprocessing.txt` | Pinned direct dependencies for the tested preprocessing environment |

The `.venv` environment was populated with the required packages. No teammates'
unrelated files were edited or deleted. No Git commit or push was performed.

**Readiness:** The preprocessing code, tests, and executed notebook are ready
for an academic demonstration within the documented scope. This is not a
validation of a complete NLP/OCR system or OCR accuracy on real documents.
