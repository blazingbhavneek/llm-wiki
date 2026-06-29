# CUDA Extended Lambda Closure Layout

## Overview
When an extended lambda functor object is passed from host code to device code (e.g., as an argument to a `__global__` function), the compiler enforces strict consistency in the lambda's closure class layout. This requirement ensures that the memory layout of captured variables is identical regardless of whether the code is compiled for the host or the device.

## The `__CUDA_ARCH__` Constraint
The layout of a lambda's closure class depends on the order in which captured variables are encountered during compilation. If the set or order of captured variables changes between host and device compilation, the resulting class layouts will differ, leading to incorrect program execution.

Therefore, any expression in the body of a lambda that captures variables must remain unchanged irrespective of:
1. Whether the `__CUDA_ARCH__` macro is defined.
2. The specific value of the `__CUDA_ARCH__` macro.

This restriction applies specifically to **extended device lambdas** (lambdas marked with `__device__` or `__host__ __device__`) that are passed across the host-device boundary.

## Introspection Limitations
For extended device lambdas, type introspection capabilities are restricted based on the execution context:
*   **Parameter Type**: Introspecting the parameter type of `operator()` is only supported in device code.
*   **Return Type**: Introspecting the return type of `operator()` is supported only in device code, unless the trait function `__nv_is_extended_device_lambda_with_preserved_return_type()` returns true.

## Example of Invalid Usage
The following example demonstrates a violation of the closure layout consistency rule. The lambda `lam1` captures `x1` conditionally based on `__CUDA_ARCH__`. This causes the closure layout to differ between host and device compilation, resulting in an error when passed to the kernel.

```cpp
__device__ int result;

template <typename T>
__global__ void kernel(T in) { result = in(); }

void foo(void) {
    int x1 = 1;
    auto lam1 = [=] __host__ __device__ {
        // Error: "x1" is only captured when __CUDA_ARCH__ is defined.
#ifdef __CUDA_ARCH__
        return x1 + 1;
#else
        return 10;
#endif
    };
    kernel<<<1,1>>>(lam1);
}
```

In this case, the host compilation does not define `__CUDA_ARCH__`, so `x1` is not captured. The device compilation defines `__CUDA_ARCH__`, so `x1` is captured. This discrepancy in capture lists leads to incompatible closure layouts.

## References
- [CUDA_C_Programming_Guide:L18798-L18823] CUDA C++ Programming Guide: Extended Device Lambdas and Closure Layout Consistency.
