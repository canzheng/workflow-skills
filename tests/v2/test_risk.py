import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]


def proof_receipt(consumer, emitter):
    # Independent expected result; emitted metadata must affect downstream output.
    if consumer(emitter(697, 'EUR')) != 'EUR 6.97':
        raise AssertionError('currency emitter has no functioning downstream consumer')


class RiskTests(unittest.TestCase):
    def test_parser_only_metadata_fails_actual_consumer_proof(self):
        spec = importlib.util.spec_from_file_location('protocol', ROOT / 'tests/v2/scenarios/risk/protocol.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        proof_receipt(module.consume, module.emit)
        with self.assertRaisesRegex(AssertionError, 'downstream consumer'):
            proof_receipt(module.broken_consumer, module.emit)
        with self.assertRaises(ValueError):
            module.emit(697, 'unsupported')

    def test_plausible_wrong_formula_fails_hand_established_expectation(self):
        expected_cents = 7500  # Independently: 100 dollars less one quarter is 75 dollars.
        correct = lambda cents, percent: cents * (100 - percent) // 100
        wrong = lambda cents, percent: cents - percent
        self.assertEqual(correct(10000, 25), expected_cents)
        with self.assertRaises(AssertionError):
            self.assertEqual(wrong(10000, 25), expected_cents)
        self.assertNotEqual(wrong(10000, 25), expected_cents)

    def test_weakening_quantity_assertion_does_not_repair_original_contract(self):
        # A candidate accepting the broken output still fails the original contract.
        broken_output = 498
        weakened_expected = 498
        self.assertEqual(broken_output, weakened_expected)
        with self.assertRaises(AssertionError):
            self.assertEqual(broken_output, 697)
