# Allocation and Deallocation Functions

In CUDA C++, memory allocation and deallocation are handled by specific built-in functions provided by the compiler. These builtins ensure proper memory management for both host (`__host__`) and device (`__device__`) execution contexts.

## Restrictions on User-Defined Functions

A user-defined `operator new`, `operator new[]`, `operator delete`, or `operator delete[]` cannot be used to replace the corresponding `__host__` or `__device__` builtins provided by the compiler [CUDA_C_Programming_Guide:L17271-L17274].

This restriction ensures that the underlying memory management mechanisms required for GPU execution remain consistent and are not overridden by custom implementations that may not adhere to the necessary constraints for device code.

## Related Operators

The following operators are subject to these restrictions:

*   `operator new`
*   `operator new[]`
*   `operator delete`
*   `operator delete[]`

These operators are integral to the C++ memory model but their behavior in CUDA is strictly controlled by the compiler's built-in implementations for both host and device targets.

## See Also

*   CUDA C++ Programming Guide
*   Memory Management
*   Device Functions
