# py_extended_euclidean_algorithm

Returns the Bézout coefficients and the gcd of two integers, so you can
solve `a*x + b*y == gcd(a, b)` and recover modular inverses without
re-deriving the bookkeeping by hand.

```python
from py_extended_euclidean_algorithm import extended_gcd

g, x, y = extended_gcd(240, 46)
assert g == 2
assert 240 * x + 46 * y == 2

# Modular inverse of 3 modulo 11:
g, x, _ = extended_gcd(3, 11)
assert g == 1
assert (3 * x) % 11 == 1
```

## Why this exists

`math.gcd` gives you the greatest common divisor but throws away the
coefficients that make the Euclidean algorithm useful for modular
arithmetic.  Re-implementing the extended version in every project that
needs a modular inverse is a small but repeated source of off-by-one
sign errors.  This library fixes the interface to a single function
returning a three-tuple `(g, x, y)`.

The trade-off is that it exposes exactly one function and no class or
options object.  That keeps the API trivial to call and to test; if you
need the coefficients for a specific normalisation (for example a
positive `x` in `[0, m)`), you apply that to the result yourself rather
than passing a flag.

## The awkward edge

`extended_gcd(0, 0)` returns `(0, 1, 0)`.  The gcd is zero, matching
`math.gcd(0, 0)`, and the pair `(1, 0)` is the canonical Bézout
certificate for that degenerate case.  If your code assumes `g > 0`,
check for zero before dividing.
