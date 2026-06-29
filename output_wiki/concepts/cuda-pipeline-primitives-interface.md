# Pipeline Primitives Interface

Pipeline primitives provide a C-like interface for `memcpy_async` functionality, enabling asynchronous memory transfers with explicit synchronization control [CUDA_C_Programming_Guide:L10149-L10151].

## Header Inclusion

The availability of the interface depends on the compilation environment:

*   **ISO C++ 2011 Compatible**: Include the `<cuda_pipeline.h>` header [CUDA_C_Programming_Guide:L10149-L10151].
*   **Non-ISO C++ 2011 Compatible**: Include the `<cuda_pipeline_primitives.h>` header [CUDA_C_Programming_Guide:L10149-L10151].

## Usage Context

This interface is part of the CUDA runtime library's support for asynchronous memory operations, allowing developers to manage pipeline stages for memory copies explicitly [CUDA_C_Programming_Guide:L10149-L10151].
