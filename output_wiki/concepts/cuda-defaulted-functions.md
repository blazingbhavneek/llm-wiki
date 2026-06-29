# Defaulted Functions in CUDA

In CUDA C++, the handling of execution space specifiers (such as `__host__`, `__device__`, and `__global__`) on explicitly defaulted functions depends on whether the function is virtual and whether the defaulting occurs on the first declaration.

## Behavior on First Declaration

For a **non-virtual** function that is explicitly defaulted on its **first declaration**, the CUDA compiler ignores any execution space specifiers present on the defaulted declaration. Instead, the compiler infers the execution space specifier based on the context in which the function is called, as described in the rules for implicitly-declared and non-virtual explicitly-defaulted functions [CUDA_C_Programming_Guide:L17840-L17900].

For example, if a constructor is defaulted on its first declaration with a `__host__` specifier, that specifier is ignored. If the constructor is subsequently called from a `__device__` function, the compiler derives the `__device__` execution space for the constructor based on that implicit call [CUDA_C_Programming_Guide:L17840-L17900].

## Exceptions: Virtual and Subsequent Declarations

Execution space specifiers are **not** ignored in the following cases:

1.  **Virtual Functions**: If the function is virtual, the execution space specifier is preserved even if defaulted on the first declaration [CUDA_C_Programming_Guide:L17840-L17900].
2.  **Subsequent Declarations**: If the function is explicitly defaulted but **not** on its first declaration, the execution space is fixed based on the first declaration and is not inferred [CUDA_C_Programming_Guide:L17840-L17900].

## Examples

### Ignored Specifier on First Declaration (Non-Virtual)

In the following example, the `__host__` specifier on `S1`'s constructor is ignored because it is defaulted on the first declaration and the function is non-virtual. The execution space is inferred from the call site in `foo1`.

```cpp
struct S1 {
  // warning: __host__ annotation is ignored on a non-virtual function that
  //          is explicitly-defaulted on its first declaration
  __host__ S1() = default;
};

__device__ void foo1() {
    // note: __device__ execution space is derived for S1::S1
    //       based on implicit call from within __device__ function
    //       foo1
    S1 s1;
}
```

### Preserved Specifier on Subsequent Declaration

In this case, `S2`'s constructor is declared with `__host__` on its first declaration. The defaulted definition on a subsequent line preserves this specifier. Calling it from a `__device__` function results in an error.

```cpp
struct S2 {
    __host__ S2();
};

// note: S2::S2 is not defaulted on its first declaration, and
//       its execution space is fixed to __host__  based on its
//       first declaration.
S2::S2() = default;

__device__ void foo2() {
    // error: call from __device__ function 'foo2' to
    //       __host__ function 'S2::S2'
    S2 s2;
}
```

### Preserved Specifier on Virtual Function

Virtual functions preserve their execution space specifiers even when defaulted on the first declaration. Attempting to call a `__host__` virtual destructor from a `__device__` function results in an error.

```cpp
struct S3 {
    // note: S3::~S3 has __host__ execution space
    virtual __host__ ~S3() = default;
};

__device__ void foo3() {
    S3 qqq;
}  /*(implicit destructor call for 'qqq'):
        error: call from a __device__ fuction 'foo3' to a
        __host__ function 'S3::~S3' */
```
