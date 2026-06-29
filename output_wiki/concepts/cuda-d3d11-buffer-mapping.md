# CUDA Direct3D 11 Buffer Mapping

CUDA allows device pointers to be mapped onto imported memory objects, such as those created via Direct3D 11. This process enables interoperability between CUDA and Direct3D 11 resources.

## Mapping Procedure

To map a device pointer to an imported memory object, use the `cudaExternalMemoryGetMappedBuffer` function. The mapping requires an `cudaExternalMemory_t` handle, along with specific offset and size parameters.

### Key Constraints

1.  **Offset and Size**: The offset and size of the mapping must exactly match those specified when creating the mapping using the corresponding Direct3D 11 API [CUDA_C_Programming_Guide:L5457-L5457].
2.  **Memory Management**: All mapped device pointers returned by this process must be freed using `cudaFree()` [CUDA_C_Programming_Guide:L5457-L5457].

### Example Implementation

The following code snippet demonstrates how to map a buffer onto external memory:

```cpp
void * mapBufferOntoExternalMemory(cudaExternalMemory_t extMem, unsigned long long offset, unsigned long long size) {
    void *ptr = NULL;
    cudaExternalMemoryBufferDesc desc = {};

    memset(&desc, 0, sizeof(desc));

    desc.offset = offset;
    desc.size = size;

    cudaExternalMemoryGetMappedBuffer(&ptr, extMem, &desc);

    // Note: 'ptr' must eventually be freed using cudaFree()
    return ptr;
}
```

In this example:
- `extMem` is the imported external memory handle.
- `offset` and `size` define the region of the memory to map.
- `desc` is a `cudaExternalMemoryBufferDesc` structure initialized with the offset and size.
- `cudaExternalMemoryGetMappedBuffer` populates `ptr` with the device pointer to the mapped memory.

## Best Practices

- Ensure that the `offset` and `size` parameters in `cudaExternalMemoryBufferDesc` are consistent with the Direct3D 11 resource creation parameters to avoid undefined behavior or mapping failures.
- Always call `cudaFree()` on the returned pointer to release the mapped memory resource [CUDA_C_Programming_Guide:L5459-L5475].
