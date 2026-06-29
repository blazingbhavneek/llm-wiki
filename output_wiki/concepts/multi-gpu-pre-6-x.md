# Multi-GPU Managed Memory (Pre-6.x)

On systems with devices of compute capabilities lower than 6.0, managed allocations are automatically visible to all GPUs in a system via the peer-to-peer capabilities of the GPUs [CUDA_C_Programming_Guide:L21837-L21847].

## Behavior and Bandwidth

Managed memory allocations behave similar to unmanaged memory allocated using `cudaMalloc()`: the current active device is the home for the physical allocation, but other GPUs in the system will access the memory at reduced bandwidth over the PCIe bus [CUDA_C_Programming_Guide:L21837-L21847].

## Linux Behavior

On Linux, the managed memory is allocated in GPU memory as long as all GPUs that are actively being used by a program have the peer-to-peer support [CUDA_C_Programming_Guide:L21837-L21847]. If at any time the application starts using a GPU that doesn’t have peer-to-peer support with any of the other GPUs that have managed allocations on them, then the driver will migrate all managed allocations to system memory [CUDA_C_Programming_Guide:L21837-L21847]. In this case, all GPUs experience PCIe bandwidth restrictions [CUDA_C_Programming_Guide:L21837-L21847].

## Windows Behavior

On Windows, if peer mappings are not available (for example, between GPUs of different architectures), then the system will automatically fall back to using zero-copy memory, regardless of whether both GPUs are actually used by a program [CUDA_C_Programming_Guide:L21837-L21847]. If only one GPU is actually going to be used, it is necessary to set the `CUDA_VISIBLE_DEVICES` environment variable before launching the program [CUDA_C_Programming_Guide:L21837-L21847]. This constrains which GPUs are visible and allows managed memory to be allocated in GPU memory [CUDA_C_Programming_Guide:L21837-L21847].

Alternatively, on Windows users can also set `CUDA_MANAGED_FORCE_DEVICE_ALLOC` to a non-zero value to force the driver to always use device memory for physical storage [CUDA_C_Programming_Guide:L21837-L21847]. When this environment variable is set to a non-zero value, all devices used in that process that support managed memory have to be peer-to-peer compatible with each other [CUDA_C_Programming_Guide:L21837-L21847]. The error `::cudaErrorInvalidDevice` will be returned if a device that supports managed memory is used and it is not peer-to-peer compatible with any of the other managed memory supporting devices that were previously used in that process, even if `::cudaDeviceReset` has been called on those devices [CUDA_C_Programming_Guide:L21837-L21847].

Note that starting from CUDA 8.0, `CUDA_MANAGED_FORCE_DEVICE_ALLOC` has no effect on Linux operating systems [CUDA_C_Programming_Guide:L21837-L21847].

## Related Documentation

These environment variables are described in CUDA Environment Variables [CUDA_C_Programming_Guide:L21837-L21847].
