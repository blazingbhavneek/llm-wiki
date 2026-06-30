# Mathematical Functions Accuracy

Accuracy bounds (ULP errors) for standard and intrinsic mathematical functions across single, double, and quad precision.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L16364-L16486

Citation: [CUDA_C_Programming_Guide:L16364-L16486]

````text
# Chapter 17. Mathematical Functions

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

The reference manual lists, along with their description, all the functions of the C/C++ standard library mathematical functions that are supported in device code, as well as all intrinsic functions (that are only supported in device code).

This section provides accuracy information for some of these functions when applicable. It uses ULP for quantification. For further information on the definition of the Unit in the Last Place (ULP), please see Jean-Michel Muller’s paper On the definition of ulp(x), RR-5504, LIP RR-2005-09, INRIA, LIP. 2005, pp.16 at https://hal.inria.fr/inria-00070503/document.

Mathematical functions supported in device code do not set the global errno variable, nor report any floating-point exceptions to indicate errors; thus, if error diagnostic mechanisms are required, the user should implement additional screening for inputs and outputs of the functions. The user is responsible for the validity of pointer arguments. The user must not pass uninitialized parameters to the Mathematical functions as this may result in undefined behavior: functions are inlined in the user program and thus are subject to compiler optimizations.

## 17.1. Standard Functions

The functions from this section can be used in both host and device code.

This section specifies the error bounds of each function when executed on the device and also when executed on the host in the case where the host does not supply the function.

The error bounds are generated from extensive but not exhaustive tests, so they are not guaranteed bounds.

## Single-Precision Floating-Point Functions

Addition and multiplication are IEEE-compliant, so have a maximum error of 0.5 ulp.

The recommended way to round a single-precision floating-point operand to an integer, with the result being a single-precision floating-point number is rintf(), not roundf(). The reason is that roundf() maps to a 4-instruction sequence on the device, whereas rintf() maps to a single instruction. truncf(), ceilf(), and floorf() each map to a single instruction as well.

Table 17: Single-Precision Mathematical Standard Library Functions with Maximum ULP Error. The maximum error is stated as the absolute value of the diference in ulps between the result returned by the CUDA library function and a correctly rounded single-precision result obtained according to the round-to-nearest ties-to-even rounding mode.

<table><tr><td>Function</td><td>Maximum ulp error</td></tr><tr><td>x+y</td><td>0 (IEEE-754 round-to-nearest-even)</td></tr><tr><td>x*y</td><td>0 (IEEE-754 round-to-nearest-even)</td></tr><tr><td>x/y</td><td>0 for compute capability ≥ 2 when compiled with -prec-div=true2 (full range), otherwise</td></tr><tr><td>1/x</td><td>0 for compute capability ≥ 2 when compiled with -prec-div=true1 (full range), otherwise</td></tr><tr><td>rsqrtf(x)1/sqrtf(x)</td><td>2 (full range)Applies to 1/sqrtf(x) only when it is converted to rsqrtf(x) by the compiler.</td></tr><tr><td>sqrtf(x)</td><td>0 when compiled with -prec-sqrt=trueOtherwise 1 for compute capability ≥ 5.2 and 3 for older architectures</td></tr><tr><td>cbrtf(x)</td><td>1 (full range)</td></tr><tr><td>rcbrtf(x)</td><td>1 (full range)</td></tr><tr><td>hypotf(x,y)</td><td>3 (full range)</td></tr><tr><td>rhypotf(x,y)</td><td>2 (full range)</td></tr><tr><td>norm3df(x,y,z)</td><td>3 (full range)</td></tr><tr><td>rnorm3df(x,y,z)</td><td>2 (full range)</td></tr><tr><td>norm4df(x,y,z,t)</td><td>3 (full range)</td></tr><tr><td>rnorm4df(x,y,z,t)</td><td>2 (full range)</td></tr><tr><td>normf(dim,arr)</td><td>An error bound cannot be provided because a fast algorithm is used with accuracy loss due to round-off. .</td></tr><tr><td>rnormf(dim,arr)</td><td>An error bound cannot be provided because a fast algorithm is used with accuracy loss due to round-off. .</td></tr><tr><td>expf(x)</td><td>2 (full range)</td></tr><tr><td>exp2f(x)</td><td>2 (full range)</td></tr><tr><td>exp10f(x)</td><td>2 (full range)</td></tr><tr><td>expm1f(x)</td><td>1 (full range)</td></tr><tr><td>logf(x)</td><td>1 (full range)</td></tr></table>

