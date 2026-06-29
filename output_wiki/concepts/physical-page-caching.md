# Physical Page Caching Behavior

By default, the CUDA allocator attempts to minimize the amount of physical memory owned by a memory pool [CUDA_C_Programming_Guide:L15529-L15572]. To reduce the overhead of operating system calls required to allocate and free physical memory, applications should configure a specific memory footprint for each pool [CUDA_C_Programming_Guide:L15529-L15572].

## Release Threshold

The behavior of memory release is controlled by the `cudaMemPoolAttrReleaseThreshold` attribute [CUDA_C_Programming_Guide:L15529-L15572]. This attribute defines the amount of memory, in bytes, that a pool retains before attempting to release memory back to the operating system [CUDA_C_Programming_Guide:L15529-L15572].

- **Automatic Release**: When the memory held by the pool exceeds the release threshold, the allocator attempts to return memory to the OS on the next call to stream, event, or device synchronization [CUDA_C_Programming_Guide:L15529-L15572].
- **Disabling Auto-Shrink**: Setting the release threshold to `UINT64_MAX` prevents the driver from attempting to shrink the pool automatically after every synchronization [CUDA_C_Programming_Guide:L15529-L15572].

```cpp
uint64_t setVal = UINT64_MAX;
cudaMemPoolSetAttribute(memPool, cudaMemPoolAttrReleaseThreshold, &setVal);
```

## Explicit Trimming

Applications that set a high release threshold to effectively disable automatic memory pool shrinking may wish to explicitly control the pool's footprint [CUDA_C_Programming_Guide:L15529-L15572]. The `cudaMemPoolTrimTo` function allows an application to shrink the memory pool's footprint [CUDA_C_Programming_Guide:L15529-L15572].

When trimming, the `minBytesToKeep` parameter allows the application to retain a specific amount of memory it expects to need in a subsequent phase of execution [CUDA_C_Programming_Guide:L15529-L15572].

### Example Workflow

1.  **Disable Auto-Shrink**: Set the release threshold to `UINT64_MAX` [CUDA_C_Programming_Guide:L15529-L15572].
2.  **High Memory Phase**: Perform allocations and kernel executions [CUDA_C_Programming_Guide:L15529-L15572].
3.  **Synchronize**: Ensure allocations are no longer in use by synchronizing the stream [CUDA_C_Programming_Guide:L15529-L15572].
4.  **Trim**: Call `cudaMemPoolTrimTo` to release unused physical memory [CUDA_C_Programming_Guide:L15529-L15572].

```cpp
uint64_t setVal = UINT64_MAX;
cudaMemPoolSetAttribute(memPool, cudaMemPoolAttrReleaseThreshold, &setVal);

// Application phase needing a lot of memory from the stream ordered allocator
for (i=0; i<10; i++) {
    for (j=0; j<10; j++) {
        cudaMallocAsync(&ptrs[j], size[j], stream);
    }
    kernel<<<..., stream>>>(ptrs, ...);
    for (j=0; j<10; j++) {
        cudaFreeAsync(ptrs[j], stream);
    }
}

// Process does not need as much memory for the next phase.
// Synchronize so that the trim operation will know that the allocations are no
// longer in use.
cudaStreamSynchronize(stream);

// Release unused physical memory back to the OS
cudaMemPoolTrimTo(memPool, 0);
```

After trimming, the physical memory released by the operation becomes available for use by other processes or allocation mechanisms [CUDA_C_Programming_Guide:L15529-L15572].
