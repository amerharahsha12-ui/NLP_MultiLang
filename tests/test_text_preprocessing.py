import unittest

from idp_core.text_preprocessing import chunk_text, clean_text


class TestChunkText(unittest.TestCase):

    def test_basic_chunking(self):
        text = "A B C D E F G H"

        expected = [
            "A B C D",
            "D E F G",
            "G H"
        ]

        actual = chunk_text(text, chunk_size=4, overlap=1)

        self.assertEqual(actual, expected)

    def test_no_redundant_chunk(self):
        text = "1 2 3 4 5 6 7 8 9 10"

        actual = chunk_text(text, chunk_size=4, overlap=2)

        self.assertEqual(len(actual), 4)

    def test_invalid_chunk_size(self):
        text = "Hello world"

        with self.assertRaises(ValueError):
            chunk_text(text, chunk_size=0, overlap=0)   
    def test_negative_chunk_size(self):
        text = "Hello world"

        with self.assertRaises(ValueError):
            chunk_text(text, chunk_size=-5, overlap=0)   

    def test_negative_overlap(self):
        text = "1 2 3 4 5 6 7 8 9 10"

        with self.assertRaises(ValueError):
            chunk_text(text, chunk_size=5, overlap=-2) 
                
class TestCleanText(unittest.TestCase):

    def test_removes_extra_spaces(self):
        self.assertEqual(clean_text("  Hello   world  "), "Hello world")

    def test_preserves_multilingual_text_and_symbols(self):
        text = "عَقْدٌ: -10%، ٥٠ ر.س؛ don't pay $20! Straße: 25€ — E-Mail £5."
        self.assertEqual(clean_text(text), text)

    def test_normalizes_combining_characters(self):
        self.assertEqual(clean_text("fu\u0308r Cafe\u0301"), "für Café")

    def test_normalizes_whitespace_and_controls(self):
        self.assertEqual(clean_text(" A\tB\nC\r\nD\x00E\u00a0F "),
                         "A B C D E F")

    def test_preserves_joiners_and_diacritics(self):
        text = "عَرَبِيّ a\u200db"
        self.assertEqual(clean_text(text), text)

    def test_empty_text(self):
        for text in ("", " \n\t "):
            with self.subTest(text=text):
                self.assertEqual(clean_text(text), "")

    def test_rejects_non_string(self):
        for text in (None, 42, b"text", ["text"]):
            with self.subTest(text=text):
                with self.assertRaises(TypeError):
                    clean_text(text)

    def test_idempotent(self):
        cleaned = clean_text("  العربية\nEnglish   für -10% €5 \x00 ")
        self.assertEqual(clean_text(cleaned), cleaned)


class TestChunkTextEdgeCases(unittest.TestCase):

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            chunk_text(None)

    def test_rejects_non_integer_parameters(self):
        for size, overlap in ((3.5, 1), (3, 1.0), (True, 0), (3, False)):
            with self.subTest(size=size, overlap=overlap):
                with self.assertRaises(TypeError):
                    chunk_text("a b c", size, overlap)

    def test_rejects_overlap_at_or_above_size(self):
        for overlap in (3, 4):
            with self.subTest(overlap=overlap):
                with self.assertRaises(ValueError):
                    chunk_text("a b c", 3, overlap)

    def test_empty_input(self):
        self.assertEqual(chunk_text(" \n\t"), [])

    def test_short_and_exact_input(self):
        for text in ("a b", "a b c"):
            with self.subTest(text=text):
                self.assertEqual(chunk_text(text, 3, 1), [text])

    def test_zero_overlap_preserves_all_words(self):
        self.assertEqual(chunk_text("a b c d e", 2, 0),
                         ["a b", "c d", "e"])

    def test_multilingual_word_order(self):
        text = "عقد تجاري English text für Straße"
        self.assertEqual(chunk_text(text, 3, 1),
                         ["عقد تجاري English", "English text für", "für Straße"])


if __name__ == "__main__":
    unittest.main()
