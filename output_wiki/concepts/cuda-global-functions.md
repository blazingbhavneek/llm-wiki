# __global__ Functions in CUDA

__global__ functions in CUDA are subject to specific restrictions regarding constexpr declarations, parameter types (excluding std::initializer_list, va_list, and rvalue references), variadic template pack placement, and the requirements for lambda closure types used as template arguments.

## constexpr Restriction

A __global__ function or function template cannot be declared as constexpr [CUDA_C_Programming_Guide:L17756-L17836].

## Parameter Type Restrictions

__global__ functions have strict limitations on the types of parameters they can accept:

*   A __global__ function or function template cannot have a parameter of type `std::initializer_list` or `va_list` [CUDA_C_Programming_Guide:L17756-L17836].
*   A __global__ function cannot have a parameter of rvalue reference type [CUDA_C_Programming_Guide:L17756-L17836].

## Variadic Template Restrictions

A variadic __global__ function template has the following restrictions:

1.  Only a single pack parameter is allowed [CUDA_C_Programming_Guide:L17756-L17836].
2.  The pack parameter must be listed last in the template parameter list [CUDA_C_Programming_Guide:L17756-L17836].

### Examples

The following examples illustrate valid and invalid variadic __global__ function templates:

```cpp
// ok
template <template <typename...> class Wrapper, typename... Pack>
__global__ void foo1(Wrapper<Pack...>);

// error: pack parameter is not last in parameter list
template <typename... Pack, template <typename...> class Wrapper>
__global__ void foo2(Wrapper<Pack...>);

// error: multiple parameter packs
template <typename... Pack1, int...Pack2, template<typename...> class Wrapper1,
    template<int...> class Wrapper2>
__global__ void foo3(Wrapper1<Pack1...>, Wrapper2<Pack2...>);
```

## Lambda Closure Types in __global__ Function Templates

If the closure type associated with a lambda expression is used in a template argument of a __global__ function template instantiation, the lambda expression must either be defined in the immediate or nested block scope of a __device__ or __global__ function, or must be an extended lambda [CUDA_C_Programming_Guide:L17756-L17836].

### Valid Usage

The following examples demonstrate valid instantiations where the lambda is defined within a __device__ function or is an extended lambda:

```cpp
template <typename T>
__global__ void kernel(T in) { }

__device__ void foo_device(void)
{
    // All kernel instantiations in this function
    // are valid, since the lambdas are defined inside
    // a __device__ function.

    kernel<<<1,1>>>( [] __device__ { } );
    kernel<<<1,1>>>( [] __host__ __device__ { } );
    kernel<<<1,1>>>( [] { } );
}

void foo_host(void)
{
    // OK: instantiated with closure type of an extended __device__ lambda
    kernel<<<1,1>>>( [] __device__ { } );

    // OK: instantiated with closure type of an extended __host__ __device__
    // lambda
    kernel<<<1,1>>>( [] __host__ __device__ { } );
}
```

### Invalid Usage

The following examples demonstrate invalid instantiations where the lambda is not an extended lambda and is not defined within a __device__ or __global__ function scope:

```cpp
auto lam1 = [] { };

auto lam2 = [] __host__ __device__ { };

void foo_host(void)
{
    // error: unsupported: instantiated with closure type of a lambda
    // that is not an extended lambda
    kernel<<<1,1>>>( [] { } );

    // error: unsupported: instantiated with closure type of a lambda
    // that is not an extended lambda
    kernel<<<1,1>>>( lam1);

    // error: unsupported: instantiated with closure type of a lambda
    // that is not an extended lambda
    kernel<<<1,1>>>( lam2);
}
```

In the invalid examples, `lam1` and `lam2` are defined in host scope but are not extended lambdas (in the case of `lam1`, it lacks any specifier; in the case of `lam2`, while it has `__host__ __device__`, it is not an extended lambda in the context of being passed to a __global__ template from host scope without being defined in a __device__/__global__ block scope, or the specific compiler interpretation of "extended lambda" for this restriction). Specifically, the documentation notes that passing `lam1` and `lam2` from `foo_host` results in an error because they are not extended lambdas or defined in the required scope [CUDA_C_Programming_Guide:L17756-L17836].
