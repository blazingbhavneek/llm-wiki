# cudaMemPoolReuseAllowInternalDependencies

## Overview

The `cudaMemPoolReuseAllowInternalDependencies` policy is a configuration option for CUDA memory pools that enables the driver to handle allocation failures by reusing existing memory through dependency insertion. This mechanism is particularly useful when the driver fails to allocate and map additional physical memory from the operating system.

## Behavior

When physical memory allocation fails, the driver checks for memory whose availability depends on the progress of another stream. If such memory is found, the driver performs the following actions:

1.  **Inserts Dependencies**: The driver inserts the required dependency into the allocating stream. This ensures that the memory is not reused until the work in the original stream that would allow access to that allocation has completed.
2.  **Reuses Memory**: The driver reuses the identified memory for the new allocation request.

This behavior is effectively equivalent to performing a `cudaStreamWaitEvent` in the allocating stream to synchronize with the completion of work in the original stream.

## Example Usage

The following code snippet illustrates the behavior when `cudaMemPoolReuseAllowInternalDependencies` is enabled:

```cpp
cudaMallocAsync(&ptr, size, originalStream);
kernel<<<..., originalStream>>>(ptr, ...);
cudaFreeAsync(ptr, originalStream);

// When cudaMemPoolReuseAllowInternalDependencies is enabled
// and the driver fails to allocate more physical memory, the driver may
// effectively perform a cudaStreamWaitEvent in the allocating stream
// to make sure that future work in 'otherStream' happens after the work
// in the original stream that would be allowed to access the original allocation.
cudaMallocAsync(&ptr2, size, otherStream);
```

In this example, if the driver cannot allocate new physical memory for `ptr2` in `otherStream`, it may reuse the memory previously allocated for `ptr` (which was freed in `originalStream`). To ensure correctness, the driver inserts a dependency so that `otherStream` waits for the completion of the work in `originalStream` that used `ptr`.

## References

- [CUDA_C_Programming_Guide:L15648-L15664]
