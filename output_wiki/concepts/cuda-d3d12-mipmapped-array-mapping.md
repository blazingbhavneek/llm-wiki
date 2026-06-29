# Mapping Mipmapped Arrays onto Imported D3D12 Memory Objects

A CUDA mipmapped array can be mapped onto an imported memory object using the CUDA Interoperability API. This process allows CUDA kernels to access and manipulate resources created in Direct3D 12. The offset, dimensions, format, and number of mip levels must match those specified when creating the mapping using the corresponding Direct3D 12 API [CUDA_C_Programming_Guide:L5116-L5256].

## Mapping Process

To map a mipmapped array, you must provide an external memory handle, an offset, a channel format description, an extent, flags, and the number of mip levels. The function `cudaExternalMemoryGetMappedMipmappedArray` is used to create the mapping [CUDA_C_Programming_Guide:L5116-L5256].

### Key Requirements

*   **Parameter Matching**: The offset, dimensions, format, and number of mip levels must match the specifications used in the Direct3D 12 API [CUDA_C_Programming_Guide:L5116-L5256].
*   **Render Target Flag**: If the mipmapped array can be bound as a render target in Direct3D 12, the flag `cudaArrayColorAttachment` must be set in the CUDA array flags [CUDA_C_Programming_Guide:L5116-L5256].
*   **Memory Management**: All mapped mipmapped arrays must be freed using `cudaFreeMipmappedArray()` [CUDA_C_Programming_Guide:L5116-L5256].

## Helper Functions for D3D12 to CUDA Conversion

The following helper functions demonstrate how to convert Direct3D 12 parameters into corresponding CUDA parameters when mapping mipmapped arrays onto imported memory objects [CUDA_C_Programming_Guide:L5116-L5256].

### 1. Mapping the Mipmapped Array

The `mapMipmappedArrayOntoExternalMemory` function encapsulates the creation of the CUDA mipmapped array from an external memory object [CUDA_C_Programming_Guide:L5116-L5256].

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

### 2. Converting DXGI Format to CUDA Channel Format

The `getCudaChannelFormatDescForDxgiFormat` function maps DXGI formats to CUDA channel format descriptions [CUDA_C_Programming_Guide:L5116-L5256].

```c
cudaChannelFormatDesc getCudaChannelFormatDescForDxgiFormat(DXGI_FORMAT dxgiFormat)
{
    cudaChannelFormatDesc d;

    memset(&d, 0, sizeof(d));

    switch (dxgiFormat) {
        case DXGI_FORMAT_R8_UINT:            d.x = 8; d.y = 0; d.z = 0; d.w = 0; d.f = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R8_SINT:            d.x = 8; d.y = 0; d.z = 0; d.w = 0; d.f = cudaChannelFormatKindSigned; break;
        case DXGI_FORMAT_R8G8_UINT:            d.x = 8; d.y = 8; d.z = 0; d.w = 0; d.f = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R8G8_SINT:            d.x = 8; d.y = 8; d.z = 0; d.w = 0; d.f = cudaChannelFormatKindSigned; break;
        case DXGI_FORMAT_R8G8B8A8_UINT:     d.x = 8; d.y = 8; d.z = 8; d.w = 8; d.f = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R8G8B8A8_SINT:     d.x = 8; d.y = 8; d.z = 8; d.w = 8; d.f = cudaChannelFormatKindSigned; break;
        case DXGI_FORMAT_R16_UINT:           d.x = 16; d.y = 0; d.z = 0; d.w = 0; d.f = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R16_SINT:           d.x = 16; d.y = 0; d.z = 0; d.w = 0; d.f = cudaChannelFormatKindSigned; break;
        case DXGI_FORMAT_R16G16_UINT:     d.x = 16; d.y = 16; d.z = 0; d.w = 0; d.f = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R16G16_SINT:     d.x = 16; d.y = 16; d.z = 0; d.w = 0; d.f = cudaChannelFormatKindSigned; break;
        case DXGI_FORMAT_R16G16B16A16_UINT:   d.x = 16; d.y = 16; d.z = 16; d.w = 16; d.f = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R16G16B16A16_SINT:   d.x = 16; d.y = 16; d.z = 16; d.w = 16; d.f = cudaChannelFormatKindSigned; break;
        case DXGI_FORMAT_R32_UINT:          d.x = 32; d.y = 0; d.z = 0; d.w = 0; d.f = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R32_SINT:          d.x = 32; d.y = 0; d.z = 0; d.w = 0; d.f = cudaChannelFormatKindSigned; break;
        case DXGI_FORMAT_R32_FLOAT:          d.x = 32; d.y = 0; d.z = 0; d.w = 0; d.f = cudaChannelFormatKindFloat; break;
        case DXGI_FORMAT_R32G32_UINT:        d.x = 32; d.y = 32; d.z = 0;   d.w = 0;   d.f = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R32G32_SINT:        d.x = 32; d.y = 32; d.z = 0;   d.w = 0;   d.f = cudaChannelFormatKindSigned;     break;
        case DXGI_FORMAT_R32G32_FLOAT:        d.x = 32; d.y = 32; d.z = 0;   d.w = 0;   d.f = cudaChannelFormatKindFloat;     break;
        case DXGI_FORMAT_R32G32B32A32_UINT:   d.x = 32; d.y = 32; d.z = 32; d.w = 32; d.f = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R32G32B32A32_SINT:   d.x = 32; d.y = 32; d.z = 32; d.w = 32; d.f = cudaChannelFormatKindSigned;     break;
        case DXGI_FORMAT_R32G32B32A32_FLOAT: d.x = 32; d.y = 32; d.z = 32; d.w = 32; d.f = cudaChannelFormatKindFloat;     break;
        default: assert(0);
    }
    return d;
}
```

