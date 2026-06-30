# 64-Bit Compatibility

Explains that the 64-bit nvcc compiles device code in 64-bit mode, which requires host code to also be compiled in 64-bit mode.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L1207-L1210

Citation: [CUDA_C_Programming_Guide:L1207-L1210]

````text

## 6.1.6. 64-Bit Compatibility

The 64-bit version of nvcc compiles device code in 64-bit mode (i.e., pointers are 64-bit). Device code compiled in 64-bit mode is only supported with host code compiled in 64-bit mode.
````
