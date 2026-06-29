# Coherency and Concurrency (Pre-6.x)

On devices with compute capability lower than 6.0, simultaneous access to managed memory by the CPU and GPU is not possible. This restriction exists because hardware coherence cannot be guaranteed if the CPU accesses a Unified Memory allocation while a GPU kernel is active [CUDA_C_Programming_Guide:L21848-L21856].

## GPU Exclusive Access

To ensure coherency on pre-6.x GPU architectures, the Unified Memory programming model imposes constraints on data accesses when both the CPU and GPU are executing concurrently. Effectively, the GPU has exclusive access to all managed data while any kernel operation is executing, regardless of whether the specific kernel is actively using that data [CUDA_C_Programming_Guide:L21848-L21856].

### Constraints on Host Operations

When managed data is used with `cudaMemcpy*()` or `cudaMemset*()`, the system may choose to access the source or destination from the host or the device. This choice places constraints on concurrent CPU access to that data while the `cudaMemcpy*()` or `cudaMemset*()` operation is executing [CUDA_C_Programming_Guide:L21848-L21856].

### Segmentation Faults on Concurrent Access

It is not permitted for the CPU to access any managed allocations or variables while the GPU is active on devices where the `concurrentManagedAccess` property is set to 0. On these systems, concurrent CPU/GPU accesses—even to different managed memory allocations—will cause a segmentation fault because the memory page is considered inaccessible to the CPU [CUDA_C_Programming_Guide:L21848-L21856].
