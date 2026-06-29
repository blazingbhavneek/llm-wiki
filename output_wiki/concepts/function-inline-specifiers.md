# Function Inline Specifiers

In CUDA C++, the compiler automatically inlines `__device__` functions when it deems appropriate for performance or code size optimization. Developers can override or guide this behavior using specific function qualifiers.

## Qualifiers

### `__noinline__`
The `__noinline__` function qualifier serves as a hint to the compiler not to inline the function, if possible. This is useful when inlining would negatively impact code size or when the function's execution characteristics are better managed as a separate call.

### `__forceinline__`
The `__forceinline__` function qualifier forces the compiler to inline the function. This is typically used when inlining is critical for performance, such as in small, frequently called kernels or device functions.

## Constraints

There are strict rules regarding the usage of these qualifiers:

1.  **Mutual Exclusivity**: The `__noinline__` and `__forceinline__` qualifiers cannot be used together on the same function.
2.  **Incompatibility with `inline`**: Neither `__noinline__` nor `__forceinline__` can be applied to a function that is already declared as `inline`.

## References

- CUDA C++ Programming Guide, Section 10.1.5 [CUDA_C_Programming_Guide:L6610-L6619]
