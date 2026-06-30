# C++20 Features

Overview of C++20 features supported by nvcc, including module support, coroutine support, three-way comparison operator, and consteval functions, with device/host execution space restrictions.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L18027-L18086

Citation: [CUDA_C_Programming_Guide:L18027-L18086]

````text
## 18.5.25. C++20 Features

C++20 features enabled by default by the host compiler are also supported by nvcc. Passing nvcc -std=c++20 flag turns on all C++20 features and also invokes the host preprocessor, compiler and linker with the corresponding C++20 dialect option<sup>22</sup>. This section describes the restrictions on the supported C++20 features.

## 18.5.25.1 Module support

Modules are not supported in CUDA C++, in either host or device code. Uses of the module, export and import keywords are diagnosed as errors.

## 18.5.25.2 Coroutine support

Coroutines are not supported in device code. Uses of the co\_await, co\_yield and co\_return keywords in the scope of a device function are diagnosed as error during device compilation.

## 18.5.25.3 Three-way comparison operator

The three-way comparison operator is supported in both host and device code, but some uses implicitly rely on functionality from the Standard Template Library provided by the host implementation. Uses of those operators may require specifying the flag --expt-relaxed-constexpr to silence warnings and the functionality requires that the host implementation satisfies the requirements of device code.

Example:

```cpp
#include<compare>
struct S {
    int x, y, z;
    auto operator<=>(const S& rhs) const = default;
    __host__ __device__ bool operator<=>(int rhs) const { return false; }
};
__host__ __device__ bool f(S a, S b) {
    if (a <=> 1) // ok, calls a user-defined host-device overload
        return true;
    return a < b; // call to an implicitly-declared function and requires
        // a device-compatible std::strong_ordering implementation
}
```

## 18.5.25.4 Consteval functions

Ordinarily, cross execution space calls are not allowed, and cause a compiler diagnostic (warning or error). This restriction does not apply when the called function is declared with the consteval specifier. Thus, a \_\_device\_\_ or \_\_global\_\_ function can call a \_\_host\_\_consteval function, and a \_\_host\_\_ function can call a \_\_device\_\_ consteval function.

Example:

```cpp
namespace N1 {
//consteval host function
consteval int hcallee() { return 10; }

__device__ int dfunc() { return hcallee(); /* OK */ }
__global__ void gfunc() { (void)hcallee(); /* OK */ }
__host__ __device__ int hdfunc() { return hcallee(); /* OK */ }
int hfunc() { return hcallee(); /* OK */ }
} // namespace N1

namespace N2 {
//consteval device function
consteval __device__ int dcallee() { return 10; }

__device__ int dfunc() { return dcallee(); /* OK */ }
__global__ void gfunc() { (void)dcallee(); /* OK */ }
__host__ __device__ int hdfunc() { return dcallee(); /* OK */ }
int hfunc() { return dcallee(); /* OK */ }
}
```
````
