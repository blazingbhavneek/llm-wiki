# Resource Usage Statistics

Resource usage statistics allow developers to monitor the memory consumption of a CUDA memory pool. These features were introduced in CUDA 11.3 [CUDA_C_Programming_Guide:L15573-L15576].

## Pool Attributes

The following attributes are available for querying memory usage statistics from a `cudaMemoryPool_t` [CUDA_C_Programming_Guide:L15573-L15576]:

*   **`cudaMemPoolAttrReservedMemCurrent`**: Reports the current total physical GPU memory consumed by the pool [CUDA_C_Programming_Guide:L15577-L15578].
*   **`cudaMemPoolAttrUsedMemCurrent`**: Returns the total size of all memory allocated from the pool that is not available for reuse [CUDA_C_Programming_Guide:L15579-L15580].

## High-Watermark Attributes

The `*MemHigh` attributes serve as watermarks, recording the maximum value achieved by their corresponding `*MemCurrent` attributes since the last reset [CUDA_C_Programming_Guide:L15581-L15582]. The specific high-watermark attributes are:

*   `cudaMemPoolAttrReservedMemHigh`
*   `cudaMemPoolAttrUsedMemHigh`

## Resetting Statistics

High-watermark values can be reset to the current value using the `cudaMemPoolSetAttribute` API [CUDA_C_Programming_Guide:L15581-L15582]. To reset the watermarks, the attribute is set with a value of 0, which causes the watermark to take on the current value [CUDA_C_Programming_Guide:L15599-L15605].

### Example Implementation

The following C code demonstrates how to retrieve usage statistics in bulk and reset the watermarks [CUDA_C_Programming_Guide:L15584-L15605]:

```c
// sample helper functions for getting the usage statistics in bulk
struct usageStatistics {
    cuuint64_t reserved;
    cuuint64_t reservedHigh;
    cuuint64_t used;
    cuuint64_t usedHigh;
};

void getUsageStatistics(cudaMemoryPool_t memPool, struct usageStatistics *statistics)
{
    cudaMemPoolGetAttribute(memPool, cudaMemPoolAttrReservedMemCurrent, statistics->reserved);
    cudaMemPoolGetAttribute(memPool, cudaMemPoolAttrReservedMemHigh, statistics->reservedHigh);
    cudaMemPoolGetAttribute(memPool, cudaMemPoolAttrUsedMemCurrent, statistics->used);
    cudaMemPoolGetAttribute(memPool, cudaMemPoolAttrUsedMemHigh, statistics->usedHigh);
}

// resetting the watermarks will make them take on the current value.
void resetStatistics(cudaMemoryPool_t memPool)
{
    cuuint64_t value = 0;
    cudaMemPoolSetAttribute(memPool, cudaMemPoolAttrReservedMemHigh, &value);
    cudaMemPoolSetAttribute(memPool, cudaMemPoolAttrUsedMemHigh, &value);
}
```