continues on next page

Table 17 – continued from previous page

<table><tr><td>Function</td><td>Maximum ulp error</td></tr><tr><td>log2f(x)</td><td>1 (full range)</td></tr><tr><td>log10f(x)</td><td>2 (full range)</td></tr><tr><td>log1pf(x)</td><td>1 (full range)</td></tr><tr><td>sinf(x)</td><td>2 (full range)</td></tr><tr><td>cosf(x)</td><td>2 (full range)</td></tr><tr><td>tanf(x)</td><td>4 (full range)</td></tr><tr><td>sincosf(x,sptr,cptr)</td><td>2 (full range)</td></tr><tr><td>sinpif(x)</td><td>1 (full range)</td></tr><tr><td>cospif(x)</td><td>1 (full range)</td></tr><tr><td>sincospif(x,sptr,cptr)</td><td>1 (full range)</td></tr><tr><td>asinf(x)</td><td>2 (full range)</td></tr><tr><td>acosf(x)</td><td>2 (full range)</td></tr><tr><td>atanf(x)</td><td>2 (full range)</td></tr><tr><td>atan2f(y,x)</td><td>3 (full range)</td></tr><tr><td>sinhf(x)</td><td>3 (full range)</td></tr><tr><td>coshf(x)</td><td>2 (full range)</td></tr><tr><td>tanhf(x)</td><td>2 (full range)</td></tr><tr><td>asinhf(x)</td><td>3 (full range)</td></tr><tr><td>acoshf(x)</td><td>4 (full range)</td></tr><tr><td>atanhf(x)</td><td>3 (full range)</td></tr><tr><td>powf(x,y)</td><td>4 (full range)</td></tr><tr><td>erff(x)</td><td>2 (full range)</td></tr><tr><td>erfcf(x)</td><td>4 (full range)</td></tr><tr><td>erfinvf(x)</td><td>2 (full range)</td></tr><tr><td>erfcinvf(x)</td><td>4 (full range)</td></tr><tr><td>erfcxf(x)</td><td>4 (full range)</td></tr><tr><td>normcdfff(x)</td><td>5 (full range)</td></tr><tr><td>normcdfinvf(x)</td><td>5 (full range)</td></tr><tr><td>lgammaf(x)</td><td>6 (outside interval -10.001 ... -2.264; larger inside)</td></tr><tr><td>tgammaf(x)</td><td>5 (full range)</td></tr><tr><td>fmaf(x,y,z)</td><td>0 (full range)</td></tr><tr><td>frexpf(x,exp)</td><td>0 (full range)</td></tr></table>

continues on next page

Table 17 – continued from previous page

