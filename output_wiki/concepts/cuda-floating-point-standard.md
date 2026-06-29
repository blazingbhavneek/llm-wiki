# CUDA Floating-Point Standard

All CUDA compute devices follow the IEEE 754-2008 standard for binary floating-point arithmetic, but with several specific deviations regarding rounding modes, exception handling, NaN behavior, and atomic operations [CUDA_C_Programming_Guide:L19524-L19551].

## Rounding Modes

CUDA does not support dynamically configurable rounding modes at the hardware level. However, most floating-point operations support multiple IEEE rounding modes, which are exposed via device intrinsics [CUDA_C_Programming_Guide:L19524-L19551].

## Exception Handling

There is no mechanism in CUDA to detect that a floating-point exception has occurred. All operations behave as if IEEE-754 exceptions are always masked, delivering the masked response defined by IEEE-754 in the event of an exceptional condition [CUDA_C_Programming_Guide:L19524-L19551].

## NaN Behavior

*   **Signaling NaNs (SNaN):** While SNaN encodings are supported, they are not signaling and are handled as quiet NaNs (QNaN) [CUDA_C_Programming_Guide:L19524-L19551].
*   **Single-Precision NaN Propagation:** The result of a single-precision floating-point operation involving one or more input NaNs is the quiet NaN with the bit pattern `0x7fffff80` (often referred to as the canonical quiet NaN) [CUDA_C_Programming_Guide:L19524-L19551].
*   **Double-Precision Absolute Value and Negation:** These operations are not compliant with IEEE-754 regarding NaNs; instead of generating a NaN, the input NaN is passed through unchanged [CUDA_C_Programming_Guide:L19524-L19551].
*   **fmin/fmax Functions:** In accordance with the IEEE-754R standard, if one input to `fminf()`, `fmin()`, `fmaxf()`, or `fmax()` is NaN and the other is not, the result is the non-NaN parameter [CUDA_C_Programming_Guide:L19524-L19551].

## Flush-to-Zero (FTZ) and Denormals

To ensure IEEE compliance, code should be compiled with `-ftz=false`, `-prec-div=true`, and `-prec-sqrt=true` (which are the default settings) [CUDA_C_Programming_Guide:L19524-L19551].

However, atomic operations have specific behaviors regardless of the `-ftz` compiler flag:

*   **Global Memory:** Atomic single-precision floating-point adds on global memory always operate in flush-to-zero mode, behaving equivalent to `FADD.F32.FTZ.RN` [CUDA_C_Programming_Guide:L19524-L19551].
*   **Shared Memory:** Atomic single-precision floating-point adds on shared memory always operate with denormal support, behaving equivalent to `FADD.F32.RN` [CUDA_C_Programming_Guide:L19524-L19551].

## Integer Conversion and Division

*   **Floating-Point to Integer Conversion:** IEEE-754 leaves the behavior undefined when a floating-point value falls outside the range of the integer format. CUDA compute devices clamp the result to the end of the supported range, which differs from x86 architecture behavior [CUDA_C_Programming_Guide:L19524-L19551].
*   **Integer Division by Zero and Overflow:** IEEE-754 leaves the behavior of integer division by zero and integer overflow undefined. CUDA provides no mechanism to detect these exceptions. Integer division by zero yields an unspecified, machine-specific value [CUDA_C_Programming_Guide:L19524-L19551].

## References

*   [CUDA_C_Programming_Guide:L19524-L19551] CUDA C++ Programming Guide, Section 20.3. Floating-Point Standard.
*   NVIDIA Precision, Performance, Floating-Point, and IEEE 754 Compliance: https://developer.nvidia.com/content/precision-performance-floating-point-and-ieee-754-compliance-nvidia-gpus [CUDA_C_Programming_Guide:L19524-L19551]
