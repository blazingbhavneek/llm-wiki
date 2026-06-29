# Controlling Access Rights

The Virtual Memory Management APIs in CUDA enable applications to explicitly protect virtual address (VA) ranges using access control mechanisms. This allows for fine-grained management of memory accessibility across different devices in a system.

## Mechanism

Mapping an allocation to a region of the address space using `cuMemMap` does not automatically make the address accessible to devices. If a CUDA kernel attempts to access an unmapped or unprotected address, it will result in a program crash. To make an address accessible, users must explicitly define access control using the `cuMemSetAccess` function. This function allows or restricts access for specific devices to a mapped address range.

### Example Usage

The following code snippet illustrates how to make a specific device able to read and write to a mapped memory range:

```cpp
void setAccessOnDevice(int device, CUdeviceptr ptr, size_t size) {
    CUmemAccessDesc accessDesc = {};
    accessDesc.location.type = CU_MEM_LOCATION_TYPE_DEVICE;
    accessDesc.location.id = device;
    accessDesc.flags = CU_MEM_ACCESS_FLAGS_PROT_READWRITE;

    // Make the address accessible
    cuMemSetAccess(ptr, size, &accessDesc, 1);
}
```

## Comparison with Peer Access

The access control mechanism provided by Virtual Memory Management offers an alternative to the traditional `cudaEnablePeerAccess` approach:

*   **`cudaEnablePeerAccess`**: This function forces all prior and future `cudaMalloc`'d allocations to be mapped to the target peer device. While convenient, it requires the user to manage the mapping state of every allocation globally and can have performance implications for applications concerned with fine-grained control.
*   **Virtual Memory Management**: This approach allows users to be explicit about which specific allocations they wish to share with other peer devices. It enables peer mappings at the allocation granularity with minimal overhead, avoiding the need to track global mapping states for every device in the system.

## References

The `vectorAddMMAP` sample application serves as an example for using the Virtual Memory Management APIs to control access rights.

[doc_id=CUDA_C_Programming_Guide:L15211-L15230]
