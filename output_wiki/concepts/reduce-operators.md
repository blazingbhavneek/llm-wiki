# Reduce Operators

Reduce operators are function objects provided by the `cooperative_groups` (cg) namespace to facilitate reduction operations within cooperative groups. These operators are designed to mirror the behavior of hardware intrinsics available on Compute Capability 8.0 and newer, while maintaining an interface similar to the C++ Standard Template Library (STL) [CUDA_C_Programming_Guide:L12889-L12954].

## Available Operators

The following function objects are defined for basic reduction operations:

*   `cg::plus<Ty>`: Returns the sum of two values using `operator+` [CUDA_C_Programming_Guide:L12889-L12954].
*   `cg::less<Ty>`: Returns the lesser of two values using `operator<` [CUDA_C_Programming_Guide:L12889-L12954].
*   `cg::greater<Ty>`: Returns the greater of two values using `operator<` [CUDA_C_Programming_Guide:L12889-L12954].
*   `cg::bit_and<Ty>`: Returns the result of bitwise AND (`operator&`) [CUDA_C_Programming_Guide:L12889-L12954].
*   `cg::bit_xor<Ty>`: Returns the result of bitwise XOR (`operator^`) [CUDA_C_Programming_Guide:L12889-L12954].
*   `cg::bit_or<Ty>`: Returns the result of bitwise OR (`operator|`) [CUDA_C_Programming_Guide:L12889-L12954].

## Differences from STL

A key distinction between these cooperative group operators and their STL counterparts is the return type of comparison operations. While STL comparators typically return a boolean, `cg::less` and `cg::greater` return the actual value (the lesser or greater operand, respectively) [CUDA_C_Programming_Guide:L12889-L12954]. This design choice allows the function objects to directly mirror the operation of underlying hardware intrinsics [CUDA_C_Programming_Guide:L12889-L12954].

## Implementation Details and Dispatch

The `reduce` function relies on compile-time information to determine the implementation strategy. On Compute Capability 8.0 and above, specific operator types can trigger the use of hardware intrinsics [CUDA_C_Programming_Guide:L12889-L12954].

*   **Integer Types**: Specializations such as `cg::plus<int>` are optimized to call hardware intrinsics like `__reduce_add_sync` [CUDA_C_Programming_Guide:L12889-L12954].
*   **Floating-Point Types**: Specializations like `cg::plus<float>` may not match an accelerator intrinsic and will instead fall back to a standard shuffle-based reduction [CUDA_C_Programming_Guide:L12889-L12954].
*   **Vector Types**: While individual components of vector types (e.g., `int4`) are supported, `reduce` will not use hardware intrinsics for them. Users must define corresponding operators for custom or vector types [CUDA_C_Programming_Guide:L12889-L12954].
*   **Lambdas and Custom Objects**: Lambdas and other function objects cannot be inspected for dispatch optimization. Consequently, they will perform shuffle-based reductions using the provided function object rather than leveraging hardware intrinsics [CUDA_C_Programming_Guide:L12889-L12954].

## Example Usage

```cpp
{
    // cg::plus<int> is specialized within cg::reduce and calls __reduce_add_sync(...)
    // on CC 8.0+
    cg::reduce(tile, (int)val, cg::plus<int>());

    // cg::plus<float> fails to match with an accelerator and instead performs a
    // standard shuffle based reduction
    cg::reduce(tile, (float)val, cg::plus<float>());

    // While individual components of a vector are supported, reduce will not use
    // hardware intrinsics for the following.
    // It will also be necessary to define a corresponding operator for vector and any
    // custom types that may be used.
    int4 vec = {...};
    cg::reduce(tile, vec, cg::plus<int4>());

    // Finally lambdas and other function objects cannot be inspected for dispatch
    // and will instead perform shuffle based reductions using the provided function
    // object.
    cg::reduce(tile, (int)val, [](int l, int r) -> int {return l + r;});
}
```

## References

*   CUDA C++ Programming Guide, Section 11.6.3.2 Reduce Operators [CUDA_C_Programming_Guide:L12889-L12954]