<table><tr><td>Function</td><td>Maximum ulp error</td></tr><tr><td>ldexpf(x,exp)</td><td>0 (full range)</td></tr><tr><td>scalbnf(x,n)</td><td>0 (full range)</td></tr><tr><td>scalblnf(x,l)</td><td>0 (full range)</td></tr><tr><td>logbf(x)</td><td>0 (full range)</td></tr><tr><td>ilogbf(x)</td><td>0 (full range)</td></tr><tr><td>j0f(x)</td><td>9 for |x| &lt; 8 otherwise, the maximum absolute error is 2.2 x  $10^{-6}$ </td></tr><tr><td>j1f(x)</td><td>9 for |x| &lt; 8 otherwise, the maximum absolute error is 2.2 x  $10^{-6}$ </td></tr><tr><td>jnf(n,x)</td><td>For n = 128, the maximum absolute error is 2.2 x  $10^{-6}$ </td></tr><tr><td>y0f(x)</td><td>9 for |x| &lt; 8 otherwise, the maximum absolute error is 2.2 x  $10^{-6}$ </td></tr><tr><td>y1f(x)</td><td>9 for |x| &lt; 8 otherwise, the maximum absolute error is 2.2 x  $10^{-6}$ </td></tr><tr><td>ynf(n,x)</td><td>ceil(2 + 2.5n) for |x| &lt; n otherwise, the maximum absolute error is 2.2 x  $10^{-6}$ </td></tr><tr><td>cyl_bessel_i0f(x)</td><td>6 (full range)</td></tr><tr><td>cyl_bessel_i1f(x)</td><td>6 (full range)</td></tr><tr><td>fmodf(x,y)</td><td>0 (full range)</td></tr><tr><td>remainderf(x,y)</td><td>0 (full range)</td></tr><tr><td>remquof(x,y,iptr)</td><td>0 (full range)</td></tr><tr><td>modff(x,iptr)</td><td>0 (full range)</td></tr><tr><td>fdimf(x,y)</td><td>0 (full range)</td></tr><tr><td>truncf(x)</td><td>0 (full range)</td></tr><tr><td>roundf(x)</td><td>0 (full range)</td></tr><tr><td>rintf(x)</td><td>0 (full range)</td></tr><tr><td>nearbyintf(x)</td><td>0 (full range)</td></tr><tr><td>ceilf(x)</td><td>0 (full range)</td></tr><tr><td>floorf(x)</td><td>0 (full range)</td></tr><tr><td>lrintf(x)</td><td>0 (full range)</td></tr></table>

continues on next page

Table 17 – continued from previous page

<table><tr><td>Function</td><td>Maximum ulp error</td></tr><tr><td>1roundf(x)</td><td>0 (full range)</td></tr><tr><td>1lrintf(x)</td><td>0 (full range)</td></tr><tr><td>1lroundf(x)</td><td>0 (full range)</td></tr></table>

## Double-Precision Floating-Point Functions

The recommended way to round a double-precision floating-point operand to an integer, with the result being a double-precision floating-point number is rint(), not round(). The reason is that round() maps to a 5-instruction sequence on the device, whereas rint() maps to a single instruction. trunc(), ceil(), and floor() each map to a single instruction as well.

Table 18: Double-Precision Mathematical Standard Library Functions with Maximum ULP Error. The maximum error is stated as the absolute value of the diference in ulps between the result returned by the CUDA library function and a correctly rounded double-precision result obtained according to the round-to-nearest ties-to-even rounding mode.

<table><tr><td>Function</td><td>Maximum ulp error</td></tr><tr><td>x+y</td><td>0 (IEEE-754 round-to-nearest-even)</td></tr><tr><td>x*y</td><td>0 (IEEE-754 round-to-nearest-even)</td></tr><tr><td>x/y</td><td>0 (IEEE-754 round-to-nearest-even)</td></tr><tr><td>1/x</td><td>0 (IEEE-754 round-to-nearest-even)</td></tr><tr><td>sqrt(x)</td><td>0 (IEEE-754 round-to-nearest-even)</td></tr><tr><td>rsqrt(x)</td><td>1 (full range)</td></tr><tr><td>cbrt(x)</td><td>1 (full range)</td></tr><tr><td>rcbrt(x)</td><td>1 (full range)</td></tr><tr><td>hypot(x,y)</td><td>2 (full range)</td></tr><tr><td>rhypot(x,y)</td><td>1 (full range)</td></tr><tr><td>norm3d(x,y,z)</td><td>2 (full range)</td></tr><tr><td>rnorm3d(x,y,z)</td><td>1 (full range)</td></tr><tr><td>norm4d(x,y,z,t)</td><td>2 (full range)</td></tr><tr><td>rnorm4d(x,y,z,t)</td><td>1 (full range)</td></tr><tr><td>norm(dim,arr)</td><td>An error bound cannot be provided because a fast algorithm is used with accuracy loss due to round-off.</td></tr><tr><td>rnorm(dim,arr)</td><td>An error bound cannot be provided because a fast algorithm is used with accuracy loss due to round-off.</td></tr></table>

continues on next page

Table 18 – continued from previous page

