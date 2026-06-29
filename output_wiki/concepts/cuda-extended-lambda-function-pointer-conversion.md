# CUDA Extended Lambda Function Pointer Conversion

CUDA extended lambdas allow for the definition of lambda expressions with execution space qualifiers (`__device__`, `__host__`, etc.). When an extended lambda is used, the CUDA compiler replaces the lambda expression with an instance of a placeholder type in the code sent to the host compiler.

## Conversion Restrictions

The support for converting these placeholder types to function pointers depends on the execution space where the conversion occurs:

*   **Device Code**: The placeholder type defines a pointer-to-function conversion operator. Therefore, converting an extended `__device__` lambda to a function pointer is supported within device code (e.g., inside a `__global__` or `__device__` function).
*   **Host Code**: The placeholder type does **not** define a pointer-to-function conversion operator in host code. Consequently, attempting to convert an extended `__device__` lambda to a function pointer in host code results in a compilation error.

### Exception for `__host__ __device__` Lambdas

The restriction described above does not apply to extended lambdas that are marked as both `__host__` and `__device__` (`__host__ __device__`). For these lambdas, the conversion to a function pointer is supported in both host and device code.

## Examples

### Supported: Conversion in Device Code

The following example demonstrates that converting an extended `__device__` lambda to a function pointer is valid inside a kernel.

```c
template <typename T>
__global__ void kern(T in) {
  int (*fp)(double) = in;

  // OK: conversion in device code is supported
  fp(0);
  auto lam1 = [](double) { return 1; };

  // OK: conversion in device code is supported
  fp = lam1;
  fp(0);
}
```

### Unsupported: Conversion in Host Code

The following example shows that converting a pure `__device__` lambda to a function pointer in host code is an error.

```c
void foo(void) {
  auto lam_d = [] __device__ (double) { return 1; };
  auto lam_hd = [] __host__ __device__ (double) { return 1; };
  kern<<<1,1>>>(lam_d);
  kern<<<1,1>>>(lam_hd);

  // OK : conversion for __host__ __device__ lambda is supported
  // in host code
  int (*fp)(double) = lam_hd;

  // Error: conversion for __device__ lambda is not supported in
  // host code.
  int (*fp2)(double) = lam_d;
}
```

## References

- CUDA C++ Programming Guide: Extended Lambda Operator Conversion [CUDA_C_Programming_Guide:L18824-L18857]
