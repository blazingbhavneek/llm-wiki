# Allocating Multicast Objects

Multicast objects are created using the `cuMulticastCreate` function. The creation process requires configuring a `CUmemAllocationProp` structure to specify the target number of devices and the desired handle types for sharing the allocation.

## Configuration

When initializing the `CUmemAllocationProp` structure, the following fields are critical:

*   **numDevices**: Specifies the number of devices that will participate in the multicast group.
*   **handleTypes**: Defines the type of handle used to share the allocation. Common options include:
    *   `CU_MEM_HANDLE_TYPE_FABRIC`: Used for multi-node or fabric-based communication.
    *   `CU_MEM_HANDLE_TYPE_POSIX_FILE_DESCRIPTOR`: Used for single-node sharing.

## Granularity and Size Alignment

Before creating the multicast object, the allocation size must satisfy specific granularity requirements. This is determined by calling `cuMulticastGetGranularity` with the allocation properties and the `CU_MEM_ALLOC_GRANULARITY_MINIMUM` flag.

The requested size must be rounded up to the nearest multiple of the returned granularity value to ensure valid allocation.

## Creation

Once the properties are set and the size is padded to meet granularity requirements, `cuMulticastCreate` is called to generate the `CUmemGenericAllocationHandle`. It is important to note that at this stage, the multicast object does not yet have any devices attached or physical memory associated with it; it serves as a container for the allocation properties.

### Example Implementation

The following C++ code demonstrates the standard procedure for allocating a multicast object:

```cpp
CUmemGenericAllocationHandle createMCHandle(int numDevices, size_t size) {
    CUmemAllocationProp mcProp = {};
    mcProp.numDevices = numDevices;
    mcProp.handleTypes = CU_MEM_HANDLE_TYPE_FABRIC; // or on single node CU_MEM_HANDLE_TYPE_POSIX_FILE_DESCRIPTOR

    size_t granularity = 0;
    cuMulticastGetGranularity(&granularity, &mcProp, CU_MEM_ALLOC_GRANULARITY_MINIMUM);

    // Ensure size matches granularity requirements for the allocation
    size_t padded_size = ROUND_UP(size, granularity);

    mcProp.size = padded_size;

    // Create Multicast Object this has no devices and no physical memory associated yet
    CUmemGenericAllocationHandle mcHandle;
    cuMulticastCreate(&mcHandle, &mcProp);

    return mcHandle;
}
```

[CUDA_C_Programming_Guide:L15290-L15315]
