# CUDA C++17 constexpr Host/Device Interaction Rules

In CUDA C++17, `constexpr` functions can be marked with `__host__`, `__device__`, or both qualifiers. When these functions are called across host and device boundaries, specific rules apply regarding code generation, One Definition Rule (ODR) usage, and supported language features. The compiler may not always emit diagnostics for invalid usage that violates these rules, potentially leading to silent failures.

## Device Code Generation for `__host__`-only `constexpr` Functions

When a `constexpr` function is marked `__host__` only, it is normally executed on the host. However, if it is called from device code in a non-`constexpr` context, the compiler generates device code for its body.

### Emission of Device Code

During device code generation, device code is generated for the body of a `__host__`-only `constexpr` function `H`, unless `H` is not used or is only called in a `constexpr` context [CUDA_C_Programming_Guide:L19117-L19206].

**Example:**
```c
// NOTE: "H" is emitted in generated device code because it is
// called from device code in a non-constexpr context
constexpr __host__ int H(int x) { return x+1; }

__device__ int doit(int in) {
  in = H(in);  // OK, even though argument is not a constant expression
  return in;
}
```

### Restrictions on `__host__`-only `constexpr` Functions Called from Device

All code restrictions applicable to a `__device__` function are also applicable to the `constexpr` `__host__`-only function `H` that is called from device code [CUDA_C_Programming_Guide:L19117-L19206]. However, the compiler may not emit any build-time diagnostics for `H` for these restrictions [CUDA_C_Programming_Guide:L19117-L19206].

Unsupported patterns in the body of `H` (as with any `__device__` function) include:

1.  **ODR-use of host variables or `__host__`-only non-`constexpr` functions:**
    If `H` attempts to refer to host variables or other host-only functions, the code may compile but will not execute correctly [CUDA_C_Programming_Guide:L19117-L19206].

    **Example:**
    ```c
    int qqq, www;
    constexpr __host__ int* H(bool b) { return b ? &qqq : &www; };
    __device__ int doit(bool flag) {
      int *ptr;
      ptr = H(flag); // ERROR: H() attempts to refer to host variables 'qqq' and 'www'.
                     // code will compile, but will NOT execute correctly.
      return *ptr;
    }
    ```

2.  **Use of exceptions and RTTI:**
    The use of `throw`/`catch` and RTTI features like `typeid` and `dynamic_cast` is unsupported in device code [CUDA_C_Programming_Guide:L19117-L19206].

    **Example:**
    ```c
    struct Base { };
    struct Derived : public Base { };

    // NOTE: "H" is emitted in generated device code
    constexpr int H(bool b, Base *ptr) {
      if (b) {
        return 1;
      } else if (typeid(ptr) == typeid(Derived)) { // ERROR: use of typeid in code executing on the GPU
        return 2;
      } else {
        throw int{4}; // ERROR: use of throw in code executing on the GPU
      }
    }
    __device__ void doit(bool flag) {
      int val;
      Derived d;
      val = H(flag, &d); //ERROR: H() attempts use typeid and throw(), which are not allowed in code that executes on the GPU
    }
    ```

## Host Code Generation for `__device__`-only `constexpr` Functions

When a `constexpr` function is marked `__device__` only, its body is preserved in the code sent to the host compiler if it is called from host code. However, similar ODR restrictions apply.

### Restrictions on `__device__`-only `constexpr` Functions Called from Host

If the body of a `__device__`-only `constexpr` function `D` attempts to ODR-use a namespace scope device variable or a `__device__`-only non-`constexpr` function, then the call to `D` from host code is not supported [CUDA_C_Programming_Guide:L19117-L19206]. The code may build without compiler diagnostics but may behave incorrectly at runtime [CUDA_C_Programming_Guide:L19117-L19206].

**Example:**
```c
__device__ int qqq, www;
constexpr __device__ int* D(bool b) { return b ? &qqq : &www; };

int doit(bool flag) {
    int *ptr;
    ptr = D(flag); // ERROR: D() attempts to refer to device variables 'qqq' and 'www'
                   // code will compile, but will NOT execute correctly.
    return *ptr;
}
```

## Warnings Regarding Standard Library Headers

Due to the restrictions on ODR-use and the potential lack of compiler diagnostics for incorrect usage, caution is advised when calling a `constexpr` `__host__` function from standard C++ headers from device code [CUDA_C_Programming_Guide:L19117-L19206].

The implementation of such functions may vary depending on the host platform, such as based on the `libstdc++` version for the GCC host compiler [CUDA_C_Programming_Guide:L19117-L19206]. If the target C++ library implementation ODR-uses a host code variable or function, the code may break silently when being ported to a different platform or host compiler version [CUDA_C_Programming_Guide:L19117-L19206].

**Example:**
```cpp
__device__ int get(int in) {
    int val = std::foo(in); // "std::foo" is constexpr function defined in
                            // the host compiler's standard library header
                            // WARNING: if std::foo implementation ODR-
                            // uses host variables or functions,
                            // code will not work correctly
}
```

## Summary of Key Points

*   **`__host__` `constexpr` in device code:** The function body is compiled for the device if called in a non-`constexpr` context. It must adhere to all `__device__` restrictions (no exceptions, no RTTI, no ODR-use of host variables/functions).
*   **`__device__` `constexpr` in host code:** The function body is preserved for the host. It must not ODR-use device variables or `__device__`-only functions.
*   **Silent Failures:** The compiler may not generate diagnostics for violations of these rules, leading to runtime errors or incorrect behavior.
*   **Standard Library Risks:** Using `constexpr` functions from standard headers in device code is risky due to potential ODR-use of host-specific variables or functions that vary by platform/compiler version.
