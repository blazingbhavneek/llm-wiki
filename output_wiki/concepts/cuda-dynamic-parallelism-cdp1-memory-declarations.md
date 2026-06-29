# CUDA Dynamic Parallelism (CDP1) Memory Declarations

## Overview

In the context of CUDA Dynamic Parallelism version 1 (CDP1), memory declarations for device and constant variables maintain consistency between host-launched and device-launched kernels. This ensures that memory semantics remain predictable regardless of the launch context.

## Device and Constant Memory

Memory declared at file scope with `__device__` or `__constant__` memory space specifiers behaves identically when using the device runtime [CUDA_C_Programming_Guide:L14584-L14593].

### Device Variables

All kernels may read or write device variables, regardless of whether the kernel was initially launched by the host or by the device runtime [CUDA_C_Programming_Guide:L14584-L14593]. This uniform access model simplifies data sharing between hierarchical kernel levels in CDP1.

### Constant Memory

All kernels will have the same view of `__constant__` variables as declared at the module scope [CUDA_C_Programming_Guide:L14584-L14593]. This ensures that constant memory data is consistent across all kernel execution contexts within the same module.

## Note on CDP2

For the updated behavior in CUDA Dynamic Parallelism version 2 (CDP2), refer to the CDP2 version of the Memory Declarations and Device and Constant Memory documentation sections.
