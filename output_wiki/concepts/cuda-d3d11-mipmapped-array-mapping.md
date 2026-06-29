# CUDA Direct3D 11 Mipmapped Array Mapping

A CUDA mipmapped array can be mapped onto an imported memory object by specifying matching offset, dimensions, format, and number of mip levels as defined in the corresponding Direct3D 11 API [CUDA_C_Programming_Guide:L5479-L5479]. If the mipmapped array is intended to be bound as a render target in Direct3D 12, the `cudaArrayColorAttachment` flag must be set [CUDA_C_Programming_Guide:L5479-L5479]. All mapped mipmapped arrays must be freed using `cudaFreeMipmappedArray()` [CUDA_C_Programming_Guide:L5479-L5479].

## Mapping Process

The mapping is performed using `cudaExternalMemoryGetMappedMipmappedArray()`. The following function demonstrates how to configure the `cudaExternalMemoryMipmappedArrayDesc` structure and retrieve the mipmapped array handle:

```cpp
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

## Parameter Conversion

When mapping mipmapped arrays onto imported memory objects, Direct3D 11 parameters must be converted to their corresponding CUDA equivalents [CUDA_C_Programming_Guide:L5479-L5479].

### Channel Format Conversion

The `cudaChannelFormatDesc` structure is populated based on the `DXGI_FORMAT` using the `getCudaChannelFormatDescForDxgiFormat` function. This function maps DXGI formats to CUDA channel formats, specifying the bit depth and kind (unsigned, signed, or float) for each channel (x, y, z, w) [CUDA_C_Programming_Guide:L5481-L5616].

Key mappings include:
- `DXGI_FORMAT_R8_UINT` maps to an 8-bit unsigned channel [CUDA_C_Programming_Guide:L5481-L5616].
- `DXGI_FORMAT_R32_FLOAT` maps to a 32-bit float channel [CUDA_C_Programming_Guide:L5481-L5616].
- `DXGI_FORMAT_R8G8B8A8_UINT` maps to four 8-bit unsigned channels [CUDA_C_Programming_Guide:L5481-L5616].

### Extent Conversion

The `cudaExtent` structure is derived from Direct3D 11 dimensions and service view dimension using `getCudaExtentForD3D11Extent`. The mapping handles various texture types:
- `D3D11_SRV_DIMENSION_TEXTURE1D`: Width is set; height and depth are 0 [CUDA_C_Programming_Guide:L5481-L5616].
- `D3D11_SRV_DIMENSION_TEXTURE2D`: Width and height are set; depth is 0 [CUDA_C_Programming_Guide:L5481-L5616].
- `D3D11_SRV_DIMENSION_TEXTURE3D`: Width, height, and depth (from `depthOrArraySize`) are set [CUDA_C_Programming_Guide:L5481-L5616].
- `D3D11_SRV_DIMENSION_TEXTURE2DARRAY`: Width, height, and depth (array size) are set [CUDA_C_Programming_Guide:L5481-L5616].

### Flag Conversion

CUDA array flags are determined based on the Direct3D 11 service view dimension, bind flags, and surface load/store requirements via `getCudaMipmappedArrayFlagsForD3D12Resource` [CUDA_C_Programming_Guide:L5481-L5616].

- **Cubemap Support**: `D3D11_SRV_DIMENSION_TEXTURECUBE` sets `cudaArrayCubemap` [CUDA_C_Programming_Guide:L5481-L5616].
- **Layered Support**: `D3D11_SRV_DIMENSION_TEXTURECUBEARRAY`, `D3D11_SRV_DIMENSION_TEXTURE1DARRAY`, and `D3D11_SRV_DIMENSION_TEXTURE2DARRAY` set `cudaArrayLayered` [CUDA_C_Programming_Guide:L5481-L5616].
- **Render Target**: If the Direct3D 11 resource has the `D3D11_BIND_RENDER_TARGET` flag, `cudaArrayColorAttachment` is set [CUDA_C_Programming_Guide:L5481-L5616].
- **Surface Load/Store**: If allowed, `cudaArraySurfaceLoadStore` is set [CUDA_C_Programming_Guide:L5481-L5616].

## Memory Management

After use, the mapped mipmapped array must be explicitly freed using `cudaFreeMipmappedArray()` to release the associated CUDA resources [CUDA_C_Programming_Guide:L5479-L5479].
