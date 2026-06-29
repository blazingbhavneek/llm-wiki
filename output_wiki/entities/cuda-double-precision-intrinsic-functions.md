# CUDA Double-Precision Intrinsic Functions

The CUDA Runtime Library provides a set of double-precision floating-point intrinsic functions that offer specific control over rounding modes and precision. These functions are distinct from standard arithmetic operators in how the compiler handles them, particularly regarding fused multiply-add (FMAD) optimizations.

## Compiler Behavior and Rounding Modes

Intrinsic functions like `__dadd_rn()` and `__dmul_rn()` map directly to addition and multiplication operations that the compiler **never merges into FMADs** [CUDA_C_Programming_Guide:L16478-L16485]. This behavior contrasts with additions and multiplications generated from the standard `*` and `+` operators, which the compiler frequently combines into FMADs [CUDA_C_Programming_Guide:L16478-L16485].

The suffixes in these function names indicate the rounding mode:
- `rn`: Round to nearest
- `rz`: Round toward zero
- `ru`: Round toward positive infinity
- `rd`: Round toward negative infinity

## Function Reference

The following table lists the supported double-precision floating-point intrinsic functions, their error bounds, and compute capability requirements [CUDA_C_Programming_Guide:L16478-L16485].

| Function | Error Bounds | Requirements |
| :--- | :--- | :--- |
| `__dadd_[rn, rz, ru, rd](x, y)` | IEEE-compliant | - |
| `__dsub_[rn, rz, ru, rd](x, y)` | IEEE-compliant | - |
| `__dmul_[rn, rz, ru, rd](x, y)` | IEEE-compliant | - |
| `__fma_[rn, rz, ru, rd](x, y, z)` | IEEE-compliant | - |
| `__ddiv_[rn, rz, ru, rd](x, y)` | IEEE-compliant | Compute Capability > 2 |
| `__drcp_[rn, rz, ru, rd](x)` | IEEE-compliant | Compute Capability > 2 |
| `__dsqrt_[rn, rz, ru, rd](x)` | IEEE-compliant | Compute Capability > 2 |

All listed functions are IEEE-compliant [CUDA_C_Programming_Guide:L16478-L16485]. Division, reciprocal, and square root operations require a compute capability greater than 2 [CUDA_C_Programming_Guide:L16478-L16485].
