# Reduce Operators

Function objects mirroring hardware intrinsics for reduction operations. Includes plus, less, greater, bit_and, bit_xor, and bit_or. Designed to match hardware behavior rather than strict STL semantics.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L12890-L12954

Citation: [CUDA_C_Programming_Guide:L12890-L12954]

````text
## 11.6.3.2 Reduce Operators

Below are the prototypes of function objects for some of the basic operations that can be done with reduce

```cpp
namespace cooperative_groups {
  template <typename Ty>
  struct cg::plus;

  template <typename Ty>
  struct cg::less;

  template <typename Ty>
  struct cg::greater;

  template <typename Ty>
  struct cg::bit_and;

  template <typename Ty>
  struct cg::bit_xor;

  template <typename Ty>
  struct cg::bit_or;
}
```

Reduce is limited to the information available to the implementation at compile time. Thus in order to make use of intrinsics introduced in CC 8.0, the cg:: namespace exposes several functional objects that mirror the hardware. These objects appear similar to those presented in the C++ STL, with the exception of less∕greater. The reason for any diference from the STL is that these function objects are designed to actually mirror the operation of the hardware intrinsics.

## Functional description:

▶ cg::plus: Accepts two values and returns the sum of both using operator+.

▶ cg::less: Accepts two values and returns the lesser using operator<. This difers in that the lower value is returned rather than a Boolean.

▶ cg::greater: Accepts two values and returns the greater using operator<. This difers in that the greater value is returned rather than a Boolean.

▶ cg::bit\_and: Accepts two values and returns the result of operator&.

▶ cg::bit\_xor: Accepts two values and returns the result of operator^.

▶ cg::bit\_or: Accepts two values and returns the result of operator|.

## Example:

```cpp
{
    // cg::plus<int> is specialized within cg::reduce and calls __reduce_add_sync(...)
    on CC 8.0+
    cg::reduce(tile, (int)val, cg::plus<int>());
    // cg::plus<float> fails to match with an accelerator and instead performs a
    standard shuffle based reduction
    cg::reduce(tile, (float)val, cg::plus<float>());
    // While individual components of a vector are supported, reduce will not use
    hardware intrinsics for the following
    // It will also be necessary to define a corresponding operator for vector and any
    custom types that may be used
    int4 vec = {...};
    cg::reduce(tile, vec, cg::plus<int4inine)

    // Finally lambdas and other function objects cannot be inspected for dispatch
    // and will instead perform shuffle based reductions using the provided function
    object.
    cg::reduce(tile, (int)val, [](int 1, int r) -> int {return 1 + r;});
}
```
````
