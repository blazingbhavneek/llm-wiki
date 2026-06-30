# Multi-GPU Managed Memory on Pre-6.x

Details managed memory visibility across GPUs via peer-to-peer, Linux driver migration behavior, Windows zero-copy fallback, and the CUDA_MANAGED_FORCE_DEVICE_ALLOC environment variable.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21837-L21847

Citation: [CUDA_C_Programming_Guide:L21837-L21847]

````text

## 24.3.2.3 Multi-GPU

On systems with devices of compute capabilities lower than 6.0 managed allocations are automatically visible to all GPUs in a system via the peer-to-peer capabilities of the GPUs. Managed memory allocations behave similar to unmanaged memory allocated using cudaMalloc(): the current active device is the home for the physical allocation but other GPUs in the system will access the memory at reduced bandwidth over the PCIe bus.

On Linux the managed memory is allocated in GPU memory as long as all GPUs that are actively being used by a program have the peer-to-peer support. If at any time the application starts using a GPU that doesn’t have peer-to-peer support with any of the other GPUs that have managed allocations on them, then the driver will migrate all managed allocations to system memory. In this case, all GPUs experience PCIe bandwidth restrictions.

On Windows, if peer mappings are not available (for example, between GPUs of diferent architectures), then the system will automatically fall back to using zero-copy memory, regardless of whether both GPUs are actually used by a program. If only one GPU is actually going to be used, it is necessary to set the CUDA\_VISIBLE\_DEVICES environment variable before launching the program. This constrains which GPUs are visible and allows managed memory to be allocated in GPU memory.

Alternatively, on Windows users can also set CUDA\_MANAGED\_FORCE\_DEVICE\_ALLOC to a non-zero value to force the driver to always use device memory for physical storage. When this environment variable is set to a non-zero value, all devices used in that process that support managed memory have to be peer-to-peer compatible with each other. The error ::cudaErrorInvalidDevice will be returned if a device that supports managed memory is used and it is not peer-to-peer compatible with any of the other managed memory supporting devices that were previously used in that process, even if ::cudaDeviceReset has been called on those devices. These environment variables are described in CUDA Environment Variables. Note that starting from CUDA 8.0 CUDA\_MANAGED\_FORCE\_DEVICE\_ALLOC has no efect on Linux operating systems.
````
