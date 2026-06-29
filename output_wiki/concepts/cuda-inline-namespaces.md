# Inline Namespaces in CUDA

When compiling a CUDA translation unit, the CUDA compiler may invoke the host compiler to process the host code sections. During this process, the CUDA compiler injects additional compiler-generated code into the host code if the translation unit contains definitions of specific CUDA entities [CUDA_C_Programming_Guide:L17660-L17711].

## Injected Entities

The compiler-generated code includes references to definitions of the following entities:

* `__global__` functions or function template instantiations
* `__device__` and `__constant__` variables
* Variables with surface or texture types [CUDA_C_Programming_Guide:L17660-L17711]

## The Ambiguity Issue

If an entity defined in the CUDA code is located within an inline namespace, and another entity with the same name and type signature exists in an enclosing namespace, the reference injected by the CUDA compiler may be considered ambiguous by the host compiler. This ambiguity results in a host compilation failure [CUDA_C_Programming_Guide:L17660-L17711].

### Example 1: Direct Conflict

In this example, a global variable `Gvar` is defined at the global scope and again within an inline namespace `N1`. The CUDA compiler inserts a reference to `Gvar` in the host code. Because `N1` is inline, its contents are visible at the global scope, creating an ambiguity with the global `Gvar` [CUDA_C_Programming_Guide:L17660-L17711].

```cpp
__device__ int Gvar;
inline namespace N1 {
  __device__ int Gvar;
}
// The CUDA compiler inserts a reference to "Gvar" here.
// This reference is ambiguous to the host compiler.
```

### Example 2: Nested Namespace Conflict

Ambiguity can also occur with nested namespaces. If `Gvar` is defined inside `N2` within an inline namespace `N1`, and another `Gvar` is defined in a separate `N2` at the global scope, the injected reference to `::N2::Gvar` becomes ambiguous [CUDA_C_Programming_Guide:L17660-L17711].

```cpp
inline namespace N1 {
    namespace N2 {
        __device__ int Gvar;
    }
}

namespace N2 {
    __device__ int Gvar;
}
// The CUDA compiler inserts a reference to "::N2::Gvar" here.
// This reference is ambiguous to the host compiler.
```

## Resolution

To avoid compilation failures caused by this ambiguity, developers should use unique names for entities defined within inline namespaces that might conflict with entities in enclosing namespaces [CUDA_C_Programming_Guide:L17660-L17711].
