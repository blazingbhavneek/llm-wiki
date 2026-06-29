# Data Usage Hints (cudaMemAdvise)

The `cudaMemAdvise` API allows applications to provide hints to the CUDA runtime about how data in a specific memory region will be accessed, particularly when multiple processors simultaneously access the same data. These hints influence memory migration, prefetching behavior, and mapping establishment to optimize performance.

## API Signature

The function signature for providing memory advice is:

```cpp
cudaError_t cudaMemAdvise(const void *devPtr,
                          size_t count,
                          enum cudaMemoryAdvise advice,
                          struct cudaMemLocation location);
```

Where:
- `devPtr`: Pointer to the start of the memory region.
- `count`: Size of the memory region in bytes.
- `advice`: The type of advice to provide (see below).
- `location`: The target location for the advice (e.g., specific device or host).

## Advice Values

### cudaMemAdviseSetReadMostly

This hint implies that the data is mostly going to be read from and only occasionally written to. In general, it allows trading of read bandwidth for write bandwidth on this region [CUDA_C_Programming_Guide:L21306-L21367].

**Example Usage:**

```cpp
void test_advise_managed(cudaStream_t stream) {
    char *dataPtr;
    size_t dataSize = 64 * TPB;  // 16 KiB
    // Allocate memory using cudaMallocManaged
    // (malloc may be used on systems with full CUDA Unified memory support)
    cudaMallocManaged(&dataPtr, dataSize);
    // Set the advice on the memory region
    cudaMemLocation loc = {.type = cudaMemLocationTypeDevice, .id = myGpuId};
    cudaMemAdvise(dataPtr, dataSize, cudaMemAdviseSetReadMostly, loc);
    int outerLoopIter = 0;
    while (outerLoopIter < maxOuterLoopIter) {
        // The data is written to in the outer loop on the CPU
        init_data(dataPtr, dataSize);
        // The data is made available to all GPUs by prefetching.
        // Prefetching here causes read duplication of data instead
        // of data migration
        cudaMemLocation location;
        location.type = cudaMemLocationTypeDevice;
        for (int device = 0; device < maxDevices; device++) {
            location.id = device;
            cudaMemcpyPrefetchAsync(dataPtr, dataSize, location, 0 /* flags */, stream);
        }
        // The kernel only reads this data in the inner loop
        int innerLoopIter = 0;
        while (innerLoopIter < maxInnerLoopIter) {
            mykernel<<<32, TPB, 0, stream>>>(const char *)dataPtr, dataSize);
            innerLoopIter++;
        }
        outerLoopIter++;
    }
    cudaFree(dataPtr);
}
```

### cudaMemAdviseSetPreferredLocation

In general, any memory may be migrated at any time to any location, for example, when a given processor is running out of physical memory. This hint tells the system that migrating this memory region away from its preferred location is undesired, by setting the preferred location for the data to be the physical memory belonging to the specified device [CUDA_C_Programming_Guide:L21306-L21367].

- Passing in a value of `cudaMemLocationTypeHost` for `location.type` sets the preferred location as CPU memory.
- Other hints, like `cudaMemPrefetchAsync`, may override this hint, leading the memory to be migrated away from its preferred location.

### cudaMemAdviseSetAccessedBy

In some systems, it may be beneficial for performance to establish a mapping into memory before accessing the data from a given processor. This hint tells the system that the data will be frequently accessed by `location.id` when `location.type` is `cudaMemLocationTypeDevice`, enabling the system to assume that creating these mappings pays off [CUDA_C_Programming_Guide:L21306-L21367].

- This hint does not imply where the data should reside.
- It can be combined with `cudaMemAdviseSetPreferredLocation` to specify both residency and access patterns.

## Unsetting Hints

Each advice can be unset by using the corresponding unset value:
- `cudaMemAdviseUnsetReadMostly`
- `cudaMemAdviseUnsetPreferredLocation`
- `cudaMemAdviseUnsetAccessedBy`

## Related Terms

- `cudaMemAdvise`
- `cudaMemAdviseSetReadMostly`
- `cudaMemAdviseSetPreferredLocation`
- `cudaMemAdviseSetAccessedBy`
