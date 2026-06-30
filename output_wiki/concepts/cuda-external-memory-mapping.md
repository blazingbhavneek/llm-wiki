# Mapping Buffers onto Imported Memory Objects

Covers mapping device pointers and mipmapped arrays onto imported NvSciBuf memory objects using `cudaExternalMemoryGetMappedBuffer` and `cudaExternalMemoryGetMappedMipmappedArray`. Includes code examples for setting offsets, sizes, formats, and extents, and notes that mapped resources must be freed with `cudaFree()` or `cudaFreeMipmappedArray()`.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L5934-L5982

Citation: [CUDA_C_Programming_Guide:L5934-L5982]

````text
## 6.2.16.5.2 Mapping Bufers onto Imported Memory Objects

A device pointer can be mapped onto an imported memory object as shown below. The ofset and size of the mapping can be filled as per the attributes of the allocated NvSciBufObj. All mapped device pointers must be freed using cudaFree().

```txt
void * mapBufferOntoExternalMemory(cudaExternalMemory_t extMem, unsigned long long
offset, unsigned long long size) {
    void *ptr = NULL;
    cudaExternalMemoryBufferDesc desc = {}

    memset(&desc, 0, sizeof(desc));

    desc.offset = offset;
    desc.size = size;

    cudaExternalMemoryGetMappedBuffer(&ptr, extMem, &desc);

    // Note: 'ptr' must eventually be freed using cudaFree()
    return ptr;
}
```

## 6.2.16.5.3 Mapping Mipmapped Arrays onto Imported Memory Objects

A CUDA mipmapped array can be mapped onto an imported memory object as shown below. The ofset, dimensions and format can be filled as per the attributes of the allocated NvSciBufObj. All mapped mipmapped arrays must be freed using cudaFreeMipmappedArray(). The following code sample shows how to convert NvSciBuf attributes into the corresponding CUDA parameters when mapping mipmapped arrays onto imported memory objects.

Note: The number of mip levels must be 1.

```txt
cudaMipmappedArray_t mapMipmappedArrayOntoExternalMemory(cudaExternalMemory_t extMem,
unsigned long long offset, cudaChannelFormatDesc *formatDesc, cudaExtent *extent,
unsigned int flags, unsigned int numLevels) {
    cudaMipmappedArray_t mipmap = NULL;
    cudaExternalMemoryMipmappedArrayDesc desc = {}

    memset(&desc, 0, sizeof(desc));

    desc.offset = offset;
    desc.formatDesc = *formatDesc;
    desc.extent = *extent;
    desc.flags = flags;
    desc.numLevels = numLevels;

    // Note: 'mipmap' must eventually be freed using cudaFreeMipmappedArray()
    cudaExternalMemoryGetMappedMipmappedArray(&mipmap, extMem, &desc);

    return mipmap;
}
```
````
