# L2 Cache Management

L2 Cache Management is a feature introduced in CUDA 11.0 for devices with compute capability 8.0 and above, allowing applications to influence the persistence of data in the L2 cache [CUDA_C_Programming_Guide:L1411-L1415]. By distinguishing between "persisting" accesses (repeatedly accessed data) and "streaming" accesses (single-use data), applications can optimize for higher bandwidth and lower latency global memory accesses [CUDA_C_Programming_Guide:L1411-L1415].

## L2 Cache Set-Aside

A portion of the L2 cache can be reserved specifically for persisting data accesses [CUDA_C_Programming_Guide:L1417-L1419]. This set-aside portion is prioritized for persisting accesses, while normal or streaming accesses can only utilize it when it is unused by persisting accesses [CUDA_C_Programming_Guide:L1419-L1421].

### Configuration

The size of the L2 cache set-aside is configured using the `cudaDeviceSetLimit` API with the `cudaLimitPersistingL2CacheSize` limit [CUDA_C_Programming_Guide:L1423-L1425]. The size must be within the device's maximum allowed limit, defined by `cudaDeviceProp::persistingL2CacheMaxSize` [CUDA_C_Programming_Guide:L1423-L1425].

```cpp
cudaDeviceProp prop;
cudaGetDeviceProperties(&prop, device_id);
size_t size = min(int(prop.l2CacheSize * 0.75), prop.persistingL2CacheMaxSize);
cudaDeviceSetLimit(cudaLimitPersistingL2CacheSize, size);
```

### Constraints

*   **Multi-Instance GPU (MIG):** The L2 cache set-aside functionality is disabled when the GPU is configured in MIG mode [CUDA_C_Programming_Guide:L1427-L1428].
*   **Multi-Process Service (MPS):** When using MPS, the set-aside size cannot be changed at runtime via `cudaDeviceSetLimit`. Instead, it must be specified at startup of the MPS server using the environment variable `CUDA_DEVICE_DEFAULT_PERSISTING_L2_CACHE_PERCENTAGE_LIMIT` [CUDA_C_Programming_Guide:L1430-L1432].

## Access Policy Windows

An access policy window defines a contiguous region of global memory and assigns a persistence property to memory accesses within that region [CUDA_C_Programming_Guide:L1435-L1437]. This can be applied to CUDA Streams or CUDA Graph Kernel Nodes [CUDA_C_Programming_Guide:L1437-L1439].

### Stream-Level Configuration

```cpp
cudaStreamAttrValue stream_attribute;
stream_attribute.accessPolicyWindow.base_ptr = reinterpret_cast<void*>(ptr);
stream_attribute.accessPolicyWindow.num_bytes = num_bytes;
stream_attribute.accessPolicyWindow.hitRatio = 0.6;
stream_attribute.accessPolicyWindow.hitProp = cudaAccessPropertyPersisting;
stream_attribute.accessPolicyWindow.missProp = cudaAccessPropertyStreaming;
cudaStreamSetAttribute(stream, cudaStreamAttributeAccessPolicyWindow, &stream_attribute);
```

### Graph Kernel Node Configuration

```cpp
cudaKernelNodeAttrValue node_attribute;
node_attribute.accessPolicyWindow.base_ptr = reinterpret_cast<void*>(ptr);
node_attribute.accessPolicyWindow.num_bytes = num_bytes;
node_attribute.accessPolicyWindow.hitRatio = 0.6;
node_attribute.accessPolicyWindow.hitProp = cudaAccessPropertyPersisting;
node_attribute.accessPolicyWindow.missProp = cudaAccessPropertyStreaming;
cudaGraphKernelNodeSetAttribute(node, cudaKernelNodeAttributeAccessPolicyWindow, &node_attribute);
```

### Parameters

*   **`base_ptr`**: Pointer to the global memory region [CUDA_C_Programming_Guide:L1443-L1444].
*   **`num_bytes`**: Size of the region, which must be less than `cudaDeviceProp::accessPolicyMaxWindowSize` [CUDA_C_Programming_Guide:L1445-L1446].
*   **`hitRatio`**: A hint specifying the fraction of accesses in the window that should receive the `hitProp` property [CUDA_C_Programming_Guide:L1453-L1455]. The specific classification of accesses is random based on this probability [CUDA_C_Programming_Guide:L1457-L1459].
*   **`hitProp`**: The access property applied when a cache hit occurs (e.g., `cudaAccessPropertyPersisting`) [CUDA_C_Programming_Guide:L1448-L1449].
*   **`missProp`**: The access property applied when a cache miss occurs (e.g., `cudaAccessPropertyStreaming`) [CUDA_C_Programming_Guide:L1450-L1451].

### Hit Ratio and Cache Thrashing

