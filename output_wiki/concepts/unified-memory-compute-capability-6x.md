# Unified Memory on Devices with Compute Capability 6.x+

Describes full support for CUDA Managed Memory on devices with compute capability 6.x or higher but without pageable memory access, noting the exclusion of system allocators.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21816-L21825

Citation: [CUDA_C_Programming_Guide:L21816-L21825]

````text
## 24.3. Unified memory on devices without full CUDA Unified Memory support

## 24.3.1. Unified memory on devices with only CUDA Managed Memory support

For devices with compute capability 6.x or higher but without pageable memory access, CUDA Managed Memory is fully supported and coherent. The programming model and performance tuning of unified memory is largely similar to the model as described in Unified memory on devices with full CUDA Unified Memory support, with the notable exception that system allocators cannot be used to allocate memory. Thus, the following list of sub-sections do not apply:

▶ System-Allocated Memory: in-depth examples

▶ Hardware/Software Coherency
````
