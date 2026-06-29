# __nv_pure__ Attribute in CUDA

The `__nv_pure__` attribute is supported for both host and device functions [CUDA_C_Programming_Guide:L17520-L17527].

## Host Functions

For host functions, the attribute behavior depends on the compiler and language dialect:

*   When using a language dialect that supports the `pure` GNU attribute, `__nv_pure__` is translated to the `pure` GNU attribute [CUDA_C_Programming_Guide:L17520-L17527].
*   When using MSVC as the host compiler, the attribute is translated to the MSVC `noalias` attribute [CUDA_C_Programming_Guide:L17520-L17527].

## Device Functions

When a device function is annotated with the `__nv_pure__` attribute, the device code optimizer assumes that the function does not change any mutable state visible to caller functions, such as memory [CUDA_C_Programming_Guide:L17520-L17527].

## See Also

*   CUDA C++ Programming Guide Section 18.5.20