<table><tr><td>Function</td><td>Maximum ulp error</td></tr><tr><td>exp(x)</td><td>1 (full range)</td></tr><tr><td>exp2(x)</td><td>1 (full range)</td></tr><tr><td>exp10(x)</td><td>1 (full range)</td></tr><tr><td>expm1(x)</td><td>1 (full range)</td></tr><tr><td>log(x)</td><td>1 (full range)</td></tr><tr><td>log2(x)</td><td>1 (full range)</td></tr><tr><td>log10(x)</td><td>1 (full range)</td></tr><tr><td>log1p(x)</td><td>1 (full range)</td></tr><tr><td>sin(x)</td><td>2 (full range)</td></tr><tr><td>cos(x)</td><td>2 (full range)</td></tr><tr><td>tan(x)</td><td>2 (full range)</td></tr><tr><td>sincos(x, sptr, cptr)</td><td>2 (full range)</td></tr><tr><td>sinpi(x)</td><td>2 (full range)</td></tr><tr><td>cospi(x)</td><td>2 (full range)</td></tr><tr><td>sincospi(x, sptr, cptr)</td><td>2 (full range)</td></tr><tr><td>asin(x)</td><td>2 (full range)</td></tr><tr><td>acos(x)</td><td>2 (full range)</td></tr><tr><td>atan(x)</td><td>2 (full range)</td></tr><tr><td>atan2(y, x)</td><td>2 (full range)</td></tr><tr><td>sinh(x)</td><td>2 (full range)</td></tr><tr><td>cosh(x)</td><td>1 (full range)</td></tr><tr><td>tanh(x)</td><td>1 (full range)</td></tr><tr><td>asinh(x)</td><td>3 (full range)</td></tr><tr><td>acosh(x)</td><td>3 (full range)</td></tr><tr><td>atanh(x)</td><td>2 (full range)</td></tr><tr><td>pow(x, y)</td><td>2 (full range)</td></tr><tr><td>erf(x)</td><td>2 (full range)</td></tr><tr><td>erfc(x)</td><td>5 (full range)</td></tr><tr><td>erfinv(x)</td><td>5 (full range)</td></tr><tr><td>erfcinv(x)</td><td>6 (full range)</td></tr><tr><td>erfcx(x)</td><td>4 (full range)</td></tr><tr><td>normcdf(x)</td><td>5 (full range)</td></tr></table>

continues on next page

Table 18 – continued from previous page

<table><tr><td>Function</td><td>Maximum ulp error</td></tr><tr><td>normcdfinv(x)</td><td>8 (full range)</td></tr><tr><td>lgamma(x)</td><td>4 (outside interval -23.0001 ... -2.2637; larger in-side)</td></tr><tr><td>tgamma(x)</td><td>10 (full range)</td></tr><tr><td>fma(x,y,z)</td><td>0 (IEEE-754 round-to-nearest-even)</td></tr><tr><td>frexp(x,exp)</td><td>0 (full range)</td></tr><tr><td>ldexp(x,exp)</td><td>0 (full range)</td></tr><tr><td>scalbn(x,n)</td><td>0 (full range)</td></tr><tr><td>scalbln(x,l)</td><td>0 (full range)</td></tr><tr><td>logb(x)</td><td>0 (full range)</td></tr><tr><td>ilogb(x)</td><td>0 (full range)</td></tr><tr><td>jθ(x)</td><td>7 for |x| &lt; 8 otherwise, the maximum absolute error is 5 x  $10^{-12}$ </td></tr><tr><td>j1(x)</td><td>7 for |x| &lt; 8 otherwise, the maximum absolute error is 5 x  $10^{-12}$ </td></tr><tr><td>jn(n,x)</td><td>For n = 128, the maximum absolute error is 5 x  $10^{-12}$ </td></tr><tr><td>yθ(x)</td><td>7 for |x| &lt; 8 otherwise, the maximum absolute error is 5 x  $10^{-12}$ </td></tr><tr><td>y1(x)</td><td>7 for |x| &lt; 8 otherwise, the maximum absolute error is 5 x  $10^{-12}$ </td></tr><tr><td>yn(n,x)</td><td>For |x| &gt; 1.5n, the maximum absolute error is 5 x  $10^{-12}$ </td></tr><tr><td>cyl_bessel_iθ(x)</td><td>6 (full range)</td></tr><tr><td>cyl_bessel_i1(x)</td><td>6 (full range)</td></tr><tr><td>fmod(x,y)</td><td>0 (full range)</td></tr><tr><td>remainder(x,y)</td><td>0 (full range)</td></tr><tr><td>remquo(x,y,iptr)</td><td>0 (full range)</td></tr><tr><td>modf(x,iptr)</td><td>0 (full range)</td></tr><tr><td>fdim(x,y)</td><td>0 (full range)</td></tr><tr><td>trunc(x)</td><td>0 (full range)</td></tr><tr><td>round(x)</td><td>0 (full range)</td></tr></table>