The `hitRatio` parameter can be used to manage cache utilization and avoid thrashing [CUDA_C_Programming_Guide:L1463-L1465]. For example, if the set-aside cache is 16KB and the window is 32KB:
*   A `hitRatio` of 1.0 attempts to cache the entire 32KB, evicting older lines to keep the most recent 16KB [CUDA_C_Programming_Guide:L1467-L1471].
*   A `hitRatio` of 0.5 designates only 16KB of the window as persisting, reducing the likelihood of evicting cache lines from other concurrent streams [CUDA_C_Programming_Guide:L1473-L1477].

## Access Properties

Three types of access properties define how memory accesses interact with the L2 cache [CUDA_C_Programming_Guide:L1481-L1483]:

1.  **`cudaAccessPropertyStreaming`**: Prefers eviction from the L2 cache [CUDA_C_Programming_Guide:L1485-L1487].
2.  **`cudaAccessPropertyPersisting`**: Prefers retention in the set-aside L2 cache portion [CUDA_C_Programming_Guide:L1489-L1491].
3.  **`cudaAccessPropertyNormal`**: Resets previously applied persisting properties to a normal status, removing preferential retention [CUDA_C_Programming_Guide:L1493-L1497].

## Resetting L2 Cache

Persisting cache lines may remain in L2 long after their intended use, reducing availability for subsequent kernels [CUDA_C_Programming_Guide:L1499-L1501]. There are three methods to reset L2 access to normal [CUDA_C_Programming_Guide:L1503-L1505]:

1.  **Explicit Reset via Property**: Set the access property of a previous persisting memory region to `cudaAccessPropertyNormal` [CUDA_C_Programming_Guide:L1507-L1509].
2.  **Explicit Reset via API**: Call `cudaCtxResetPersistingL2Cache()` to reset all persisting L2 cache lines to normal [CUDA_C_Programming_Guide:L1511-L1513].
3.  **Automatic Reset**: Untouched lines are eventually reset automatically, but reliance on this is discouraged due to undetermined timing [CUDA_C_Programming_Guide:L1515-L1517].

## Querying Properties

L2 cache properties are queried via the `cudaDeviceProp` structure using `cudaGetDeviceProperties` [CUDA_C_Programming_Guide:L1521-L1523]. Key properties include:

*   **`l2CacheSize`**: Total available L2 cache size [CUDA_C_Programming_Guide:L1525-L1527].
*   **`persistingL2CacheMaxSize`**: Maximum size that can be set-aside for persisting accesses [CUDA_C_Programming_Guide:L1529-L1531].
*   **`accessPolicyMaxWindowSize`**: Maximum size of an access policy window [CUDA_C_Programming_Guide:L1533-L1535].

## Concurrent Utilization

The L2 set-aside cache is shared among all concurrent CUDA kernels across different streams [CUDA_C_Programming_Guide:L1539-L1543]. The net utilization is the sum of all concurrent kernels' individual use [CUDA_C_Programming_Guide:L1543-L1545]. Applications must manage the size of the set-aside cache, the number of concurrent kernels, and their respective access policy windows to optimize performance [CUDA_C_Programming_Guide:L1547-L1551].

## Example Workflow

The following example demonstrates setting aside L2 cache, applying an access policy window to a stream, and resetting the cache [CUDA_C_Programming_Guide:L1555-L1563]:

```cpp
cudaStream_t stream;
cudaStreamCreate(&stream);

cudaDeviceProp prop;
cudaGetDeviceProperties(&prop, device_id);
size_t size = min(int(prop.l2CacheSize * 0.75), prop.persistingL2CacheMaxSize);
cudaDeviceSetLimit(cudaLimitPersistingL2CacheSize, size);

size_t window_size = min(prop.accessPolicyMaxWindowSize, num_bytes);
cudaStreamAttrValue stream_attribute;
stream_attribute.accessPolicyWindow.base_ptr = reinterpret_cast<void*>(data1);
stream_attribute.accessPolicyWindow.num_bytes = window_size;
stream_attribute.accessPolicyWindow.hitRatio = 0.6;
stream_attribute.accessPolicyWindow.hitProp = cudaAccessPropertyPersisting;
stream_attribute.accessPolicyWindow.missProp = cudaAccessPropertyStreaming;
cudaStreamSetAttribute(stream, cudaStreamAttributeAccessPolicyWindow, &stream_attribute);

// Kernels using data1 benefit from persistence
cuda_kernelA<<<grid_size, block_size, 0, stream>>>(data1);
cuda_kernelB<<<grid_size, block_size, 0, stream>>>(data1);

// Disable window and reset cache
cudaStreamAttrValue reset_attribute;
reset_attribute.accessPolicyWindow.num_bytes = 0;
cudaStreamSetAttribute(stream, cudaStreamAttributeAccessPolicyWindow, &reset_attribute);
cudaCtxResetPersistingL2Cache();

// data2 uses full L2 in normal mode
cuda_kernelC<<<grid_size, block_size, 0, stream>>>(data2);
```
