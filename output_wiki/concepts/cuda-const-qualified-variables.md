# Const-Qualified Variables in CUDA

In CUDA C++, variables declared with `const` qualification at namespace scope or as class static members, which lack explicit execution space annotations (such as `__device__`, `__constant__`, or `__shared__`), are treated as **host code variables** [CUDA_C_Programming_Guide:L17406-L17450].

## Usage in Device Code

Although these variables reside in host memory, their values may be directly used in device code under specific conditions [CUDA_C_Programming_Guide:L17406-L17450]. The value of a const variable `V` can be used in device code if all of the following criteria are met:

1.  **Constant Initialization**: `V` has been initialized with a constant expression before the point of use [CUDA_C_Programming_Guide:L17406-L17450].
2.  **Non-Volatile**: The type of `V` is not volatile-qualified [CUDA_C_Programming_Guide:L17406-L17450].
3.  **Supported Types**: The type of `V` is one of the following:
    *   A built-in floating point type (with the exception that this is not supported when the Microsoft compiler is used as the host compiler) [CUDA_C_Programming_Guide:L17406-L17450].
    *   A built-in integral type [CUDA_C_Programming_Guide:L17406-L17450].

## Restrictions

Device source code **cannot** contain a reference to such a host const variable, nor can it take the address of such a variable [CUDA_C_Programming_Guide:L17406-L17450]. Attempting to create a reference or pointer to a namespace-scope or static member const variable in device code results in a compilation error [CUDA_C_Programming_Guide:L17406-L17450].

## Examples

The following example illustrates valid and invalid uses of const variables in device code:

```cpp
const int xxx = 10;
struct S1_t { static const int yyy = 20; };

extern const int zzz;
const float www = 5.0;

__device__ void foo(void) {
    int local1[xxx];          // OK: xxx is a const int initialized with a constant expression
    int local2[S1_t::yyy];   // OK: S1_t::yyy is a static const int initialized with a constant expression

    int val1 = xxx;                // OK
    int val2 = S1_t::yyy;   // OK

    int val3 = zzz;                 // error: zzz is not initialized with a constant expression at the point of use

    const int &val3 = xxx;     // error: reference to host variable
    const int *val4 = &xxx;   // error: address of host variable
    
    const float val5 = www;   // OK except when the Microsoft compiler is used as the host compiler
}

const int zzz = 20;
```

In this example:
*   `xxx` and `S1_t::yyy` are valid because they are integral types initialized with constant expressions.
*   `zzz` is invalid in device code because it is declared `extern` and not initialized with a constant expression at the point of use within `foo`.
*   Taking the address or reference of `xxx` is prohibited.
*   `www` is a floating-point const variable, which is valid on non-Microsoft host compilers.
