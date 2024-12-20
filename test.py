import unittest

from translator import ConfigTranslator


class TestConfigTranslator(unittest.TestCase):
    def setUp(self):
        self.sample_config = {
            "NUM": 10,
            "ARR": 'array(1, 2, 3)',
            "CONST": 20
        }
        self.translator = ConfigTranslator(self.sample_config)

    def test_translate(self):
        result = self.translator.translate()
        self.assertIn("NUM <- 10;", result)
        self.assertIn('ARR <- array(1, 2, 3);', result)

    def test_invalid_name(self):
        invalid_config = {"Invalid1": 10}
        with self.assertRaises(ValueError):
            ConfigTranslator(invalid_config).translate()

    def test_invalid_value(self):
        invalid_config = {"NUM": "not_array"}
        with self.assertRaises(ValueError):
            ConfigTranslator(invalid_config).translate()

    def test_evaluate_expression(self):
        self.translator.translate()
        self.assertEqual(self.translator.evaluate_expression("@[NUM]"), 10)

    def test_evaluate_expression_invalid(self):
        with self.assertRaises(ValueError):
            self.translator.evaluate_expression("@[INVALID]")

if __name__ == "__main__":
    unittest.main()