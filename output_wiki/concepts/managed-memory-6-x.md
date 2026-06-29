# Managed Memory on Devices with Compute Capability 6.x+

CUDA Managed Memory is fully supported and coherent on devices with compute capability 6.x or higher that do not have pageable memory access [CUDA_C_Programming_Guide:L21819-L21821].

## Programming Model

The programming model and performance tuning of unified memory on these devices is largely similar to the model described for devices with full CUDA Unified Memory support [CUDA_C_Programming_Guide:L21819-L21821].

## Limitations

A notable exception to the full unified memory model is that system allocators cannot be used to allocate memory [CUDA_C_Programming_Guide:L21819-L21821]. Consequently, specific sub-sections related to system allocator usage do not apply to this configuration [CUDA_C_Programming_Guide:L21819-L21821].
