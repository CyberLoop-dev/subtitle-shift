import unittest
from main import shift_srt, validate_srt


SAMPLE = "1\n00:00:01,000 --> 00:00:02,500\nHello\n\n2\n00:00:03,000 --> 00:00:04,000\nWorld\n"


class SubtitleTests(unittest.TestCase):
    def test_positive_shift_preserves_text(self):
        result = shift_srt(SAMPLE, 1250)
        self.assertIn("00:00:02,250 --> 00:00:03,750", result)
        self.assertIn("Hello", result)

    def test_negative_shift_clamps_at_zero(self):
        result = shift_srt(SAMPLE, -1500)
        self.assertIn("00:00:00,000 --> 00:00:01,000", result)

    def test_detects_reversed_cue_order(self):
        bad = "1\n00:00:04,000 --> 00:00:05,000\nA\n\n2\n00:00:01,000 --> 00:00:02,000\nB\n"
        self.assertTrue(any("chronological" in issue for issue in validate_srt(bad)))


if __name__ == "__main__":
    unittest.main()
