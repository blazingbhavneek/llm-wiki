
A hitRatio value below 1.0 can be used to manually control the amount of data diferent accessPolicyWindows from concurrent CUDA streams can cache in L2. For example, let the L2 set-aside cache size be 16KB; two concurrent kernels in two diferent CUDA streams, each with a 16KB accessPolicyWindow, and both with hitRatio value 1.0, might evict each others’ cache lines when competing for the shared L2 resource. However, if both accessPolicyWindows have a hitRatio value of 0.5, they will be less likely to evict their own or each others’ persisting cache lines.

## 6.2.3.3 L2 Access Properties

Three types of access properties are defined for diferent global memory data accesses:

1. cudaAccessPropertyStreaming: Memory accesses that occur with the streaming property are less likely to persist in the L2 cache because these accesses are preferentially evicted.

2. cudaAccessPropertyPersisting: Memory accesses that occur with the persisting property are more likely to persist in the L2 cache because these accesses are preferentially retained in the set-aside portion of L2 cache.

3. cudaAccessPropertyNormal: This access property forcibly resets previously applied persisting access property to a normal status. Memory accesses with the persisting property from previous CUDA kernels may be retained in L2 cache long after their intended use. This persistenceafter-use reduces the amount of L2 cache available to subsequent kernels that do not use the persisting property. Resetting an access property window with the cudaAccessPropertyNormal property removes the persisting (preferential retention) status of the prior access, as if the prior access had been without an access property.

## 6.2.3.4 L2 Persistence Example

The following example shows how to set-aside L2 cache for persistent accesses, use the set-aside L2 cache in CUDA kernels via CUDA Stream and then reset the L2 cache.

```txt
cudaStream_t stream;
cudaStreamCreate(&stream);
    // Create CUDA stream

cudaDeviceProp prop;
    // CUDA device properties variable
cudaGetDeviceProperties( &prop, device_id);
    // Query GPU properties
size_t size = min( int(prop.l2CacheSize * 0.75) , prop.persistingL2CacheMaxSize );
cudaDeviceSetLimit( cudaLimitPersistingL2CacheSize, size);
    // set-aside 3/4 of L2 cache for persisting accesses or the max allowed

size_t window_size = min(prop.accessPolicyMaxWindowSize, num_bytes);
    // Select minimum of user defined num_bytes and max window size.

cudaStreamAttrValue stream_attribute;
    // Stream level attributes data structure
stream_attribute.accessPolicyWindow.base_ptr = reinterpret_cast<void*>(data1);
    // Global Memory data pointer
stream_attribute.accessPolicyWindow.num_bytes = window_size;
    // Number of bytes for persistence access
stream_attribute.accessPolicyWindow.hitRatio = 0.6;
    // Hint for cache hit ratio
stream_attribute.accessPolicyWindow.hitProp = cudaAccessPropertyPersisting;
    // Persistence Property
stream_attribute.accessPolicyWindow.missProp = cudaAccessPropertyStreaming;
    // Type of access property on cache miss

cudaStreamSetAttribute(stream, cudaStreamAttributeAccessPolicyWindow, &stream_
attribute);   // Set the attributes to a CUDA Stream

for(int i = 0; i < 10; i++) {
```

(continues on next page)

```cpp
cuda_kernelA<<<grid_size,block_size,0,stream>>>(data1);
// This data1 is used by a kernel multiple times
}
// [data1 + num_bytes) benefits from L2 persistence
cuda_kernelB<<<grid_size,block_size,0,stream>>>(data1);
// A different kernel in the same stream can also benefit

// from the persistence of data1

stream_attribute.accessPolicyWindow.num_bytes = 0;
// Setting the window size to 0 disable it
cudaStreamSetAttribute(stream, cudaStreamAttributeAccessPolicyWindow, &stream_
attribute); // Overwrite the access policy attribute to a CUDA Stream
cudaCtxResetPersistingL2Cache();
// Remove any persistent lines in L2

cuda_kernelC<<<grid_size,block_size,0,stream>>>(data2);
// data2 can now benefit from full L2 in normal mode
```

## 6.2.3.5 Reset L2 Access to Normal

A persisting L2 cache line from a previous CUDA kernel may persist in L2 long after it has been used. Hence, a reset to normal for L2 cache is important for streaming or normal memory accesses to utilize the L2 cache with normal priority. There are three ways a persisting access can be reset to normal status.

1. Reset a previous persisting memory region with the access property, cudaAccessPropertyNormal.

2. Reset all persisting L2 cache lines to normal by calling cudaCtxResetPersistingL2Cache().

3. Eventually untouched lines are automatically reset to normal. Reliance on automatic reset is strongly discouraged because of the undetermined length of time required for automatic reset to occur.

## 6.2.3.6 Manage Utilization of L2 set-aside cache

Multiple CUDA kernels executing concurrently in diferent CUDA streams may have a diferent access policy window assigned to their streams. However, the L2 set-aside cache portion is shared among all these concurrent CUDA kernels. As a result, the net utilization of this set-aside cache portion is the sum of all the concurrent kernels’ individual use. The benefits of designating memory accesses as persisting diminish as the volume of persisting accesses exceeds the set-aside L2 cache capacity.

To manage utilization of the set-aside L2 cache portion, an application must consider the following:

Size of L2 set-aside cache.

CUDA kernels that may concurrently execute.

▶ The access policy window for all the CUDA kernels that may concurrently execute.

▶ When and how L2 reset is required to allow normal or streaming accesses to utilize the previously set-aside L2 cache with equal priority.

## 6.2.3.7 Query L2 cache Properties

Properties related to L2 cache are a part of cudaDeviceProp struct and can be queried using CUDA runtime API cudaGetDeviceProperties

CUDA Device Properties include:

l2CacheSize: The amount of available L2 cache on the GPU.

persistingL2CacheMaxSize: The maximum amount of L2 cache that can be set-aside for persisting memory accesses.

▶ accessPolicyMaxWindowSize: The maximum size of the access policy window.

## 6.2.3.8 Control L2 Cache Set-Aside Size for Persisting Memory Access

The L2 set-aside cache size for persisting memory accesses is queried using CUDA runtime API cudaDeviceGetLimit and set using CUDA runtime API cudaDeviceSetLimit as a cudaLimit. The maximum value for setting this limit is cudaDeviceProp::persistingL2CacheMaxSize.

```txt
enum cudaLimit {
    /* other fields not shown */
    cudaLimitPersistingL2CacheSize
};
```
