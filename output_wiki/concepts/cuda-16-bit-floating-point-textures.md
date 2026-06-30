# 16-Bit Floating-Point Textures

Details the IEEE 754-2008 binary2 half format support in CUDA arrays, host/device conversion intrinsics, texture fetching promotion to 32-bit, and channel description creation.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3811-L3820

Citation: [CUDA_C_Programming_Guide:L3811-L3820]

````text
## 6.2.14.1.2 16-Bit Floating-Point Textures

The 16-bit floating-point or half format supported by CUDA arrays is the same as the IEEE 754-2008 binary2 format.

CUDA C++ does not support a matching data type, but provides intrinsic functions to convert to and from the 32-bit floating-point format via the unsigned short type: \_\_float2half\_rn(float) and \_half2float(unsigned short). These functions are only supported in device code. Equivalent functions for the host code can be found in the OpenEXR library, for example.

16-bit floating-point components are promoted to 32 bit float during texture fetching before any filtering is performed.

A channel description for the 16-bit floating-point format can be created by calling one of the cudaCreateChannelDescHalf\*() functions.
````
