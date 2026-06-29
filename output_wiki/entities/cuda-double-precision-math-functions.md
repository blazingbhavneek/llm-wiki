# CUDA Double-Precision Mathematical Functions

The CUDA C++ standard library provides a comprehensive set of double-precision floating-point mathematical functions. These functions are optimized for NVIDIA GPUs and are documented with their maximum error bounds, defined as the absolute difference in ULPs between the function's result and a correctly rounded result using the round-to-nearest-ties-to-even mode [CUDA_C_Programming_Guide:L16410-L16435].

## Rounding Functions

While several rounding functions are available, their implementation efficiency varies significantly on the device [CUDA_C_Programming_Guide:L16410-L16435]:

*   **`rint()`**: The recommended function for rounding a double-precision operand to an integer (returning a double). It maps to a single instruction [CUDA_C_Programming_Guide:L16410-L16435].
*   **`round()`**: Maps to a 5-instruction sequence on the device, making it less efficient than `rint()` for this specific purpose [CUDA_C_Programming_Guide:L16410-L16435].
*   **`trunc()`, `ceil()`, `floor()`**: Each maps to a single instruction [CUDA_C_Programming_Guide:L16410-L16435].

All standard rounding functions (`trunc`, `round`, `rint`, `nearbyint`, `ceil`, `floor`, `lrint`, `lround`, `llrint`, `llround`) have a maximum ULP error of 0 [CUDA_C_Programming_Guide:L16410-L16435].

## Arithmetic and Basic Functions

Basic arithmetic operations and their inverses are guaranteed to be correctly rounded according to IEEE-754 round-to-nearest-even rules, resulting in 0 ULP error [CUDA_C_Programming_Guide:L16410-L16435].

| Function | Maximum ULP Error | Notes |
| :--- | :--- | :--- |
| `x + y` | 0 | IEEE-754 round-to-nearest-even [CUDA_C_Programming_Guide:L16410-L16435] |
| `x * y` | 0 | IEEE-754 round-to-nearest-even [CUDA_C_Programming_Guide:L16410-L16435] |
| `x / y` | 0 | IEEE-754 round-to-nearest-even [CUDA_C_Programming_Guide:L16410-L16435] |
| `1 / x` | 0 | IEEE-754 round-to-nearest-even [CUDA_C_Programming_Guide:L16410-L16435] |
| `sqrt(x)` | 0 | IEEE-754 round-to-nearest-even [CUDA_C_Programming_Guide:L16410-L16435] |
| `fma(x, y, z)` | 0 | IEEE-754 round-to-nearest-even [CUDA_C_Programming_Guide:L16410-L16435] |

## Exponential and Logarithmic Functions

Exponential and logarithmic functions generally maintain a maximum error of 1 ULP across their full range, with specific exceptions for `erfc` and related functions [CUDA_C_Programming_Guide:L16410-L16435].

| Function | Maximum ULP Error | Notes |
| :--- | :--- | :--- |
| `exp(x)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `exp2(x)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `exp10(x)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `expm1(x)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `log(x)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `log2(x)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `log10(x)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `log1p(x)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `lgamma(x)` | 4 | Outside interval [-23.0001, -2.2637]; larger inside [CUDA_C_Programming_Guide:L16410-L16435] |
| `tgamma(x)` | 10 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `erf(x)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `erfc(x)` | 5 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `erfinv(x)` | 5 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `erfcinv(x)` | 6 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `erfcx(x)` | 4 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `normcdf(x)` | 5 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `normcdfinv(x)` | 8 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |

## Trigonometric Functions

Standard trigonometric functions typically have a maximum error of 2 ULPs, while hyperbolic functions vary between 1 and 3 ULPs [CUDA_C_Programming_Guide:L16410-L16435].

| Function | Maximum ULP Error | Notes |
| :--- | :--- | :--- |
| `sin(x)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `cos(x)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `tan(x)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `sincos(x, sptr, cptr)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `sinpi(x)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `cospi(x)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `sincospi(x, sptr, cptr)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `asin(x)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `acos(x)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `atan(x)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `atan2(y, x)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `sinh(x)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `cosh(x)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `tanh(x)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `asinh(x)` | 3 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `acosh(x)` | 3 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `atanh(x)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |

## Power and Root Functions

| Function | Maximum ULP Error | Notes |
| :--- | :--- | :--- |
| `pow(x, y)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `rsqrt(x)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `cbrt(x)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `rcbrt(x)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |

## Hypotenuse and Norm Functions

| Function | Maximum ULP Error | Notes |
| :--- | :--- | :--- |
| `hypot(x, y)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `rhypot(x, y)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `norm3d(x, y, z)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `rnorm3d(x, y, z)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `norm4d(x, y, z, t)` | 2 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `rnorm4d(x, y, z, t)` | 1 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `norm(dim, arr)` | N/A | Fast algorithm used; accuracy loss due to round-off [CUDA_C_Programming_Guide:L16410-L16435] |
| `rnorm(dim, arr)` | N/A | Fast algorithm used; accuracy loss due to round-off [CUDA_C_Programming_Guide:L16410-L16435] |

## Floating-Point Manipulation and Remainder Functions

These functions provide exact results (0 ULP error) or operate on the full range of double-precision values [CUDA_C_Programming_Guide:L16410-L16435].

| Function | Maximum ULP Error | Notes |
| :--- | :--- | :--- |
| `frexp(x, exp)` | 0 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `ldexp(x, exp)` | 0 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `scalbn(x, n)` | 0 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `scalbln(x, l)` | 0 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `logb(x)` | 0 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `ilogb(x)` | 0 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `fmod(x, y)` | 0 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `remainder(x, y)` | 0 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `remquo(x, y, iptr)` | 0 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `modf(x, iptr)` | 0 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `fdim(x, y)` | 0 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |

## Bessel Functions

Bessel functions have specific error bounds that may depend on the input magnitude or order `n` [CUDA_C_Programming_Guide:L16410-L16435].

| Function | Maximum ULP Error | Notes |
| :--- | :--- | :--- |
| `j0(x)` | 7 | For \|x\| < 8; otherwise max absolute error is 5 x 10^-12 [CUDA_C_Programming_Guide:L16410-L16435] |
| `j1(x)` | 7 | For \|x\| < 8; otherwise max absolute error is 5 x 10^-12 [CUDA_C_Programming_Guide:L16410-L16435] |
| `jn(n, x)` | N/A | For n = 128, max absolute error is 5 x 10^-12 [CUDA_C_Programming_Guide:L16410-L16435] |
| `y0(x)` | 7 | For \|x\| < 8; otherwise max absolute error is 5 x 10^-12 [CUDA_C_Programming_Guide:L16410-L16435] |
| `y1(x)` | 7 | For \|x\| < 8; otherwise max absolute error is 5 x 10^-12 [CUDA_C_Programming_Guide:L16410-L16435] |
| `yn(n, x)` | N/A | For \|x\| > 1.5n, max absolute error is 5 x 10^-12 [CUDA_C_Programming_Guide:L16410-L16435] |
| `cyl_bessel_i0(x)` | 6 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
| `cyl_bessel_i1(x)` | 6 | Full range [CUDA_C_Programming_Guide:L16410-L16435] |
