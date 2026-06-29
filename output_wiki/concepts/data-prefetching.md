# Data Prefetching in Unified Memory

The `cudaMemPrefetchAsync` API is an asynchronous, stream-ordered function that migrates data to reside closer to a specified processor. This allows data to be accessed while it is being prefetched, optimizing performance in systems with unified memory or multiple devices.

## API Signature

```cpp
cudaError_t cudaMemPrefetchAsync(const void *devPtr,
                                 size_t count,
                                 struct cudaMemLocation location,
                                 unsigned int flags,
                                 cudaStream_t stream);
```

## Behavior and Synchronization

The migration behavior is governed by the CUDA stream order:

1.  **Start Condition**: The migration does not begin until all prior operations in the specified stream have completed.
2.  **Completion Condition**: The migration completes before any subsequent operation in the stream is executed.
3.  **Concurrent Access**: Data may be accessed by the application while it is being prefetched.

The function targets a memory region defined by `[devPtr, devPtr + count)`. The destination is determined by the `location` argument:
*   If `location.type` is `cudaMemLocationTypeDevice`, the data is migrated to the device specified by `location.id`.
*   If `location.type` is `cudaMemLocationTypeHost`, the data is migrated to the CPU.

## Usage Patterns

### System Allocator
When using standard system memory (allocated via `malloc`), explicit prefetching is required to move data between the host and device before kernel execution or host access.

```cpp
void test_prefetch_sam(cudaStream_t s) {
    char *data = (char*)malloc(N);
    init_data(data, N);                                // execute on CPU
    
    cudaMemLocation location = {.type = cudaMemLocationTypeDevice, .id = myGpuId};
    cudaMemPrefetchAsync(data, N, location, s, 0 /* flags */); // prefetch to GPU
    
    mykernel<<<(N + TPB - 1) / TPB, TPB, 0, s>>>(data, N);      // execute on GPU
    
    location = {.type = cudaMemLocationTypeHost};
    cudaMemPrefetchAsync(data, N, location, s, 0 /* flags */); // prefetch to CPU
    
    cudaStreamSynchronize(s);
    use_data(data, N);
    free(data);
}
```

### Managed Memory
When using managed memory (allocated via `cudaMallocManaged`), the same prefetching pattern applies to ensure data locality before kernel launches or host accesses.

```cpp
void test_prefetch_managed(cudaStream_t s) {
    char *data;
    cudaMallocManaged(&data, N);
    init_data(data, N);                                // execute on CPU
    
    cudaMemLocation location = {.type = cudaMemLocationTypeDevice, .id = myGpuId};
    cudaMemPrefetchAsync(data, N, location, s, 0 /* flags */);  // prefetch to GPU
    
    mykernel<<<(N + TPB - 1) / TPB, TPB, 0, s>>>(data, N);      // execute on GPU
    
    location = {.type = cudaMemLocationTypeHost};
    cudaMemPrefetchAsync(data, N, location, s, 0 /* flags */);  // prefetch to CPU
    
    cudaStreamSynchronize(s);
    use_data(data, N);
    cudaFree(data);
}
```

## References
- [CUDA_C_Programming_Guide:L21202-L21258]
