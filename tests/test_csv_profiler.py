import tempfile
import unittest
from pathlib import Path

from csv_profiler import profile_csv


class ProfileTests(unittest.TestCase):
    def profile(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.csv"
            path.write_text(text, encoding="utf-8")
            return profile_csv(path)

    def test_numeric_missing_and_quoted_text(self):
        result = self.profile('name,score\n"Shah, Devam",10\nAlice,\nAlice,20\n')
        self.assertEqual(result["rows"], 3)
        self.assertEqual(result["columns"]["name"]["distinct"], 2)
        self.assertEqual(
            result["columns"]["score"],
            {
                "type": "numeric",
                "missing": 1,
                "nonmissing": 2,
                "distinct": 2,
                "min": 10.0,
                "max": 20.0,
                "mean": 15.0,
            },
        )

    def test_bom_whitespace_and_blank_lines(self):
        result = self.profile("\ufeff a ,b\n\n1, \n2,\n")
        self.assertEqual(result["rows"], 2)
        self.assertEqual(result["columns"]["b"]["type"], "empty")

    def test_nonfinite_and_mixed_values_are_text(self):
        for value in ["NaN", "inf", "hello"]:
            with self.subTest(value=value):
                result = self.profile(f"x\n1\n{value}\n")
                self.assertEqual(result["columns"]["x"]["type"], "text")
                self.assertNotIn("mean", result["columns"]["x"])

    def test_header_only(self):
        self.assertEqual(self.profile("x,y\n")["rows"], 0)

    def test_invalid_structure(self):
        for text in ["", "a,\n1,2", "a, a\n1,2", "a,b\n1", "a\n1,2"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.profile(text)


if __name__ == "__main__":
    unittest.main()
