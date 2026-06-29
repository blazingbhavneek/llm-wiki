# Mapping Buffers onto Imported D3D12 Memory Objects

A device pointer can be mapped onto an imported memory object, such as one created via Direct3D 12, to allow CUDA kernels to access the data. This process involves creating a buffer descriptor and calling `cudaExternalMemoryGetMappedBuffer`.

## Prerequisites and Constraints

When mapping a buffer onto imported memory, the following constraints apply:

*   **Offset and Size**: The offset and size of the mapping must match exactly those specified when creating the mapping using the corresponding Direct3D 12 API [CUDA_C_Programming_Guide:L5094-L5115].
*   **Memory Management**: All mapped device pointers obtained through this mechanism must be freed using `cudaFree()` [CUDA_C_Programming_Guide:L5094-L5115].

## Implementation Example

The following C++ function demonstrates how to map a buffer onto an external memory object:

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
1.  A `cudaExternalMemoryBufferDesc` structure is initialized to zero.
2.  The `offset` and `size` fields are set according to the imported memory region.
3.  `cudaExternalMemoryGetMappedBuffer` is called to retrieve the device pointer `ptr`.
4.  The caller is responsible for freeing `ptr` using `cudaFree()` when it is no longer needed [CUDA_C_Programming_Guide:L5094-L5115].
