# CUDA C++ Language Restrictions

CUDA C++ enforces specific language restrictions when compiling code for device execution, particularly regarding extensions provided by the host compiler. These restrictions ensure compatibility between the host and device compilation environments.

## Host Compiler Extensions

Host compiler-specific language extensions are not supported in device code [CUDA_C_Programming_Guide:L16530-L16541]. This means that features specific to GCC, Clang, or MSVC that are not part of the standard CUDA C++ language cannot be used in kernels or device functions.

## Special Type Support

Certain extended types have specific support conditions in device code:

### __Complex Types

The `__Complex` type is only supported in host code [CUDA_C_Programming_Guide:L16530-L16541]. It cannot be used in device code.

### __int128 Type

The `__int128` type is supported in device code, provided that it is compiled in conjunction with a host compiler that supports it [CUDA_C_Programming_Guide:L16530-L16541].

### __float128 Type

The `__float128` type is supported for devices with compute capability 1.0 and later, when compiled in conjunction with a host compiler that supports the type [CUDA_C_Programming_Guide:L16530-L16541]. 

Note that a constant expression of `__float128` type may be processed by the compiler in a floating-point representation with lower precision [CUDA_C_Programming_Guide:L16530-L16541].

## References

- CUDA C++ Programming Guide, Section 18.5.1: Host Compiler Extensions [CUDA_C_Programming_Guide:L16530-L16541]
