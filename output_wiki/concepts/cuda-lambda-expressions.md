# Lambda Expressions in CUDA

Lambda expressions in CUDA are subject to specific rules regarding execution space specifiers and template instantiation, particularly when interacting with device code.

## Execution Space Specifiers

The execution space specifiers for all member functions of the closure class associated with a lambda expression are derived by the compiler based on the enclosing scope. As per the C++11 standard, the compiler creates a closure type in the smallest block scope, class scope, or namespace scope that contains the lambda expression. The compiler then computes the innermost function scope enclosing the closure type and assigns the corresponding function’s execution space specifiers to the closure class member functions. If there is no enclosing function scope, the execution space specifier defaults to `__host__` [CUDA_C_Programming_Guide:L17535-L17591].

### Examples

The following examples illustrate how the execution space of a lambda is determined by its enclosing function:

```cpp
// No enclosing function scope; defaults to __host__
auto globalVar = [] { return 0; }; 

void f1(void) {
    auto l1 = [] { return 1; };      // __host__
}

__device__ void f2(void) {
    auto l2 = [] { return 2; };      // __device__
}

__host__ __device__ void f3(void) {
    auto l3 = [] { return 3; };      // __host__ __device__
}

// Default argument lambda is __host__ unless specified otherwise
__device__ void f4(int (*fp)() = [] { return 4; } /* __host__ */) {
}

__global__ void f5(void) {
    auto l5 = [] { return 5; };      // __device__
}

__device__ void f6(void) {
    struct S1_t {
        static void helper(int (*fp)() = [] {return 6; } /* __device__ */) {
        }
    };
}
```

## Restrictions on Template Arguments

The closure type of a lambda expression cannot be used in the type or non-type argument of a `__global__` function template instantiation, unless the lambda is defined within a `__device__` or `__global__` function [CUDA_C_Programming_Guide:L17535-L17591].

### Invalid Usage Example

The following code demonstrates invalid usage where a lambda closure type is passed to a `__global__` template function:

```cpp
template <typename T>
__global__ void foo(T in) { };

template <typename T>
struct S1_t { };

void bar(void) {
  auto temp1 = [] { };

  // Error: lambda closure type used in template type argument
  foo<<<1,1>>>(temp1);                      
  
  // Error: lambda closure type used in template type argument
  foo<<<1,1>>>( S1_t<decltype(temp1)>()); 
}
```

In this example, `temp1` is defined in a `__host__` function (`bar`), so its closure type is not eligible for use in the template argument of the `__global__` function `foo` [CUDA_C_Programming_Guide:L17535-L17591].
