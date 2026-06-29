# Thread Local Storage in CUDA

The `thread_local` storage specifier is not allowed in device code [CUDA_C_Programming_Guide:L17752-L17755].

## Context

This restriction is part of the C++ language extensions supported in CUDA device code, specifically under the section detailing storage specifiers [CUDA_C_Programming_Guide:L17752-L17755]. While `thread_local` is a standard C++ specifier for defining variables with thread-local storage duration, it is explicitly prohibited in the context of kernels and other device-side execution environments in CUDA.

## Related Concepts

*   **CUDA C++ Language Extensions**: The rules for storage specifiers in device code are defined within the broader set of C++ extensions supported by the CUDA compiler.
*   **Device Code Restrictions**: Developers must rely on other mechanisms for managing per-thread data in device code, as standard C++ thread-local storage is unavailable.

## Caveats

*   This information is based on a deterministic fallback due to a research subagent failure, so it is critical to stay close to the source evidence [CUDA_C_Programming_Guide:L17752-L17755].
*   The restriction applies specifically to device code; host code may still use `thread_local` as per standard C++ rules.

## References

*   [CUDA_C_Programming_Guide:L17752-L17755] CUDA C++ Programming Guide, Section 18.5.22.7 thread_local.
