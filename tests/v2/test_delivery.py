import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = ROOT / 'tests/v2/scenarios/delivery'


def load_cart(phase):
    spec = importlib.util.spec_from_file_location('cart_' + phase, FIXTURE / phase / 'cart.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DeliveryTests(unittest.TestCase):
    def test_original_bug_is_caught_by_preserved_independent_expectation(self):
        before, after = load_cart('before'), load_cart('after')
        lines = [(199, 2), (299, 1)]
        # Independent hand arithmetic, not recomputed with the implementation.
        self.assertEqual(before.total(lines), 498)
        self.assertNotEqual(before.total(lines), 697)
        self.assertEqual(after.total(lines), 697)

    def test_ordinary_feature_consumes_config_and_rejects_invalid_values(self):
        cart = load_cart('after')
        self.assertEqual(cart.total([(199, 2), (299, 1)], shipping_cents=50), 747)
        for shipping in (-1, 1.5, True):
            with self.subTest(shipping=shipping), self.assertRaises(ValueError):
                cart.total([(100, 1)], shipping)
        for lines in ([], [(-1, 1)], [(1, 0)], [(1.5, 2)], [(True, 1)]):
            with self.subTest(lines=lines), self.assertRaises(ValueError):
                cart.total(lines)
