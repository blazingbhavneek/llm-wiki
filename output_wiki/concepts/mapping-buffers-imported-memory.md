# Mapping Buffers onto Imported Memory Objects

A device pointer can be mapped onto an imported memory object, such as an `NvSciBufObj`, allowing CUDA kernels to access external memory resources. This mapping is achieved using the `cudaExternalMemoryGetMappedBuffer` function.

## Procedure

To map a buffer onto external memory:

1.  Define a `cudaExternalMemoryBufferDesc` structure to specify the mapping parameters.
2.  Initialize the structure and set the `offset` and `size` fields. These values should correspond to the attributes of the allocated `NvSciBufObj` [CUDA_C_Programming_Guide:L5934-L5954].
3.  Call `cudaExternalMemoryGetMappedBuffer` to obtain the device pointer [CUDA_C_Programming_Guide:L5934-L5954].

### Example Implementation

The following code snippet demonstrates how to map an external memory object to a device pointer:

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

## Memory Management

All mapped device pointers obtained via `cudaExternalMemoryGetMappedBuffer` must be freed using `cudaFree()` [CUDA_C_Programming_Guide:L5934-L5954]. Failure to free these pointers may result in resource leaks. The external memory object itself (`cudaExternalMemory_t`) is managed separately and does not require `cudaFree()`; it is typically destroyed using `cudaExternalMemoryDestroy()` after all associated buffers have been unmapped or freed.

## Related Functions

*   `cudaExternalMemoryGetMappedBuffer`: Maps a buffer onto an imported memory object.
*   `cudaFree`: Frees device memory, including mapped buffers from external memory.
*   `cudaExternalMemoryDestroy`: Destroys an external memory object.

## See Also

*   [Importing CUDA Memory](concept/importing-cuda-memory)
*   [Exporting CUDA Memory](concept/exporting-cuda-memory)
*   [NvSciBuf](concept/nvscibuf)

## References

*   CUDA C++ Programming Guide, Section 6.2.16.5.2 [CUDA_C_Programming_Guide:L5934-L5954]
