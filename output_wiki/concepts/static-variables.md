# Static Variables within Function

Static variables can be declared within the immediate or nested block scope of a function, subject to specific constraints regarding the function's execution space and memory space specifiers.

## Scope and Function Types

Variable memory space specifiers are permitted in the declaration of a static variable `V` within a function `F` under the following conditions:

*   `F` is a `__global__` or `__device__`-only function.
*   `F` is a `__host__ __device__` function and the macro `__CUDA_ARCH__` is defined during compilation [CUDA_C_Programming_Guide:L17156-L17163].

## Implicit Memory Space Specifiers

If no explicit memory space specifier is present in the declaration of a static variable, an implicit `__device__` specifier is assumed during device compilation [CUDA_C_Programming_Guide:L17165-L17166].

## Initialization Restrictions

Static variables within function scope are subject to the same initialization restrictions as variables with equivalent memory space specifiers declared in namespace scope. For example, a `__device__` variable cannot have a "non-empty" constructor [CUDA_C_Programming_Guide:L17168-L17170].

### Prohibited Initializations

Dynamic initialization is not allowed for static variables within functions. The following are considered errors:

*   Initialization with a non-constant expression (e.g., `static int i6 = x;` where `x` is a local variable) [CUDA_C_Programming_Guide:L17198-L17199].
*   Initialization with aggregate members that depend on non-constant expressions (e.g., `static S1_t i7 = {x};`) [CUDA_C_Programming_Guide:L17200].
*   Initialization of types with non-empty constructors (e.g., `static S2_t i8;` or `static S3_t i9(44);`) [CUDA_C_Programming_Guide:L17202-L17203].

### Host/Device Compilation Differences

For `__host__ __device__` functions, the visibility and validity of memory space specifiers depend on whether the code is being compiled for the host or the device:

*   **Device Compilation (`__CUDA_ARCH__` defined):**
    *   Implicit `__device__` specifiers are applied [CUDA_C_Programming_Guide:L17207-L17208].
    *   Explicit `__device__` declarations are valid [CUDA_C_Programming_Guide:L17210-L17211].
*   **Host Compilation (`__CUDA_ARCH__` not defined):**
    *   Explicit `__device__` or `__shared__` variables inside a host function are errors, as these specifiers are not valid during host compilation [CUDA_C_Programming_Guide:L17215-L17223].
    *   Host-only static variables (e.g., `static int d0;`) are valid when guarded by `#ifndef __CUDA_ARCH__` [CUDA_C_Programming_Guide:L17217-L17220].

## Examples

### Legal Uses

```cpp
struct S1_t {
  int x;
};

__device__ void f1() {
  static int i1;                 // OK, implicit __device__ memory space specifier
  static int i2 = 11;         // OK, implicit __device__ memory space specifier
  static __managed__ int m1;   // OK
  static __device__ int d1;    // OK
  static __constant__ int c1; // OK

  static S1_t i3;             // OK, implicit __device__ memory space specifier
  static S1_t i4 = {22};       // OK, implicit __device__ memory space specifier

  static __shared__ int i5;   // OK
}
```

### Illegal Uses

```cpp
struct S2_t {
  int x;
  __device__ S2_t(void) { x = 10; } // Non-empty constructor
};

struct S3_t {
  int x;
  __device__ S3_t(int p) : x(p) { } // Constructor with parameters
};

__device__ void f1() {
  int x = 33;
  static int i6 = x;           // error: dynamic initialization is not allowed
  static S1_t i7 = {x};        // error: dynamic initialization is not allowed

  static S2_t i8;             // error: dynamic initialization is not allowed
  static S3_t i9(44);       // error: dynamic initialization is not allowed
}

__host__ __device__ void f2() {
  static __device__ int d2;   // error: __device__ variable inside
                              // a host function during host compilation
                              // i.e. when __CUDA_ARCH__ is not defined

  static __shared__ int i2;   // error: __shared__ variable inside
                              // a host function during host compilation
                              // i.e. when __CUDA_ARCH__ is not defined
}
```

## See Also

*   [Device Memory Space Specifiers]
*   [CUDA Architecture Macros]
