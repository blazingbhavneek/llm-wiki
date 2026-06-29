# Device Accessibility for Multi-GPU Support

In CUDA's virtual memory management, memory pool allocation accessibility is distinct from standard peer access controls. While traditional peer access is managed via `cudaDeviceEnablePeerAccess` or `cuCtxEnablePeerAccess`, memory pool accessibility is controlled through the `cudaMemPoolSetAccess` API [CUDA_C_Programming_Guide:L15670-L15704].

## Default Behavior and Constraints

By default, allocations from a memory pool are accessible only from the device where the allocations are located [CUDA_C_Programming_Guide:L15670-L15704]. This default access cannot be revoked [CUDA_C_Programming_Guide:L15670-L15704].

To enable access from other devices, the accessing device must be peer-capable with the device associated with the memory pool [CUDA_C_Programming_Guide:L15670-L15704]. The peer capability should be verified using `cudaDeviceCanAccessPeer` before attempting to set access [CUDA_C_Programming_Guide:L15670-L15704]. If peer capability is not verified and the devices are not peer-capable, `cudaMemPoolSetAccess` may fail with `cudaErrorInvalidDevice` [CUDA_C_Programming_Guide:L15670-L15704].

> **Note:** If no allocations have been made from the pool, `cudaMemPoolSetAccess` may succeed even if the devices are not peer-capable; however, the next allocation from the pool will subsequently fail [CUDA_C_Programming_Guide:L15670-L15704].

## Scope of Accessibility Settings

Accessibility settings applied via `cudaMemPoolSetAccess` affect all allocations from the memory pool, not just future ones [CUDA_C_Programming_Guide:L15670-L15704]. Similarly, the accessibility reported by `cudaMemPoolGetAccess` applies to all existing and future allocations from the pool [CUDA_C_Programming_Guide:L15670-L15704].

## Best Practices

It is recommended that accessibility settings for a memory pool on a given GPU not be changed frequently [CUDA_C_Programming_Guide:L15670-L15704]. Once a pool is made accessible from a specific GPU, it should remain accessible from that GPU for the lifetime of the pool [CUDA_C_Programming_Guide:L15670-L15704].

## Example Usage

The following code snippet demonstrates how to enable read-write access for a specific device to a memory pool, including peer capability verification:

```cpp
cudaError_t setAccessOnDevice(cudaMemPool_t memPool, int residentDevice,
        int accessingDevice) {
    cudaMemAccessDesc accessDesc = {};
    accessDesc.location.type = cudaMemLocationTypeDevice;
    accessDesc.location.id = accessingDevice;
    accessDesc.flags = cudaMemAccessFlagsProtReadWrite;

    int canAccess = 0;
    cudaError_t error = cudaDeviceCanAccessPeer(&canAccess, accessingDevice,
            residentDevice);
    if (error != cudaSuccess) {
        return error;
    } else if (canAccess == 0) {
        return cudaErrorPeerAccessUnsupported;
    }

    // Make the address accessible
    return cudaMemPoolSetAccess(memPool, &accessDesc, 1);
}
```

[CUDA_C_Programming_Guide:L15670-L15704]
