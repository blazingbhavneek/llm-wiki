# EGM: Using CUDA Memory Pool

## Overview

Explicit Graph Memory (EGM) can be implemented by creating a CUDA memory pool on a specific node and granting access to peer devices. This approach allows for fine-grained control over memory allocation and accessibility across different devices in a multi-GPU system.

## Creating the Memory Pool

To define EGM, the user must create a memory pool on a node and explicitly configure the location type. The location type should be set to `cudaMemLocationTypeHostNuma`, with the `numaId` serving as the location identifier. This ensures the memory is allocated in the correct NUMA node.

The following code snippet demonstrates how to create a memory pool using `cudaMemPoolCreate`:

```cpp
cudaSetDevice(homeDevice);
cudaMemPoolProps props {};
props.allocType = cudaMemAllocationTypePinned;
props.location.type = cudaMemLocationTypeHostNuma;
props.location.id = numaId;
cudaMemPoolCreate(&memPool, &props);
```

## Granting Peer Access

For direct connect peer access, the existing peer access API `cudaMemPoolSetAccess` can be used to grant other devices access to the created memory pool. An example for an `accessingDevice` is shown below:

```cpp
cudaMemAccessDesc desc {};
desc.flags = cudaMemAccessFlagsProtReadWrite;
desc.location.type = cudaMemLocationTypeDevice;
desc.location.id = accessingDevice;
cudaMemPoolSetAccess(memPool, &desc, 1);
```

## Allocating Memory

Once the memory pool is created and access permissions are granted, the pool can be set as the default memory pool for the resident device. Memory allocations can then be performed using `cudaMallocAsync`:

```cpp
cudaDeviceSetMemPool(residentDevice, memPool);
cudaMallocAsync(&ptr, size, memPool, stream);
```

## Performance Considerations

EGM is mapped with 2MB pages. Users should be aware that this large page size may result in increased Translation Lookaside Buffer (TLB) misses when accessing very large allocations [CUDA_C_Programming_Guide:L22327-L22327].

## References

- [CUDA_C_Programming_Guide:L22297-L22297]
- [CUDA_C_Programming_Guide:L22299-L22299]
- [CUDA_C_Programming_Guide:L22301-L22308]
- [CUDA_C_Programming_Guide:L22310-L22310]
- [CUDA_C_Programming_Guide:L22312-L22318]
- [CUDA_C_Programming_Guide:L22320-L22320]
- [CUDA_C_Programming_Guide:L22322-L22325]
- [CUDA_C_Programming_Guide:L22327-L22327]
