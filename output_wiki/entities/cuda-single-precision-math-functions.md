# CUDA Single-Precision Mathematical Functions

The single-precision floating-point functions described in this section are part of the CUDA Standard Library and can be used in both host and device code [CUDA_C_Programming_Guide:L16374-L16377]. This section specifies the error bounds for each function when executed on the device, as well as on the host in cases where the host does not supply the function [CUDA_C_Programming_Guide:L16378-L16380].

## Error Bounds and Accuracy

The error bounds provided are generated from extensive but not exhaustive tests; therefore, they are not guaranteed bounds [CUDA_C_Programming_Guide:L16381-L16383]. The maximum error is stated as the absolute value of the difference in ULPs between the result returned by the CUDA library function and a correctly rounded single-precision result obtained according to the round-to-nearest ties-to-even rounding mode [CUDA_C_Programming_Guide:L16385-L16387].

### Basic Arithmetic

Addition and multiplication are IEEE-compliant, resulting in a maximum error of 0.5 ULP [CUDA_C_Programming_Guide:L16388-L16390]. Division and reciprocal operations have specific accuracy characteristics depending on the compute capability and compilation flags [CUDA_C_Programming_Guide:L16391-L16395].

### Rounding Functions

For rounding a single-precision floating-point operand to an integer with the result being a single-precision floating-point number, `rintf()` is the recommended function over `roundf()` [CUDA_C_Programming_Guide:L16391-L16395]. This recommendation is based on performance: `roundf()` maps to a 4-instruction sequence on the device, whereas `rintf()` maps to a single instruction [CUDA_C_Programming_Guide:L16391-L16395]. Additionally, `truncf()`, `ceilf()`, and `floorf()` each map to a single instruction [CUDA_C_Programming_Guide:L16391-L16395].

## Function Reference Table

The following tables list single-precision mathematical standard library functions and their maximum ULP error bounds.

### Arithmetic and Root Functions

| Function | Maximum ulp error |
| :--- | :--- |
| `x+y` | 0 (IEEE-754 round-to-nearest-even) [CUDA_C_Programming_Guide:L16391-L16393] |
| `x*y` | 0 (IEEE-754 round-to-nearest-even) [CUDA_C_Programming_Guide:L16391-L16393] |
| `x/y` | 0 for compute capability ≥ 2 when compiled with `-prec-div=true` (full range); otherwise varies [CUDA_C_Programming_Guide:L16391-L16395] |
| `1/x` | 0 for compute capability ≥ 2 when compiled with `-prec-div=true` (full range); otherwise varies [CUDA_C_Programming_Guide:L16391-L16395] |
| `rsqrtf(x)` / `1/sqrtf(x)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `sqrtf(x)` | 0 when compiled with `-prec-sqrt=true`; otherwise 1 for compute capability ≥ 5.2 and 3 for older architectures [CUDA_C_Programming_Guide:L16391-L16395] |
| `cbrtf(x)` | 1 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `rcbrtf(x)` | 1 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `hypotf(x,y)` | 3 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `rhypotf(x,y)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `norm3df(x,y,z)` | 3 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `rnorm3df(x,y,z)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `norm4df(x,y,z,t)` | 3 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `rnorm4df(x,y,z,t)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `normf(dim,arr)` | An error bound cannot be provided because a fast algorithm is used with accuracy loss due to round-off [CUDA_C_Programming_Guide:L16391-L16395] |
| `rnormf(dim,arr)` | An error bound cannot be provided because a fast algorithm is used with accuracy loss due to round-off [CUDA_C_Programming_Guide:L16391-L16395] |

### Exponential and Logarithmic Functions

| Function | Maximum ulp error |
| :--- | :--- |
| `expf(x)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `exp2f(x)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `exp10f(x)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `expm1f(x)` | 1 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `logf(x)` | 1 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `log2f(x)` | 1 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `log10f(x)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `log1pf(x)` | 1 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |

### Trigonometric Functions

| Function | Maximum ulp error |
| :--- | :--- |
| `sinf(x)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `cosf(x)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `tanf(x)` | 4 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `sincosf(x,sptr,cptr)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `sinpif(x)` | 1 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `cospif(x)` | 1 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `sincospif(x,sptr,cptr)` | 1 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `asinf(x)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `acosf(x)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `atanf(x)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `atan2f(y,x)` | 3 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |

### Hyperbolic Functions

| Function | Maximum ulp error |
| :--- | :--- |
| `sinhf(x)` | 3 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `coshf(x)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `tanhf(x)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `asinhf(x)` | 3 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `acoshf(x)` | 4 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `atanhf(x)` | 3 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |

### Power and Special Functions

| Function | Maximum ulp error |
| :--- | :--- |
| `powf(x,y)` | 4 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `erff(x)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `erfcf(x)` | 4 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `erfinvf(x)` | 2 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `erfcinvf(x)` | 4 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `erfcxf(x)` | 4 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `normcdfff(x)` | 5 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `normcdfinvf(x)` | 5 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `lgammaf(x)` | 6 (outside interval -10.001 ... -2.264; larger inside) [CUDA_C_Programming_Guide:L16391-L16395] |
| `tgammaf(x)` | 5 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |

### Floating-Point Manipulation

| Function | Maximum ulp error |
| :--- | :--- |
| `fmaf(x,y,z)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `frexpf(x,exp)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `ldexpf(x,exp)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `scalbnf(x,n)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `scalblnf(x,l)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `logbf(x)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `ilogbf(x)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `fmodf(x,y)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `remainderf(x,y)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `remquof(x,y,iptr)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `modff(x,iptr)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `fdimf(x,y)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |

### Rounding and Integer Conversion

| Function | Maximum ulp error |
| :--- | :--- |
| `truncf(x)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `roundf(x)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `rintf(x)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `nearbyintf(x)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `ceilf(x)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `floorf(x)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `lrintf(x)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `llroundf(x)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `llrintf(x)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `lroundf(x)` | 0 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |

### Bessel Functions

| Function | Maximum ulp error |
| :--- | :--- |
| `j0f(x)` | 9 for \|x\| < 8; otherwise, the maximum absolute error is 2.2 x 10⁻⁶ [CUDA_C_Programming_Guide:L16391-L16395] |
| `j1f(x)` | 9 for \|x\| < 8; otherwise, the maximum absolute error is 2.2 x 10⁻⁶ [CUDA_C_Programming_Guide:L16391-L16395] |
| `jnf(n,x)` | For n = 128, the maximum absolute error is 2.2 x 10⁻⁶ [CUDA_C_Programming_Guide:L16391-L16395] |
| `y0f(x)` | 9 for \|x\| < 8; otherwise, the maximum absolute error is 2.2 x 10⁻⁶ [CUDA_C_Programming_Guide:L16391-L16395] |
| `y1f(x)` | 9 for \|x\| < 8; otherwise, the maximum absolute error is 2.2 x 10⁻⁶ [CUDA_C_Programming_Guide:L16391-L16395] |
| `ynf(n,x)` | ceil(2 + 2.5n) for \|x\| < n; otherwise, the maximum absolute error is 2.2 x 10⁻⁶ [CUDA_C_Programming_Guide:L16391-L16395] |
| `cyl_bessel_i0f(x)` | 6 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
| `cyl_bessel_i1f(x)` | 6 (full range) [CUDA_C_Programming_Guide:L16391-L16395] |
}
