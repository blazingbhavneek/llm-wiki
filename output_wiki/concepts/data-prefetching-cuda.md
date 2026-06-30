# Data Prefetching in CUDA

Describes cudaMemPrefetchAsync, an asynchronous stream-ordered API to migrate data closer to a specified processor (GPU or CPU). Includes examples for System Allocator and Managed memory prefetching workflows.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21201-L21258

Citation: [CUDA_C_Programming_Guide:L21201-L21258]

````text
## 24.1.2.8.1 Data Prefetching

The cudaMemPrefetchAsync API is an asynchronous stream-ordered API that may migrate data to reside closer to the specified processor. The data may be accessed while it is being prefetched. The migration does not begin until all prior operations in the stream have completed, and completes before any subsequent operation in the stream.

```txt
cudaError_t cudaMemPrefetchAsync(const void *devPtr,
                               size_t count,
                               struct cudaMemLocation location,
                               unsigned int flags,
                               cudaStream_t stream);
```

A memory region containing [devPtr, devPtr + count) may be migrated to the destination device location.id if location.type is cudaMemLocationTypeDevice - or CPU if location.type is cudaMemLocationTypeHost - when the prefetch task is executed in the given stream. For details on flags, see the current CUDA Runtime API documentation.

Consider a simple code example below:

## System Allocator

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
```

(continues on next page)

```txt
use_data(data, N);
    free(data);
}
```

(continued from previous page)

## Managed

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
````