### 3. Converting D3D12 Extent to CUDA Extent

The `getCudaExtentForD3D12Extent` function converts D3D12 resource dimensions (width, height, depth/array size) and service view dimension into a CUDA extent structure [CUDA_C_Programming_Guide:L5116-L5256].

```c
cudaExtent getCudaExtentForD3D12Extent(UINT64 width, UINT height, UINT16 depthOrArraySize, D3D12_SRV_DIMENSION d3d12SRVDimension) {
    cudaExtent e = { 0, 0, 0 };

    switch (d3d12SRVDimension) {
        case D3D12_SRV_DIMENSION_TEXTURE1D:            e.width = width; e.height = 0;      e.depth = 0;                  break;
        case D3D12_SRV_DIMENSION_TEXTURE2D:          e.width = width; e.height = height; e.depth = 0;                  break;
        case D3D12_SRV_DIMENSION_TEXTURE3D:          e.width = width; e.height = height; e.depth = depthOrArraySize; break;
        case D3D12_SRV_DIMENSION_TEXTURECUBE:       e.width = width; e.height = height; e.depth = depthOrArraySize; break;
        case D3D12_SRV_DIMENSION_TEXTURE1DARRAY:   e.width = width; e.height = 0;      e.depth = depthOrArraySize; break;
        case D3D12_SRV_DIMENSION_TEXTURE2DARRAY:   e.width = width; e.height = height; e.depth = depthOrArraySize; break;
        case D3D12_SRV_DIMENSION_TEXTURECUBEARRAY: e.width = width; e.height = height; e.depth = depthOrArraySize; break;
        default: assert(0);
    }

    return e;
}
```

### 4. Converting D3D12 Resource Flags to CUDA Array Flags

The `getCudaMipmappedArrayFlagsForD3D12Resource` function maps D3D12 resource dimensions and flags to CUDA array flags, including support for cubemaps, layered arrays, color attachments, and surface load/store operations [CUDA_C_Programming_Guide:L5116-L5256].

```c
unsigned int getCudaMipmappedArrayFlagsForD3D12Resource(D3D12_SRV_DIMENSION d3d12SRVDimension, D3D12_RESOURCE_FLAGS d3d12ResourceFlags, bool allowSurfaceLoadStore) {
    unsigned int flags = 0;

    switch (d3d12SRVDimension) {
        case D3D12_SRV_DIMENSION_TEXTURECUBE:       flags |= cudaArrayCubemap; break;
        case D3D12_SRV_DIMENSION_TEXTURECUBEARRAY: flags |= cudaArrayCubemap | cudaArrayLayered; break;
        case D3D12_SRV_DIMENSION_TEXTURE1DARRAY:   flags |= cudaArrayLayered; break;
        case D3D12_SRV_DIMENSION_TEXTURE2DARRAY: flags |= cudaArrayLayered; break;
        default: break;
    }

    if (d3d12ResourceFlags & D3D12_RESOURCE_FLAG_ALLOW_RENDER_TARGET) {
        flags |= cudaArrayColorAttachment;
    }
    if (allowSurfaceLoadStore) {
        flags |= cudaArraySurfaceLoadStore;
    }

    return flags;
}
```
