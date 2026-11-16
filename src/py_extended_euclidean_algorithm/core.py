"""Extended Euclidean Algorithm.

Given two integers ``a`` and ``b``, returns a triple ``(g, x, y)`` such
that ``a*x + b*y == g`` and ``g == gcd(a, b)``.  The gcd is always
non-negative, which is the convention the rest of the numeric ecosystem
(``math.gcd``, ``fractions``, ``pow`` inverse helpers) uses; choosing a
negative gcd would make ``g`` depend on the sign of ``b`` and surprise
callers who compare against ``math.gcd``.

``gcd(0, 0)`` is defined as ``0``, matching ``math.gcd``.  For that input
the Bézout coefficients are ``(1, 0)``: the pair satisfies the identity
``0*1 + 0*0 == 0`` and is the canonical choice returned by the iterative
loop below.
"""

from __future__ import annotations

__all__ = ["extended_gcd"]


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return ``(g, x, y)`` with ``a*x + b*y == g == gcd(a, b)``.

    The implementation is the classic iterative form: it tracks the
    coefficients of the current remainder in terms of the original
    inputs, so no recursion limit is involved and the intermediate
    values stay bounded by the inputs.  The final gcd is normalised to
    be non-negative; if ``a`` and ``b`` are both zero the loop never
    runs and the initial state ``(a, 1, 0)`` would be ``(0, 1, 0)``,
    which is exactly the documented answer for that edge case.

    Accepts any objects that support ``//`` and ``%`` consistently with
    the Euclidean division identity; in practice that means ``int``.
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    # Normalise the gcd sign.  Flipping g also flips both coefficients so
    # the identity a*x + b*y == g is preserved.
    if old_r < 0:
        old_r, old_s, old_t = -old_r, -old_s, -old_t

    return old_r, old_s, old_t
