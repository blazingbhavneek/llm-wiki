# Compressible Memory

Details on allocating and querying compressible memory using CU_MEM_ALLOCATION_COMP_GENERIC and CU_DEVICE_ATTRIBUTE_GENERIC_COMPRESSION_SUPPORTED.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L15101-L15128

Citation: [CUDA_C_Programming_Guide:L15101-L15128]

````text
## 14.3.2.1 Compressible Memory

Compressible memory can be used to accelerate accesses to data with unstructured sparsity and other compressible data patterns. Compression can save DRAM bandwidth, L2 read bandwidth and L2 capacity depending on the data being operated on. Applications that want to allocate compressible memory on devices that support Compute Data Compression can do so by setting CUmemAllocationProp::allocFlags::compressionType to CU\_MEM\_ALLOCATION\_COMP\_GENERIC. Users must query if device supports Compute Data Compression by using CU\_DEVICE\_ATTRIBUTE\_GENERIC\_COMPRESSION\_SUPPORTED. The following code snippet illustrates querying compressible memory support cuDeviceGetAttribute.

```txt
int compressionSupported = 0;
cuDeviceGetAttribute(&compressionSupported, CU_DEVICE_ATTRIBUTE_GENERIC_COMPRESSION_
→SUPPORTED, device);
```

On devices that support Compute Data Compression, users must opt in at allocation time as shown below:

```javascript
prop.allocFlags.compressionType = CU_MEM_ALLOCATION_COMP_GENERIC;
```

Due to various reasons such as limited HW resources, the allocation may not have compression attributes, the user is expected to query back the properties of the allocated memory using cuMemGetAllocationPropertiesFromHandle and check for compression attribute.

```javascript
CUmemAllocationProp allocationProp = {};
cuMemGetAllocationPropertiesFromHandle(&allocationProp, allocationHandle);

if (allocationProp.allocFlags.compressionType == CU_MEM_ALLOCATION_COMP_GENERIC)
{
    // Obtained compressible memory allocation
}
```
````
