# Lazy Loading (CUDA)

Lazy Loading is a feature in the CUDA programming model that delays the loading of CUDA modules and kernels from program initialization closer to the time of kernel execution. This optimization is designed to be invisible to the user, provided the CUDA Programming Model is followed [CUDA_C_Programming_Guide:L22078-L22091].

## Motivation

In many applications, particularly those that include libraries, programs often utilize only a small subset of the available kernels [CUDA_C_Programming_Guide:L22078-L22091]. Without lazy loading, kernels that are never invoked are still loaded unnecessarily during initialization [CUDA_C_Programming_Guide:L22078-L22091]. Lazy Loading allows programs to load only the kernels that are actually used, thereby saving initialization time and reducing memory overhead on both the GPU and the host [CUDA_C_Programming_Guide:L22078-L22091].

## Implementation Details

Lazy loading involves two primary optimizations introduced in recent CUDA versions:

### 1. Module Loading Delay (CUDA Runtime)

In CUDA 11.8, the CUDA Runtime was updated to no longer load all modules during program initialization [CUDA_C_Programming_Guide:L22078-L22091]. Instead, each module is loaded upon the first usage of a variable or a kernel from that module [CUDA_C_Programming_Guide:L22078-L22091].

*   **Exception:** Modules containing managed variables are still loaded during initialization [CUDA_C_Programming_Guide:L22078-L22091].
*   **Scope:** This optimization is relevant to CUDA Runtime users. CUDA Driver users who use `cuModuleLoad` are unaffected by this specific change [CUDA_C_Programming_Guide:L22078-L22091].

### 2. Kernel Loading Delay (CUDA Runtime and Driver)

Starting in CUDA 11.7, the loading of kernels is delayed until `cuModuleGetFunction()` is called, rather than happening immediately during the `cuModuleLoad*()` family of functions [CUDA_C_Programming_Guide:L22078-L22091].

*   **CUDA Runtime:** The runtime only calls `cuModuleGetFunction()` when a kernel is used or referenced for the first time [CUDA_C_Programming_Guide:L22078-L22091].
*   **CUDA Driver:** This optimization is relevant to both CUDA Runtime and CUDA Driver users [CUDA_C_Programming_Guide:L22078-L22091].
*   **Exceptions:** Some kernels must be loaded during `cuModuleLoad*()`, such as those whose pointers are stored in global variables [CUDA_C_Programming_Guide:L22078-L22091].

## Configuration

Lazy Loading is enabled by setting the `CUDA_MODULE_LOADING` environment variable to `LAZY` [CUDA_C_Programming_Guide:L22078-L22091].

For CUDA Driver users who use `cuLibraryLoad` to load module data into memory, the behavior can be changed by setting the `CUDA_MODULE_DATA_LOADING` environment variable [CUDA_C_Programming_Guide:L22078-L22091].

## References

*   CUDA C Programming Guide: Section 25.1. What is Lazy Loading? [CUDA_C_Programming_Guide:L22078-L22091]
