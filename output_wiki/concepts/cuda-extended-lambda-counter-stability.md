# CUDA Extended Lambda Counter Stability

## Overview
When the CUDA compiler parses a function, it assigns a unique counter value to each extended lambda defined within that function. This counter value is critical because it is used in the substituted named type that is passed to the host compiler [CUDA_C_Programming_Guide:L18737-L18757].

## Stability Requirement
Because the counter value is integral to the type substitution process, the presence and relative declaration order of extended lambdas must remain consistent regardless of compilation context. Specifically, whether or not an extended lambda is defined within a function must not depend on:

1. A particular value of the `__CUDA_ARCH__` macro.
2. The state of `__CUDA_ARCH__` being undefined [CUDA_C_Programming_Guide:L18737-L18757].

Violating this stability constraint results in compilation errors, as the host compiler receives inconsistent type information based on the device architecture definitions [CUDA_C_Programming_Guide:L18737-L18757].

## Example
The following code demonstrates a scenario that triggers an error due to unstable lambda definition order dependent on `__CUDA_ARCH__`:

```cpp
template <typename T>
__global__ void kernel(T in) { in(); }

__host__ __device__ void foo(void) {
    // Error: the number and relative declaration
    // order of extended lambdas depends on
    // __CUDA_ARCH__
#if defined(__CUDA_ARCH__)
    auto lam1 = [] __device__ { return 0; };
    auto lam1b = [] __host__ __device__ { return 10; };
#endif
    auto lam2 = [] __device__ { return 4; };
    kernel<<<1,1>>>(lam2);
}
```

In this example, `lam1` and `lam1b` are only defined when `__CUDA_ARCH__` is defined (i.e., during device code compilation). However, `lam2` is always defined. This conditional definition changes the set of extended lambdas and their relative order depending on the compilation target, violating the stability requirement [CUDA_C_Programming_Guide:L18737-L18757].
