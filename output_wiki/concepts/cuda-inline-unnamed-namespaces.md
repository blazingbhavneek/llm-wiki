# Inline Unnamed Namespaces in CUDA

In CUDA C++, inline unnamed namespaces (also known as anonymous inline namespaces) provide a mechanism to introduce names into the enclosing scope while maintaining namespace semantics. However, certain CUDA-specific entities are restricted from being declared at the namespace scope within these inline unnamed namespaces.

## Restrictions on CUDA Entities

The following entities cannot be declared in namespace scope within an inline unnamed namespace:

*   Variables with the `__managed__`, `__device__`, `__shared__`, or `__constant__` storage class specifiers.
*   `__global__` functions and function templates.
*   Variables with surface or texture types.

These restrictions apply because these entities have specific linkage and execution space requirements that are incompatible with the namespace scope resolution rules within an inline unnamed namespace.

## Example

The following code demonstrates the errors that occur when attempting to declare restricted entities within an inline unnamed namespace:

```cpp
inline namespace {
  namespace N2 {
    template <typename T>
      __global__ void foo(void);          // error

      __global__ void bar(void) { }         // error

      template <>
      __global__ void foo<int>(void) { }     // error

      __device__ int x1b;                    // error

      __constant__ int x2b;                     // error
      __shared__ int x3b;                       // error

      texture<int> q2;                            // error
      surface<int> s2;                            // error
  }
};
```

In this example, all declarations inside `namespace N2` (which is inside the inline unnamed namespace) that involve CUDA-specific storage classes or execution spaces result in compilation errors.

## References

[CUDA_C_Programming_Guide:L17712-L17751]
