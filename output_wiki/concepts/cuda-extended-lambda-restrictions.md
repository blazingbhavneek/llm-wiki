# CUDA Extended Lambda Restrictions

CUDA C++ extended lambdas, which are marked with both `__host__` and `__device__` specifiers, are subject to several syntactic and semantic restrictions to ensure correct compilation and execution across host and device environments.

## Restrictions on Definition Context

An extended lambda cannot be defined inside a class that is local to a function. This restriction prevents the lambda from capturing context that is not properly supported across the host-device boundary.

For example, the following code results in an error because the lambda `lam4` is defined within `bar`, which is a member of `S1_t`, a class local to the function `foo`:

```cpp
void foo(void) {
    struct S1_t {
        void bar(void) {
            // Error: bar is member of a class that is local to a function.
            auto lam4 = [] __host__ __device__ { return 0; };
        }
    };
}
```

## Restrictions on Enclosing Function Return Type

The enclosing function for an extended lambda cannot have a deduced return type. The compiler requires explicit type information to correctly generate the necessary host and device code paths.

For example, defining an extended lambda inside a function with a deduced return type (using `auto`) is an error:

```cpp
auto foo(void) {
  // Error: the return type of foo is deduced.
  auto lam1 = [] __host__ __device__ { return 0; };
}
```

## Restrictions on Generic Lambdas

`__host__ __device__` extended lambdas cannot be generic lambdas. Generic lambdas, which use `auto` parameters to deduce argument types at call time, are incompatible with the extended lambda model in CUDA.

The following examples demonstrate errors when attempting to create generic extended lambdas:

```cpp
void foo(void) {
    // Error: __host__ __device__ extended lambdas cannot be
    // generic lambdas.
    auto lam1 = [] __host__ __device__ (auto i) { return i; };

    // Error: __host__ __device__ extended lambdas cannot be
    // generic lambdas.
    auto lam2 = [] __host__ __device__ (auto ...i) {
        return sizeof...(i);
        };
}
```

## References

- [CUDA_C_Programming_Guide:L18516-L18558]
