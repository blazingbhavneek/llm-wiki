# Querying Data Usage Attributes

Describes cudaMemRangeGetAttribute and cudaMemRangeGetAttributes APIs used to query attributes set via cudaMemAdvise or cudaMemPrefetchAsync. Lists queryable attributes like ReadMostly, PreferredLocation, AccessedBy, and LastPrefetchLocation.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21368-L21407

Citation: [CUDA_C_Programming_Guide:L21368-L21407]

````text
## 24.1.2.8.4 Querying Data Usage Attributes on Managed Memory

A program can query memory range attributes assigned through cudaMemAdvise or cudaMem-PrefetchAsync on CUDA Managed Memory by using the following API:

```txt
cudaMemRangeGetAttribute(void *data,
                    size_t dataSize,
                    enum cudaMemRangeAttribute attribute,
                    const void *devPtr,
                    size_t count);
```

This function queries an attribute of the memory range starting at devPtr with a size of count bytes. The memory range must refer to managed memory allocated via cudaMallocManaged or declared via \_\_managed\_\_ variables. It is possible to query the following attributes:

▶ cudaMemRangeAttributeReadMostly: the result returned will be 1 if the entire memory range has the cudaMemAdviseSetReadMostly attribute set, or 0 otherwise.

cudaMemRangeAttributePreferredLocation: the result returned will be a GPU device id or cudaCpuDeviceId if the entire memory range has the corresponding processor as preferred location, otherwise cudaInvalidDeviceId will be returned. An application can use this query API to make decision about staging data through CPU or GPU depending on the preferred location attribute of the managed pointer. Note that the actual location of the memory range at the time of the query may be diferent from the preferred location.

▶ cudaMemRangeAttributeAccessedBy: will return the list of devices that have that advise set for that memory range.

▶ cudaMemRangeAttributeLastPrefetchLocation: will return the last location to which the memory range was prefetched explicitly using cudaMemPrefetchAsync. Note that this simply returns the last location that the application requested to prefetch the memory range to. It gives no indication as to whether the prefetch operation to that location has completed or even begun.

## ▶ cudaMemRangeAttributePreferredLocationType:

will return the location type of the preferred location which will be cudaMemLocationType-Device if all pages in the memory range have the same GPU as their preferred location, or will be cudaMemLocationTypeHost if all pages in the memory range have the CPU as their preferred location, or it will be cudaMemLocationTypeHostNuma if all the pages in the memory range have the same host NUMA node ID as their preferred location or it will be cudaMemLocationTypeInvalid if either all the pages don’t have the same preferred location or some of the pages don’t have a preferred location at all.

## ▶ cudaMemRangeAttributePreferredLocationId:

If the cudaMemRangeAttributePreferredLocationType query for the same address range returns cudaMemLocationTypeDevice, it will be a valid device ordinal or if it returns cudaMemLocationTypeHostNuma, it will be a valid host NUMA node ID or if it returns any other location type, the id should be ignored.

## ▶ cudaMemRangeAttributeLastPrefetchLocationType:

will be the last location type to which all pages in the memory range were prefetched explicitly via cudaMemPrefetchAsync which will be cudaMemLocationTypeDevice if all pages in the memory range were prefetched to the same GPU, or will be cudaMemLocationType-Host if all pages in the memory range were prefetched to the CPU or it will be cudaMemLocationTypeHostNuma if all the pages in the memory range were prefetched to the same host NUMA node ID or it will be cudaMemLocationTypeInvalid if either all the pages were not prefetched to the same location or some of the pages were never prefetched at all.

## ▶ cudaMemRangeAttributeLastPrefetchLocationId:

If the cudaMemRangeAttributeLastPrefetchLocationType query for the same address range returns cudaMemLocationTypeDevice, it will be a valid device ordinal or if it returns cudaMemLocationTypeHostNuma, it will be a valid host NUMA node ID or if it returns any other location type, the id should be ignored.

Additionally, multiple attributes can be queried by using corresponding cudaMemRangeGetAttributes function.
````
