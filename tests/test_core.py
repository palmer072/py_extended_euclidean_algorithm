"""Tests for py_extended_euclidean_algorithm.

Every assertion is checked against the documented contract: the returned
``g`` equals ``math.gcd`` of the inputs and the Bézout identity holds
exactly.  No timing, no randomness, no floating point.
"""

import math
import unittest

from py_extended_euclidean_algorithm import extended_gcd


class TestExtendedGCD(unittest.TestCase):
    def assert_bezout(self, a, b):
        g, x, y = extended_gcd(a, b)
        self.assertEqual(g, math.gcd(a, b))
        self.assertEqual(a * x + b * y, g)
        return g, x, y

    def test_positive_coprime(self):
        g, x, y = self.assert_bezout(240, 46)
        self.assertEqual(g, 2)
        # 240*(-9) + 46*47 == 2 is one valid pair; the loop's particular
        # pair is deterministic, so pin it down.
        self.assertEqual((x, y), (-9, 47))

    def test_negative_input(self):
        self.assert_bezout(-240, 46)
        self.assert_bezout(240, -46)
        self.assert_bezout(-240, -46)

    def test_zero_and_zero(self):
        # gcd(0, 0) is 0 by convention; (1, 0) satisfies 0*1 + 0*0 == 0.
        self.assertEqual(extended_gcd(0, 0), (0, 1, 0))

    def test_zero_and_nonzero(self):
        self.assertEqual(extended_gcd(0, 7), (7, 0, 1))
        self.assertEqual(extended_gcd(7, 0), (7, 1, 0))
        self.assertEqual(extended_gcd(0, -7), (7, 0, -1))

    def test_multiples(self):
        g, x, y = self.assert_bezout(12, 4)
        self.assertEqual(g, 4)
        self.assertEqual((x, y), (0, 1))

    def test_one_and_one(self):
        self.assertEqual(extended_gcd(1, 1), (1, 0, 1))

    def test_large_inputs(self):
        # Fibonacci neighbours are the worst case for the Euclidean loop;
        # this exercises the iterative path with values that would blow a
        # naive recursive implementation.
        a, b = 10**18 + 9, 10**18 + 7
        self.assert_bezout(a, b)

    def test_modular_inverse_use_case(self):
        # The motivating use case: find x such that a*x == 1 (mod m).
        a, m = 3, 11
        g, x, _ = extended_gcd(a, m)
        self.assertEqual(g, 1)
        self.assertEqual((a * x) % m, 1)

    def test_returns_plain_ints(self):
        # Downstream code does arithmetic on the result, so the tuple
        # members must be real ints, not bools or other int subclasses.
        g, x, y = extended_gcd(8, 12)
        for value in (g, x, y):
            self.assertIs(type(value), int)


if __name__ == "__main__":
    unittest.main()
