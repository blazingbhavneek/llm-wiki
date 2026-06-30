# Floating-Point Standard

IEEE 754-2008 compliance details, deviations, rounding modes, NaN handling, flush-to-zero behavior, compiler flags, and atomic operation specifics for NVIDIA GPUs.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L19524-L19551

Citation: [CUDA_C_Programming_Guide:L19524-L19551]

````text
## 20.3. Floating-Point Standard

All compute devices follow the IEEE 754-2008 standard for binary floating-point arithmetic with the following deviations:

▶ There is no dynamically configurable rounding mode; however, most of the operations support multiple IEEE rounding modes, exposed via device intrinsics.

There is no mechanism for detecting that a floating-point exception has occurred and all operations behave as if the IEEE-754 exceptions are always masked, and deliver the masked response as defined by IEEE-754 if there is an exceptional event. For the same reason, while SNaN encodings are supported, they are not signaling and are handled as quiet.

▶ The result of a single-precision floating-point operation involving one or more input NaNs is the quiet NaN of bit pattern 0x7ffff.

▶ Double-precision floating-point absolute value and negation are not compliant with IEEE-754 with respect to NaNs; these are passed through unchanged.

Code must be compiled with -ftz=false, -prec-div=true, and -prec-sqrt=true to ensure IEEE compliance (this is the default setting; see the nvcc user manual for description of these compilation flags).

Regardless of the setting of the compiler flag -ftz,

atomic single-precision floating-point adds on global memory always operate in flush-to-zero mode, i.e., behave equivalent to FADD.F32.FTZ.RN,

▶ atomic single-precision floating-point adds on shared memory always operate with denormal support, i.e., behave equivalent to FADD.F32.RN.

In accordance to the IEEE-754R standard, if one of the input parameters to fminf(), fmin(), fmaxf(), or fmax() is NaN, but not the other, the result is the non-NaN parameter.

The conversion of a floating-point value to an integer value in the case where the floating-point value falls outside the range of the integer format is left undefined by IEEE-754. For compute devices, the behavior is to clamp to the end of the supported range. This is unlike the x86 architecture behavior.

The behavior of integer division by zero and integer overflow is left undefined by IEEE-754. For compute devices, there is no mechanism for detecting that such integer operation exceptions have occurred. Integer division by zero yields an unspecified, machine-specific value.

https://developer.nvidia.com/content/precision-performance-floating-point-and-ieee-754-compliance-nvidia-gpus includes more information on the floating point accuracy and compliance of NVIDIA GPUs.
````
