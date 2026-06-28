
## 24.1.2.4 Diference between Unified Memory and Mapped Memory

The main diference between Unified Memory and Mapped Memory is that CUDA Mapped Memory does not guarantee that all kinds of memory accesses (for example atomics) are supported on all systems, while Unified Memory does. The limited set of memory operations that are guaranteed to be portably supported by CUDA Mapped Memory is available on more systems than Unified Memory.

## 24.1.2.5 Pointer Attributes

CUDA Programs may check whether a pointer addresses a CUDA Managed Memory allocation by calling cudaPointerGetAttributes() and testing whether the pointer attribute value is cudaMemoryTypeManaged.

This API returns cudaMemoryTypeHost for System-Allocated Memory that has been registered with cudaHostRegister() and cudaMemoryTypeUnregistered for System-Allocated Memory that CUDA is unaware of.

Pointer attributes do not state where the memory resides, they state how the memory was allocated or registered.

The following example shows how to detect the type of pointer at runtime:

```javascript
char const* kind(cudaPointerAttributes a, bool pma, bool cma) {
    switch(a.type) {
        case cudaMemoryTypeHost: return pma?
            "Unified: CUDA Host or Registered Memory" :
            "Not Unified: CUDA Host or Registered Memory";
        case cudaMemoryTypeDevice: return "Not Unified: CUDA Device Memory";
        case cudaMemoryTypeManaged: return cma?
            "Unified: CUDA Managed Memory" : "Not Unified: CUDA Managed Memory";
```

(continues on next page)

(continued from previous page)

```c
case cudaMemoryTypeUnregistered: return pma?
    "Unified: System-Allocated Memory" :
    "Not Unified: System-Allocated Memory";
default: return "unknown";
}
}

void check_pointer(int i, void* ptr) {
cudaPointerAttributes attr;
cudaPointerGetAttributes(&attr, ptr);
int pma = 0, cma = 0, device = 0;
cudaGetDevice(&device);
cudaDeviceGetAttribute(&pma, cudaDevAttrPageableMemoryAccess, device);
cudaDeviceGetAttribute(&cma, cudaDevAttrConcurrentManagedAccess, device);
printf("Pointer %d: memory is %s\n", i, kind(attr, pma, cma));
}

__managed__ int managed_var = 5;

int main() {
int* ptr[5];
ptr[0] = (int*)malloc(sizeof(int));
cudaMallocManaged(&ptr[1], sizeof(int));
cudaMallocHost(&ptr[2], sizeof(int));
cudaMalloc(&ptr[3], sizeof(int));
ptr[4] = &managed_var;

for (int i = 0; i < 5; ++i) check_pointer(i, ptr[i]);

cudaFree(ptr[3]);
cudaFreeHost(ptr[2]);
cudaFree(ptr[1]);
free(ptr[0]);
return 0;
}
```

## 24.1.2.6 Runtime detection of Unified Memory Support Level

The following example shows how to detect the Unified Memory support level at runtime:

```c
int main() {
    int d;
    cudaGetDevice(&d);

    int pma = 0;
    cudaDeviceGetAttribute(&pma, cudaDevAttrPageableMemoryAccess, d);
    printf("Full Unified Memory Support: %s\n", pma == 1? "YES" : "NO");

    int cma = 0;
    cudaDeviceGetAttribute(&cma, cudaDevAttrConcurrentManagedAccess, d);
    printf("CUDA Managed Memory with full support: %s\n", cma == 1? "YES" : "NO");

    return 0;
}
```

## 24.1.2.7 GPU Memory Oversubscription

Unified Memory enables applications to oversubscribe the memory of any individual processor: in other words they can allocate and share arrays larger than the memory capacity of any individual processor in the system, enabling among others out-of-core processing of datasets that do not fit within a single GPU, without adding significant complexity to the programming model.

## 24.1.2.8 Performance Hints

The following sections describes the available unified memory performance hints, which may be used on all Unified Memory, for example, CUDA Managed memory or, on systems with full CUDA Unified Memory support, also all System-Allocated Memory. These APIs are hints, that is, they do not impact the semantics of applications, only their peformance. That is, they can be added or removed anywhere on any application without impacting its results.

CUDA Unified Memory may not always have all the information necessary to make the best performance decisions related to unified memory. These performance hints enable the application to provide CUDA with more information.

Note that applications should only use these hints if they improve their performance.

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

## 24.1.2.8.2 Memory Discarding

