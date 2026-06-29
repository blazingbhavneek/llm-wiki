# Compressible Memory

Compressible memory is a feature designed to accelerate accesses to data with unstructured sparsity and other compressible data patterns. By leveraging Compute Data Compression, this memory type can save DRAM bandwidth, L2 read bandwidth, and L2 capacity, depending on the specific data being operated on [CUDA_C_Programming_Guide:L15101-L15128].

## Prerequisites and Support

Before allocating compressible memory, applications must verify that the target device supports Compute Data Compression. This is done by querying the device attribute `CU_DEVICE_ATTRIBUTE_GENERIC_COMPRESSION_SUPPORTED` using `cuDeviceGetAttribute` [CUDA_C_Programming_Guide:L15101-L15128].

```c
int compressionSupported = 0;
cuDeviceGetAttribute(&compressionSupported, CU_DEVICE_ATTRIBUTE_GENERIC_COMPRESSION_SUPPORTED, device);
```

## Allocation

To allocate compressible memory on a supported device, applications must opt in at allocation time by setting the `compressionType` field within `CUmemAllocationProp::allocFlags` to `CU_MEM_ALLOCATION_COMP_GENERIC` [CUDA_C_Programming_Guide:L15101-L15128].

```c
prop.allocFlags.compressionType = CU_MEM_ALLOCATION_COMP_GENERIC;
```

## Verification

Due to hardware resource limitations, an allocation request for compressible memory may not result in memory with compression attributes enabled. Therefore, applications are expected to query the properties of the allocated memory after allocation using `cuMemGetAllocationPropertiesFromHandle` and verify that the compression attribute is present [CUDA_C_Programming_Guide:L15101-L15128].

```c
CUmemAllocationProp allocationProp = {};
cuMemGetAllocationPropertiesFromHandle(&allocationProp, allocationHandle);

if (allocationProp.allocFlags.compressionType == CU_MEM_ALLOCATION_COMP_GENERIC)
{
    // Obtained compressible memory allocation
}
```
