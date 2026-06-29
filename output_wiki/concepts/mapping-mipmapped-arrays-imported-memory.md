# Mapping Mipmapped Arrays onto Imported Memory Objects

A CUDA mipmapped array can be mapped onto an imported memory object. The offset, dimensions, and format of the array are filled according to the attributes of the allocated `NvSciBufObj` [CUDA_C_Programming_Guide:L5956-L5982].

## API Usage

The mapping is performed using the `cudaExternalMemoryGetMappedMipmappedArray` function. The parameters for the mapping, including offset, format, extent, flags, and number of levels, are specified via a `cudaExternalMemoryMipmappedArrayDesc` structure [CUDA_C_Programming_Guide:L5956-L5982].

### Example Implementation

The following code sample demonstrates how to convert NvSciBuf attributes into the corresponding CUDA parameters when mapping mipmapped arrays onto imported memory objects [CUDA_C_Programming_Guide:L5956-L5982]:

```c
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

## Constraints and Cleanup

- **Mip Levels**: The number of mip levels must be 1 [CUDA_C_Programming_Guide:L5956-L5982].
- **Memory Management**: All mapped mipmapped arrays must be freed using `cudaFreeMipmappedArray()` [CUDA_C_Programming_Guide:L5956-L5982].
