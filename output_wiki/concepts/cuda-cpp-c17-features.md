# C++17 Features

Overview of C++17 features supported by nvcc, including inline variables and structured bindings, with specific restrictions for device/managed memory spaces and whole-program compilation.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L17984-L18026

Citation: [CUDA_C_Programming_Guide:L17984-L18026]

````text
## 18.5.24. C++17 Features

C++17 features enabled by default by the host compiler are also supported by nvcc. Passing nvcc -std=c++17 flag turns on all C++17 features and also invokes the host preprocessor, compiler and linker with the corresponding C++17 dialect option<sup>21</sup>. This section describes the restrictions on the supported C++17 features.

## 18.5.24.1 Inline Variable

▶ A namespace scope inline variable declared with \_\_device\_\_ or \_\_constant\_\_ or \_\_managed\_\_ memory space specifier must have internal linkage, if the code is compiled with nvcc in whole program compilation mode.

Examples:

```txt
inline __device__ int xxx; //error when compiled with nvcc in
//whole program compilation mode.
//ok when compiled with nvcc in
//separate compilation mode.

inline __shared__ int yyyy0; // ok.
```

(continues on next page)

(continued from previous page)

```txt
static inline __device__ int yyy; // ok: internal linkage
namespace {
inline __device__ int zzz; // ok: internal linkage
}
```

▶ When using g++ host compiler, an inline variable declared with \_\_managed\_\_ memory space specifier may not be visible to the debugger.

## 18.5.24.2 Structured Binding

A structured binding cannot be declared with a variable memory space specifier.

Example:

```c
struct S { int x; int y; };
__device__ auto [a1, b1] = S{4,5}; // error
```
````
