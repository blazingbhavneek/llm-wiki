# Long Double in CUDA

## Overview

In the context of CUDA programming, the `long double` data type is explicitly unsupported for execution on the device (GPU). While `long double` may be available in host-side C/C++ code, attempts to use it within device code (functions marked with `__device__` or `__global__`) will result in compilation errors or unsupported behavior.

## Technical Details

According to the CUDA C Programming Guide, the use of the `long double` type is not supported in device code [CUDA_C_Programming_Guide:L17451-L17454]. Developers requiring high-precision floating-point arithmetic on the GPU should utilize `double` (64-bit) or `float` (32-bit) types, as these are fully supported across all CUDA architectures.

## References

- CUDA C Programming Guide: Section 18.5.15. Long Double [CUDA_C_Programming_Guide:L17451-L17454]
