# Noreturn Annotation in CUDA

The NVIDIA CUDA compiler (`nvcc`) supports the `noreturn` annotation for both host and device functions. This annotation indicates that a function does not return control to its caller, typically because it terminates the program or enters an infinite loop.

## Supported Syntax

The specific syntax supported depends on the host compiler being used and the C++ dialect enabled:

*   **GCC, Clang, xlC, ICC, or PGCC**: When using these host compilers, the `__attribute__((noreturn))` syntax is supported.
*   **MSVC (cl.exe)**: When using the Microsoft Visual C++ compiler, the `__declspec(noreturn)` syntax is supported.
*   **C++11 Dialect**: When the C++11 dialect is enabled, the standard `[[noreturn]]` attribute is supported.

These annotations can be applied to both host-side and device-side functions within CUDA code.

## References

- CUDA C++ Programming Guide, Section 18.5.17: Noreturn Annotation [CUDA_C_Programming_Guide:L17462-L17467]
