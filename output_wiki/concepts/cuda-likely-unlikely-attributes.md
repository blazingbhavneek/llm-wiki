# Likely/Unlikely Attributes in CUDA

The `[[likely]]` and `[[unlikely]]` standard attributes are supported in all CUDA configurations that accept C++ standard attribute syntax. These attributes serve as hints to the device compiler optimizer regarding the expected frequency of execution for specific code paths.

## Purpose and Usage

Developers can use these attributes to indicate whether a statement is more or less likely to be executed compared to alternative paths that do not include the statement. This information can help the optimizer make better decisions regarding instruction scheduling and branch prediction.

### Example

The following example demonstrates the usage of these attributes within a device function:

```cpp
__device__ int foo(int x) {
  if (i < 10) [[likely]] { // the 'if' block will likely be entered
    return 4;
  }
  if (i < 20) [[unlikely]] { // the 'if' block will not likely be entered
    return 1;
  }
  return 0;
}
```

## Host Code Considerations

When these attributes are used in host code (i.e., when `__CUDA_ARCH__` is undefined), the attributes remain in the code parsed by the host compiler. If the host compiler does not support C++ standard attributes, it may generate warnings, such as an 'unknown attribute' warning. For instance, the Clang 11 host compiler is known to generate such warnings when encountering these attributes [CUDA_C_Programming_Guide:L17468-L17488].

## References

- CUDA C++ Programming Guide, Section 18.5.18: [[likely]] / [[unlikely]] Standard Attributes [CUDA_C_Programming_Guide:L17468-L17488]
