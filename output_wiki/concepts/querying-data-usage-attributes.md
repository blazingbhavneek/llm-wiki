# Querying Data Usage Attributes on Managed Memory

A program can query memory range attributes assigned through `cudaMemAdvise` or `cudaMemPrefetchAsync` on CUDA Managed Memory by using the `cudaMemRangeGetAttribute` API [CUDA_C_Programming_Guide:L21368-L21408]. This allows applications to inspect the current state and history of managed memory ranges to make informed decisions about data staging and optimization [CUDA_C_Programming_Guide:L21368-L21408].

## API Signature

The primary function for querying a single attribute is:

```c
cudaMemRangeGetAttribute(void *data,
                    size_t dataSize,
                    enum cudaMemRangeAttribute attribute,
                    const void *devPtr,
                    size_t count);
```

This function queries an attribute of the memory range starting at `devPtr` with a size of `count` bytes [CUDA_C_Programming_Guide:L21368-L21408]. The memory range must refer to managed memory allocated via `cudaMallocManaged` or declared via `__managed__` variables [CUDA_C_Programming_Guide:L21368-L21408].

Additionally, multiple attributes can be queried simultaneously using the corresponding `cudaMemRangeGetAttributes` function [CUDA_C_Programming_Guide:L21368-L21408].

## Available Attributes

The following attributes can be queried to determine the properties and history of a managed memory range [CUDA_C_Programming_Guide:L21368-L21408]:

### cudaMemRangeAttributeReadMostly

Returns `1` if the entire memory range has the `cudaMemAdviseSetReadMostly` attribute set, or `0` otherwise [CUDA_C_Programming_Guide:L21368-L21408].

### cudaMemRangeAttributePreferredLocation

Returns a GPU device ID or `cudaCpuDeviceId` if the entire memory range has the corresponding processor as its preferred location; otherwise, it returns `cudaInvalidDeviceId` [CUDA_C_Programming_Guide:L21368-L21408].

An application can use this query API to make decisions about staging data through the CPU or GPU depending on the preferred location attribute of the managed pointer [CUDA_C_Programming_Guide:L21368-L21408]. Note that the actual location of the memory range at the time of the query may be different from the preferred location [CUDA_C_Programming_Guide:L21368-L21408].

### cudaMemRangeAttributeAccessedBy

Returns the list of devices that have the `cudaMemAdviseSetAccessedBy` attribute set for that memory range [CUDA_C_Programming_Guide:L21368-L21408].

### cudaMemRangeAttributeLastPrefetchLocation

Returns the last location to which the memory range was prefetched explicitly using `cudaMemPrefetchAsync` [CUDA_C_Programming_Guide:L21368-L21408].

Note that this simply returns the last location that the application requested to prefetch the memory range to. It gives no indication as to whether the prefetch operation to that location has completed or even begun [CUDA_C_Programming_Guide:L21368-L21408].

### Location Type and ID Attributes

For more granular control, specific attributes provide both the type of location and the specific ID (device ordinal or NUMA node) [CUDA_C_Programming_Guide:L21368-L21408]:

#### cudaMemRangeAttributePreferredLocationType

Returns the location type of the preferred location [CUDA_C_Programming_Guide:L21368-L21408]:

*   `cudaMemLocationTypeDevice`: If all pages in the memory range have the same GPU as their preferred location [CUDA_C_Programming_Guide:L21368-L21408].
*   `cudaMemLocationTypeHost`: If all pages in the memory range have the CPU as their preferred location [CUDA_C_Programming_Guide:L21368-L21408].
*   `cudaMemLocationTypeHostNuma`: If all the pages in the memory range have the same host NUMA node ID as their preferred location [CUDA_C_Programming_Guide:L21368-L21408].
*   `cudaMemLocationTypeInvalid`: If either all the pages don’t have the same preferred location or some of the pages don’t have a preferred location at all [CUDA_C_Programming_Guide:L21368-L21408].

#### cudaMemRangeAttributePreferredLocationId

If `cudaMemRangeAttributePreferredLocationType` returns `cudaMemLocationTypeDevice`, this attribute returns a valid device ordinal. If it returns `cudaMemLocationTypeHostNuma`, it returns a valid host NUMA node ID. If it returns any other location type, the ID should be ignored [CUDA_C_Programming_Guide:L21368-L21408].

#### cudaMemRangeAttributeLastPrefetchLocationType

Returns the last location type to which all pages in the memory range were prefetched explicitly via `cudaMemPrefetchAsync` [CUDA_C_Programming_Guide:L21368-L21408]:

*   `cudaMemLocationTypeDevice`: If all pages in the memory range were prefetched to the same GPU [CUDA_C_Programming_Guide:L21368-L21408].
*   `cudaMemLocationTypeHost`: If all pages in the memory range were prefetched to the CPU [CUDA_C_Programming_Guide:L21368-L21408].
*   `cudaMemLocationTypeHostNuma`: If all the pages in the memory range were prefetched to the same host NUMA node ID [CUDA_C_Programming_Guide:L21368-L21408].
*   `cudaMemLocationTypeInvalid`: If either all the pages were not prefetched to the same location or some of the pages were never prefetched at all [CUDA_C_Programming_Guide:L21368-L21408].

#### cudaMemRangeAttributeLastPrefetchLocationId

If `cudaMemRangeAttributeLastPrefetchLocationType` returns `cudaMemLocationTypeDevice`, this attribute returns a valid device ordinal. If it returns `cudaMemLocationTypeHostNuma`, it returns a valid host NUMA node ID. If it returns any other location type, the ID should be ignored [CUDA_C_Programming_Guide:L21368-L21408].

## See Also

*   [Unified memory on devices with full CUDA Unified Memory support](concept/unified-memory-full-support)
