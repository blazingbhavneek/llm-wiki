# CUDA Single-Precision Intrinsic Functions

CUDA provides a set of single-precision floating-point intrinsic functions that offer control over rounding modes and specific performance characteristics compared to standard C++ operators. These functions are part of the CUDA Runtime Library and are designed to provide deterministic behavior and specific accuracy guarantees.

## Rounding Modes

Intrinsic functions ending with a suffix indicate the rounding mode used for the operation [CUDA_C_Programming_Guide:L16460-L16477]:

*   **`_rn`**: Round to nearest even [CUDA_C_Programming_Guide:L16460-L16477].
*   **`_rz`**: Round towards zero [CUDA_C_Programming_Guide:L16460-L16477].
*   **`_ru`**: Round up (to positive infinity) [CUDA_C_Programming_Guide:L16460-L16477].
*   **`_rd`**: Round down (to negative infinity) [CUDA_C_Programming_Guide:L16460-L16477].

## Compiler Behavior and FMAD Fusion

The intrinsic functions `__fadd_[rn,rz,ru,rd]()` and `__fmul_[rn,rz,ru,rd]()` map directly to addition and multiplication operations. A key distinction is that the compiler **never** merges these intrinsic operations into Fused Multiply-Add (FMAD) instructions [CUDA_C_Programming_Guide:L16460-L16477].

In contrast, additions and multiplications generated from standard `*` and `+` operators are frequently combined into FMADs by the compiler [CUDA_C_Programming_Guide:L16460-L16477]. This makes the intrinsic functions useful when strict separation of operations is required for reproducibility or specific hardware behavior.

## Division Accuracy

The accuracy of floating-point division depends on the compilation flag `-prec-div` [CUDA_C_Programming_Guide:L16460-L16477]:

*   **`-prec-div=false`**: Both the regular division `/` operator and `__fdividef(x,y)` have the same accuracy for most ranges. However, for $2^{126} < |y| < 2^{128}$, `__fdividef(x,y)` returns zero, whereas the `/` operator returns the correct result within stated accuracy [CUDA_C_Programming_Guide:L16460-L16477]. Additionally, if $x$ is infinity in this range, `__fdividef(x,y)` returns a NaN (due to infinity multiplied by zero), while the `/` operator returns infinity [CUDA_C_Programming_Guide:L16460-L16477].
*   **`-prec-div=true` (default)**: The `/` operator is IEEE-compliant [CUDA_C_Programming_Guide:L16460-L16477].

## Function Reference and Error Bounds

The following table lists single-precision floating-point intrinsic functions and their respective error bounds [CUDA_C_Programming_Guide:L16460-L16477].

| Function | Error bounds |
| :--- | :--- |
| `__fadd_[rn, rz, ru, rd](x,y)` | IEEE-compliant. |
| `__fsub_[rn, rz, ru, rd](x,y)` | IEEE-compliant. |
| `__fmul_[rn, rz, ru, rd](x,y)` | IEEE-compliant. |
| `__fmaf_[rn, rz, ru, rd](x,y,z)` | IEEE-compliant. |
| `__frcp_[rn, rz, ru, rd](x)` | IEEE-compliant. |
| `__fsqrt_[rn, rz, ru, rd](x)` | IEEE-compliant. |
| `__frsqrt_rn(x)` | IEEE-compliant. |
| `__fdiv_[rn, rz, ru, rd](x,y)` | IEEE-compliant. |
| `__fdividef(x,y)` | For $|y|$ in $[2^{-126}, 2^{126}]$, the maximum ulp error is 2. |
| `__expf(x)` | The maximum ulp error is $2 + \text{floor}(|1.173 \times x|)$. |
| `__exp10f(x)` | The maximum ulp error is $2 + \text{floor}(|2.97 \times x|)$. |
| `__logf(x)` | For $x$ in $[0.5, 2]$, the maximum absolute error is $2^{-21.41}$; otherwise, the maximum ulp error is 3. |
| `__log2f(x)` | For $x$ in $[0.5, 2]$, the maximum absolute error is $2^{-22}$; otherwise, the maximum ulp error is 2. |
| `__log10f(x)` | For $x$ in $[0.5, 2]$, the maximum absolute error is $2^{-24}$; otherwise, the maximum ulp error is 3. |
| `__sinf(x)` | For $x$ in $[-\pi, \pi]$, the maximum absolute error is $2^{-21.41}$, and larger otherwise. |
| `__cosf(x)` | For $x$ in $[-\pi, \pi]$, the maximum absolute error is $2^{-21.19}$, and larger otherwise. |
| `__sincosf(x, sptr, cptr)` | Same as `__sinf(x)` and `__cosf(x)`. |
| `__tanf(x)` | Derived from its implementation as `__sinf(x) * (1/__cosf(x))`. |
| `__powf(x, y)` | Derived from its implementation as `exp2f(y * __log2f(x))`. |
| `__tanhf(x)` | The maximum relative error of the current implementation is $2^{-11}$. Subnormal results are not flushed to zero even under `-ftz=true`. Available for devices with compute capability of at least 7.5; defaults to regular `tanhf()` behavior on other devices. |

### Notes on Specific Functions

*   **`__tanhf`**: This fast intrinsic is available only for devices with compute capability 7.5 or higher. On older devices, it defaults to the behavior of the standard `tanhf()` function [CUDA_C_Programming_Guide:L16460-L16477].
*   **`__tanf` and `__powf`**: These are not hardware intrinsics with independent error bounds but are derived from other intrinsic implementations [CUDA_C_Programming_Guide:L16460-L16477].
