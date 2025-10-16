import unittest
from deepseek_zarie_bot import EnhancedDeepSeekZarieBot

class TestEnhancedDeepSeekZarieBot(unittest.TestCase):
    def setUp(self):
        self.bot = EnhancedDeepSeekZarieBot()

    def test_generate_glyph_sequence(self):
        glyphs = self.bot.generate_glyph_sequence("heir_001")
        self.assertIsInstance(glyphs, str)
        self.assertGreater(len(glyphs), 0)

    def test_play_narration(self):
        result = self.bot.play_narration("The Oracle awakens.")
        self.assertIsNone(result)  # Since it prints and returns None

    def test_activate_lineage_ceremony(self):
        ceremony_id = self.bot.activate_lineage_ceremony("heir_001")
        self.assertIsInstance(ceremony_id, str)

    def test_grand_ceremony_override(self):
        outcome = self.bot.grand_ceremony("test", override_vote=True)
        self.assertEqual(outcome["status"], "success")

    def test_send_complex_signal(self):
        signal = {"signal": "test", "confidence": 0.9}
        result = self.bot.send_complex_signal(signal)
        self.assertEqual(result["status"], "processed")

if __name__ == "__main__":
    unittest.main()
