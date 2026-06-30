# 10.18.6 Compiler Optimization Hint Restrictions

Restrictions for compiler optimization hint functions. __assume() only supported with cl.exe host compiler. Other functions require invocation from __device__/__global__ functions or when __CUDA_ARCH__ macro is defined, unless host compiler supports them.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8554-L8561

Citation: [CUDA_C_Programming_Guide:L8554-L8561]

````text

## 10.18.6. Restrictions

\_\_assume() is only supported when using cl.exe host compiler. The other functions are supported on all platforms, subject to the following restrictions:

▶ If the host compiler supports the function, the function can be invoked from anywhere in translation unit.

Otherwise, the function must be invoked from within the body of a \_\_device\_\_/ \_\_global\_\_function, or only when the \_\_CUDA\_ARCH\_\_ macro is defined<sup>5</sup>.
````
