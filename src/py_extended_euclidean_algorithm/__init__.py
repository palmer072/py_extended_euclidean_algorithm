"""Public API for py_extended_euclidean_algorithm.

Only ``extended_gcd`` is exported; it is the entire surface area of the
library, so a package-level re-export keeps call sites short.
"""

from .core import extended_gcd

__all__ = ["extended_gcd"]