The cudaMemDiscardBatchAsync API allows applications to inform the CUDA runtime that the contents of specified memory ranges are no longer useful. The Unified Memory driver performs automatic memory transfers due to fault-based migration or memory evictions to support device memory oversubscription. These automatic memory transfers can sometimes be redundant, which severely decreases performance. Marking an address range as ‘discard’ will inform the Unified Memory driver that the application has consumed the contents in the range and there is no need to migrate this data on prefetches or page evictions in order to make room for other allocations. Reading a discarded page without a subsequent write access or prefetch will yield an indeterminate value. Whereas any new writes after the discard operation is guaranteed to be seen by a subsequent read access. Concurrent accesses or prefetches to address ranges being discarded will result in undefined behavior.

```c
cudaError_t cudaMemDiscardBatchAsync(void **dptrs,
                               size_t *sizes,
                               size_t count,
                               unsigned long long flags,
                               cudaStream_t stream);
```

The function performs a batch of memory discards on address ranges specified in dptrs and sizes arrays. Both arrays must be of the same length as specified by count. Each memory range must refer to managed memory allocated via cudaMallocManaged or declared via \_\_managed\_\_ variables.

The cudaMemDiscardAndPrefetchBatchAsync API combines both discard and prefetch operations. Calling cudaMemDiscardAndPrefetchBatchAsync is semantically equivalent to calling cudaMemDiscardBatchAsync followed by cudaMemPrefetchBatchAsync, but is more optimal. This is useful when the application needs the memory to be on the target location but does not need the contents of the memory.

```csv
cudaError_t cudaMemDiscardAndPrefetchBatchAsync(void **dptrs,
size_t *sizes,
```

(continues on next page)

(continued from previous page)

```txt
size_t count,
struct cudaMemLocation *prefetchLocs,
size_t *prefetchLocIdxs,
size_t numPrefetchLocs,
unsigned long long flags,
cudaStream_t stream);
```

The prefetchLocs array specifies the destinations for prefetching, while prefetchLocIdxs indicates which operations each prefetch location applies to. For example, if a batch has 10 operations and the first 6 should be prefetched to one location while the remaining 4 to another, then numPrefetchLocs would be 2, prefetchLocIdxs would be {0, 6}, and prefetchLocs would contain the two destination locations.

## Important considerations:

▶ Reading from a discarded range without a subsequent write or prefetch will return an indeterminate value

▶ The discard operation can be undone by writing to the range or prefetching it via cudaMem-PrefetchAsync

▶ Any reads, writes, or prefetches that occur simultaneously with the discard operation result in undefined behavior

▶ All devices must have a non-zero value for cudaDevAttrConcurrentManagedAccess

## 24.1.2.8.3 Data Usage Hints

When multiple processors simultaneously access the same data, cudaMemAdvise may be used to hint how the data at [devPtr, devPtr + count) will be accessed:

```txt
cudaError_t cudaMemAdvise(const void *devPtr,
                    size_t count,
                    enum cudaMemoryAdvise advice,
                    struct cudaMemLocation location);
```

Where advice may take the following values:

▶ cudaMemAdviseSetReadMostly: This implies that the data is mostly going to be read from and only occasionally written to. In general, it allows trading of read bandwidth for write bandwidth on this region. Example:

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
```

(continues on next page)

(continued from previous page)

```cpp
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

cudaMemAdviseSetPreferredLocation: In general, any memory may be migrated at any time to any location, for example, when a given processor is running out of physical memory. This hint tells the system that migrating this memory region away from its preferred location is undesired, by setting the preferred location for the data to be the physical memory belonging to device. Passing in a value of cudaMemLocationTypeHost for location.type sets the preferred location as CPU memory. Other hints, like cudaMemPrefetchAsync, may override this hint, leading the memory to be migrated away from its preferred location.

▶ cudaMemAdviseSetAccessedBy: In some systems, it may be beneficial for performance to establish a mapping into memory before accessing the data from a given processor. This hint tells the system that the data will be frequently accessed by location.id when location.type is cudaMemLocationTypeDevice, enabling the system to assume that creating these mappings pays of. This hint does not imply where the data should reside, but it can be combined with cudaMemAdviseSetPreferredLocation to specify that.

Each advice can be also unset by using one of the following values: cudaMemAdviseUnsetRead-Mostly, cudaMemAdviseUnsetPreferredLocation and cudaMemAdviseUnsetAccessedBy.

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

# 24.2. Unified memory on devices with full CUDA Unified Memory support