continues on next page

Table 18 – continued from previous page

<table><tr><td>Function</td><td>Maximum ulp error</td></tr><tr><td>rint(x)</td><td>0 (full range)</td></tr><tr><td>nearbyint(x)</td><td>0 (full range)</td></tr><tr><td>ceil(x)</td><td>0 (full range)</td></tr><tr><td>floor(x)</td><td>0 (full range)</td></tr><tr><td>lrint(x)</td><td>0 (full range)</td></tr><tr><td>lround(x)</td><td>0 (full range)</td></tr><tr><td>llrint(x)</td><td>0 (full range)</td></tr><tr><td>llround(x)</td><td>0 (full range)</td></tr></table>

## Quad-Precision Floating-Point Functions

Note that the quad-precision mathematical functions are currently only available to devices with compute capability 10.0 and later. Due to the specifics of implementation, the support of \_\_float128 and \_Float128 types in device code is also limited to select combinations of host platforms, see also Host Compiler Extensions.

Table 19: Quad-Precision Mathematical Standard Library Functions with Maximum ULP Error. The maximum error is stated as the absolute value of the diference in ulps between the result returned by the CUDA library function and a correctly rounded quad-precision result obtained according to the round-tonearest ties-to-even rounding mode.

<table><tr><td>Function</td><td>Maximum ulp error</td></tr><tr><td>x+y __nv_fp128_add(x, y)</td><td>0 (IEEE-754 round-to-nearest-even)</td></tr><tr><td>x-y __nv_fp128_sub(x, y)</td><td>0 (IEEE-754 round-to-nearest-even)</td></tr><tr><td>x*y __nv_fp128_mul(x, y)</td><td>0 (IEEE-754 round-to-nearest-even)</td></tr><tr><td>x/y __nv_fp128_div(x, y)</td><td>0 (IEEE-754 round-to-nearest-even)</td></tr><tr><td>__nv_fp128_sqrt(x)</td><td>0 (IEEE-754 round-to-nearest-even)</td></tr><tr><td>__nv_fp128_fma(x, y, z)</td><td>0 (IEEE-754 round-to-nearest-even)</td></tr><tr><td>__nv_fp128_sin(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_cos(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_tan(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_asin(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_acos(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_atan(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_exp(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_exp2(x)</td><td>1 (full range)</td></tr></table>

continues on next page

Table 19 – continued from previous page

<table><tr><td>Function</td><td>Maximum ulp error</td></tr><tr><td>__nv_fp128_exp10(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_expm1(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_log(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_log2(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_log10(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_log1p(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_pow(x, y)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_sinh(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_cosh(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_tanh(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_asinh(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_acosh(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_atanh(x)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_hypot(x, y)</td><td>1 (full range)</td></tr><tr><td>__nv_fp128_ceil(x)</td><td>0 (full range)</td></tr><tr><td>__nv_fp128_trunc(x)</td><td>0 (full range)</td></tr><tr><td>__nv_fp128_floor(x)</td><td>0 (full range)</td></tr><tr><td>__nv_fp128_round(x)</td><td>0 (full range)</td></tr><tr><td>__nv_fp128_rint(x)</td><td>0 (full range)</td></tr><tr><td>__nv_fp128_fabs(x)</td><td>0 (full range)</td></tr><tr><td>__nv_fp128_copysign(x, y)</td><td>0 (full range)</td></tr><tr><td>__nv_fp128_fmax(x, y)</td><td>0 (full range)</td></tr><tr><td>__nv_fp128_fmin(x, y)</td><td>0 (full range)</td></tr><tr><td>__nv_fp128_fdim(x, y)</td><td>0 (full range)</td></tr><tr><td>__nv_fp128_fmod(x, y)</td><td>0 (full range)</td></tr><tr><td>__nv_fp128_remainder(x, y)</td><td>0 (full range)</td></tr><tr><td>__nv_fp128_frexp(x, nptr)</td><td>0 (full range)</td></tr><tr><td>__nv_fp128_modf(x, iptr)</td><td>0 (full range)</td></tr><tr><td>__nv_fp128_ldexp(x, exp)</td><td>0 (full range)</td></tr><tr><td>__nv_fp128_ilogb(x)</td><td>0 (full range)</td></tr></table>

## 17.2. Intrinsic Functions

The functions from this section can only be used in device code.

Among these functions are the less accurate, but faster versions of some of the functions of Standard Functions. They have the same name prefixed with \_\_ (such as \_\_sinf(x)). They are faster as they map to fewer native instructions. The compiler has an option (-use\_fast\_math) that forces each function in Table 20 to compile to its intrinsic counterpart. In addition to reducing the accuracy of the afected functions, it may also cause some diferences in special case handling. A more robust approach is to selectively replace mathematical function calls by calls to intrinsic functions only where it is merited by the performance gains and where changed properties such as reduced accuracy and diferent special case handling can be tolerated.

Table 20: Functions Afected by -use\_fast\_math

<table><tr><td>Operator/Function</td><td>Device Function</td></tr><tr><td>x/y</td><td>__fdividef(x,y)</td></tr><tr><td>sinf(x)</td><td>__sinf(x)</td></tr><tr><td>cosf(x)</td><td>__cosf(x)</td></tr><tr><td>tanf(x)</td><td>__tanf(x)</td></tr><tr><td>sincosf(x,sptr,cptr)</td><td>__sincosf(x,sptr,cptr)</td></tr><tr><td>logf(x)</td><td>__logf(x)</td></tr><tr><td>log2f(x)</td><td>__log2f(x)</td></tr><tr><td>log10f(x)</td><td>__log10f(x)</td></tr><tr><td>expf(x)</td><td>__expf(x)</td></tr><tr><td>exp10f(x)</td><td>__exp10f(x)</td></tr><tr><td>powf(x,y)</td><td>__powf(x,y)</td></tr><tr><td>tanhf(x)</td><td>__tanhf(x)</td></tr></table>

## Single-Precision Floating-Point Functions

\_\_fadd\_[rn,rz,ru,rd]() and \_\_fmul\_[rn,rz,ru,rd]() map to addition and multiplication operations that the compiler never merges into FMADs. By contrast, additions and multiplications generated from the ‘\*’ and ‘+’ operators will frequently be combined into FMADs.

Functions sufixed with \_rn operate using the round to nearest even rounding mode.

Functions sufixed with \_rz operate using the round towards zero rounding mode.

Functions sufixed with \_ru operate using the round up (to positive infinity) rounding mode.

Functions sufixed with \_rd operate using the round down (to negative infinity) rounding mode.

The accuracy of floating-point division varies depending on whether the code is compiled with -prec-div=false or -prec-div=true. When the code is compiled with -prec-div=false, both the regular division ∕ operator and \_\_fdividef(x,y) have the same accuracy, but for $2 ^ { 1 2 6 } < | \mathsf { y } | <$ 2<sup>128</sup>, \_\_fdividef(x,y) delivers a result of zero, whereas the ∕ operator delivers the correct result to within the accuracy stated in Table 21. Also, for $2 ^ { 1 2 6 } < | \mathsf { y } | < 2 ^ { \dot { 1 } 2 8 }$ , if x is infinity, \_\_fdividef(x, y) delivers a NaN (as a result of multiplying infinity by zero), while the ∕ operator returns infinity. On the other hand, the ∕ operator is IEEE-compliant when the code is compiled with -prec-div=true or without any -prec-div option at all since its default value is true.

Table 21: Single-Precision Floating-Point Intrinsic Functions. (Supported by the CUDA Runtime Library with Respective Error Bounds)

<table><tr><td>Function</td><td>Error bounds</td></tr><tr><td>__fadd_[rn, rz, ru, rd](x,y)</td><td>IEEE-compliant.</td></tr><tr><td>__fsub_[rn, rz, ru, rd](x,y)</td><td>IEEE-compliant.</td></tr><tr><td>__fmul_[rn, rz, ru, rd](x,y)</td><td>IEEE-compliant.</td></tr><tr><td>__fmaf_[rn, rz, ru, rd](x,y,z)</td><td>IEEE-compliant.</td></tr><tr><td>__frcp_[rn, rz, ru, rd](x)</td><td>IEEE-compliant.</td></tr><tr><td>__fsqrt_[rn, rz, ru, rd](x)</td><td>IEEE-compliant.</td></tr><tr><td>__frsqrt_rn(x)</td><td>IEEE-compliant.</td></tr><tr><td>__fdiv_[rn, rz, ru, rd](x,y)</td><td>IEEE-compliant.</td></tr><tr><td>__fdividef(x,y)</td><td>For |y| in [2-126, 2126], the maximum ulp error is 2.</td></tr><tr><td>__expf(x)</td><td>The maximum ulp error is 2 + floor(abs(1.173 * x)).</td></tr><tr><td>__exp10f(x)</td><td>The maximum ulp error is 2 + floor(abs(2.97 * x)).</td></tr><tr><td>__logf(x)</td><td>For x in [0.5, 2], the maximum absolute error is 2-21.41, otherwise, the maximum ulp error is 3.</td></tr><tr><td>__log2f(x)</td><td>For x in [0.5, 2], the maximum absolute error is 2-22, otherwise, the maximum ulp error is 2.</td></tr><tr><td>__log10f(x)</td><td>For x in [0.5, 2], the maximum absolute error is 2-24, otherwise, the maximum ulp error is 3.</td></tr><tr><td>__sinf(x)</td><td>For x in [-π, π], the maximum absolute error is 2-21.41, and larger otherwise.</td></tr><tr><td>__cosf(x)</td><td>For x in [-π, π], the maximum absolute error is 2-21.19, and larger otherwise.</td></tr><tr><td>__sincosf(x, sptr, cptr)</td><td>Same as __sinf(x) and __cosf(x).</td></tr><tr><td>__tanf(x)</td><td>Derived from its implementation as __sinf(x) * (1/__cosf(x)).</td></tr><tr><td>__powf(x, y)</td><td>Derived from its implementation as exp2f(y * __log2f(x)).</td></tr><tr><td>__tanhf(x)</td><td>The maximum relative error of the current implementation is 2-11. Subnormal results of this fast intrinsic are not flushed to zero even under -ftz=true compiler setting. Available for devices with compute capability of at least 7.5; and defaults to regular tanhf() function behavior on other devices.</td></tr></table>

## Double-Precision Floating-Point Functions

\_\_dadd\_rn() and \_\_dmul\_rn() map to addition and multiplication operations that the compiler never merges into FMADs. By contrast, additions and multiplications generated from the ‘\*’ and ‘+’ operators will frequently be combined into FMADs.

Table 22: Double-Precision Floating-Point Intrinsic Functions. (Supported by the CUDA Runtime Library with Respective Error Bounds)

<table><tr><td>Function</td><td>Error bounds</td></tr><tr><td>__dadd_[rn, rz, ru, rd](x,y)</td><td>IEEE-compliant.</td></tr><tr><td>__dsub_[rn, rz, ru, rd](x,y)</td><td>IEEE-compliant.</td></tr><tr><td>__dmul_[rn, rz, ru, rd](x,y)</td><td>IEEE-compliant.</td></tr><tr><td>__fma_[rn, rz, ru, rd](x,y,z)</td><td>IEEE-compliant.</td></tr><tr><td>__ddiv_[rn, rz, ru, rd](x,y)(x,y)</td><td>IEEE-compliant.Requires compute capability &gt; 2.</td></tr><tr><td>__drcp_[rn, rz, ru, rd](x)</td><td>IEEE-compliant.Requires compute capability &gt; 2.</td></tr><tr><td>__dsqrt_[rn, rz, ru, rd](x)</td><td>IEEE-compliant.Requires compute capability &gt; 2.</td></tr></table>

# Chapter 18. C++ Language Support
````
