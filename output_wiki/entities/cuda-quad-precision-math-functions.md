# CUDA Quad-Precision Mathematical Functions

The quad-precision mathematical functions in CUDA are implemented using the `__nv_fp128` and `_Float128` types. These functions provide high-precision arithmetic operations for scientific computing and other applications requiring greater precision than standard double-precision floating-point.

## Availability and Prerequisites

Quad-precision mathematical functions are currently only available to devices with **compute capability 10.0** and later [CUDA_C_Programming_Guide:L16436-L16449].

Due to implementation specifics, support for `__float128` and `_Float128` types in device code is limited to select combinations of host platforms. Users should consult the [Host Compiler Extensions](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#host-compiler-extensions) documentation for details on supported host configurations [CUDA_C_Programming_Guide:L16436-L16449].

## Error Bounds

The accuracy of these functions is measured in Units in the Last Place (ULP). The maximum error is defined as the absolute value of the difference in ULPs between the result returned by the CUDA library function and a correctly rounded quad-precision result obtained according to the **round-to-nearest, ties-to-even** rounding mode [CUDA_C_Programming_Guide:L16436-L16449].

### Arithmetic and Basic Functions

Basic arithmetic operations and square root are implemented to be correctly rounded, resulting in a maximum ULP error of 0 [CUDA_C_Programming_Guide:L16436-L16449].

| Function | Maximum ULP Error |
| :--- | :--- |
| `__nv_fp128_add(x, y)` | 0 (IEEE-754 round-to-nearest-even) |
| `__nv_fp128_sub(x, y)` | 0 (IEEE-754 round-to-nearest-even) |
| `__nv_fp128_mul(x, y)` | 0 (IEEE-754 round-to-nearest-even) |
| `__nv_fp128_div(x, y)` | 0 (IEEE-754 round-to-nearest-even) |
| `__nv_fp128_sqrt(x)` | 0 (IEEE-754 round-to-nearest-even) |
| `__nv_fp128_fma(x, y, z)` | 0 (IEEE-754 round-to-nearest-even) |

### Transcendental Functions

Transcendental functions such as trigonometric, exponential, and logarithmic functions have a maximum ULP error of 1 across their full range [CUDA_C_Programming_Guide:L16436-L16449].

| Function | Maximum ULP Error |
| :--- | :--- |
| `__nv_fp128_sin(x)` | 1 (full range) |
| `__nv_fp128_cos(x)` | 1 (full range) |
| `__nv_fp128_tan(x)` | 1 (full range) |
| `__nv_fp128_asin(x)` | 1 (full range) |
| `__nv_fp128_acos(x)` | 1 (full range) |
| `__nv_fp128_atan(x)` | 1 (full range) |
| `__nv_fp128_exp(x)` | 1 (full range) |
| `__nv_fp128_exp2(x)` | 1 (full range) |
| `__nv_fp128_exp10(x)` | 1 (full range) |
| `__nv_fp128_expm1(x)` | 1 (full range) |
| `__nv_fp128_log(x)` | 1 (full range) |
| `__nv_fp128_log2(x)` | 1 (full range) |
| `__nv_fp128_log10(x)` | 1 (full range) |
| `__nv_fp128_log1p(x)` | 1 (full range) |
| `__nv_fp128_pow(x, y)` | 1 (full range) |
| `__nv_fp128_sinh(x)` | 1 (full range) |
| `__nv_fp128_cosh(x)` | 1 (full range) |
| `__nv_fp128_tanh(x)` | 1 (full range) |
| `__nv_fp128_asinh(x)` | 1 (full range) |
| `__nv_fp128_acosh(x)` | 1 (full range) |
| `__nv_fp128_atanh(x)` | 1 (full range) |
| `__nv_fp128_hypot(x, y)` | 1 (full range) |

### Rounding and Conversion Functions

Rounding, absolute value, sign, and comparison functions are also correctly rounded, with a maximum ULP error of 0 [CUDA_C_Programming_Guide:L16436-L16449].

| Function | Maximum ULP Error |
| :--- | :--- |
| `__nv_fp128_ceil(x)` | 0 (full range) |
| `__nv_fp128_trunc(x)` | 0 (full range) |
| `__nv_fp128_floor(x)` | 0 (full range) |
| `__nv_fp128_round(x)` | 0 (full range) |
| `__nv_fp128_rint(x)` | 0 (full range) |
| `__nv_fp128_fabs(x)` | 0 (full range) |
| `__nv_fp128_copysign(x, y)` | 0 (full range) |
| `__nv_fp128_fmax(x, y)` | 0 (full range) |
| `__nv_fp128_fmin(x, y)` | 0 (full range) |
| `__nv_fp128_fdim(x, y)` | 0 (full range) |
| `__nv_fp128_fmod(x, y)` | 0 (full range) |
| `__nv_fp128_remainder(x, y)` | 0 (full range) |
| `__nv_fp128_frexp(x, nptr)` | 0 (full range) |
| `__nv_fp128_modf(x, iptr)` | 0 (full range) |
| `__nv_fp128_ldexp(x, exp)` | 0 (full range) |
| `__nv_fp128_ilogb(x)` | 0 (full range) |

## References

- [CUDA C Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html) [CUDA_C_Programming_Guide:L16436-L16449]
