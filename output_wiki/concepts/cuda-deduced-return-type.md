# Deduced Return Type in CUDA

## Overview
CUDA imposes specific restrictions on functions with deduced return types (using `auto` or `decltype(auto)`) to ensure compatibility between device code and the host compiler. These restrictions primarily affect `__global__` and `__device__` functions.

## Restrictions on __global__ Functions
A `__global__` function cannot have a deduced return type. Attempting to define a kernel with a deduced return type is not supported.

## Restrictions on __device__ Functions
For `__device__` functions, the CUDA frontend compiler modifies the function declaration before invoking the host compiler. Specifically, if a `__device__` function has a deduced return type, the frontend compiler changes its declaration to have a `void` return type.

This transformation causes issues when host code attempts to introspect the deduced return type of the `__device__` function. Consequently, the CUDA compiler issues compile-time errors if the deduced return type is referenced outside device function bodies, with one exception: references are allowed if they are absent when `__CUDA_ARCH__` is undefined.

## Examples

### Valid Device Usage
A `__device__` function with a deduced return type can be used within other device functions. For example, taking the address of the function is valid inside a device function:

```c
__device__ auto fn1(int x) {
    return x;
}

__device__ void device_fn1() {
    // OK: Referencing fn1 inside a device function body
    int (*p1)(int) = fn1;
}
```

### Invalid Host Usage
Referencing the deduced return type of a `__device__` function in host code results in a compile-time error:

```c
// error: referenced outside device function bodies
decltype(fn1(10)) g1;

void host_fn1() {
    // error: referenced outside device function bodies
    int (*p1)(int) = fn1;

    struct S_local_t {
        // error: referenced outside device function bodies
        decltype(fn2(10)) m1;

        S_local_t() : m1(10) { }
    };
}

// error: referenced outside device function bodies
template <typename T = decltype(fn2)>
void host_fn2() { }

template<typename T> struct S1_t { };

// error: referenced outside device function bodies
struct S1_derived_t : S1_t<decltype(fn1)> { };
```

## References
- [CUDA_C_Programming_Guide:L17905-L17951]
