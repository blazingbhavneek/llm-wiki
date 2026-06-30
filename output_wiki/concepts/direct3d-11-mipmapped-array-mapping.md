# Direct3D 11 Mipmapped Array Mapping

Maps CUDA mipmapped arrays onto imported memory objects, including DXGI format conversion and extent/mip-level flag handling.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L5501-L5616

Citation: [CUDA_C_Programming_Guide:L5501-L5616]

````text

cudaChannelFormatDesc getCudaChannelFormatDescForDxgiFormat(DXGI_FORMAT dxgiFormat)
{
    cudaChannelFormatDesc d;
```

(continued from previous page)

```txt
memset(&d, 0, sizeof(d));
switch (dxgiFormat) {
case DXGI_FORMAT_R8_UINT: d.x = 8; d.y = 0; d.z = 0; d.w = 0; d.f
cudaChannelFormatKindUnsigned; break;
case DXGI_FORMAT_R8_SINT: d.x = 8; d.y = 0; d.z = 0; d.w = 0; d.f
cudaChannelFormatKindSigned; break;
case DXGI_FORMAT_R8G8_UINT: d.x = 8; d.y = 8; d.z = 0; d.w = 0; d.f
cudaChannelFormatKindUnsigned; break;
case DXGI_FORMAT_R8G8_SINT: d.x = 8; d.y = 8; d.z = 0; d.w = 0; d.f
cudaChannelFormatKindSigned; break;
case DXGI_FORMAT_R8G8B8A8_UINT: d.x = 8; d.y = 8; d.z = 8; d.w = 8; d.f
cudaChannelFormatKindUnsigned; break;
case DXGI_FORMAT_R8G8B8A8_SINT: d.x = 8; d.y = 8; d.z = 8; d.w = 8; d.f
cudaChannelFormatKindSigned; break;
case DXGI_FORMAT_R16_UINT: d.x = 16; d.y = 0; d.z = 0; d.w = 0; d.f
cudaChannelFormatKindUnsigned; break;
case DXGI_FORMAT_R16_SINT: d.x = 16; d.y = 0; d.z = 0; d.w = 0; d.f
cudaChannelFormatKindSigned; break;
case DXGI_FORMAT_R16G16_UINT: d.x = 16; d.y = 16; d.z = 0; d.w = 0; d.f
cudaChannelFormatKindUnsigned; break;
case DXGI_FORMAT_R16G16_SINT: d.x = 16; d.y = 16; d.z = 0; d.w = 0; d.f
cudaChannelFormatKindSigned; break;
case DXGI_FORMAT_R16G16B16A16_UINT: d.x = 16; d.y = 16; d.z = 16; d.w = 16; d.f
cudaChannelFormatKindUnsigned; break;
case DXGI_FORMAT_R16G16B16A16_SINT: d.x = 16; d.y = 16; d.z = 16; d.w = 16; d.f
cudaChannelFormatKindSigned; break;
case DXGI_FORMAT_R32_UINT: d.x = 32; d.y = 0; d.z = 0; d.w = 0; d.f
cudaChannelFormatKindUnsigned; break;
case DXGI_FORMAT_R32_SINT: d.x = 32; d.y = 0; d.z = 0; d.w = 0; d.f
cudaChannelFormatKindSigned; break;
case DXGI_FORMAT_R32_FLOAT: d.x = 32; d.y = 0; d.z = 0; d.w = 0; d.f
cudaChannelFormatKindFloat; break;
case DXGI_FORMAT_R32G32_UINT: d.x = 32; d.y = 32; d.z = 0; d.w = 0; d.f
cudaChannelFormatKindUnsigned; break;
case DXGI_FORMAT_R32G32_SINT: d.x = 32; d.y = 32; d.z = 0; d.w = 0; d.f
cudaChannelFormatKindSigned; break;
case DXGI_FORMAT_R32G32_FLOAT: d.x = 32; d.y = 32; d.z = 0; d.w = 0; d.f
cudaChannelFormatKindFloat; break;
case DXGI_FORMAT_R32G32B32A32_UINT: d.x = 32; d.y = 32; d.z = 32; d.w = 32; d.f
cudaChannelFormatKindUnsigned; break;
case DXGI_FORMAT_R32G32B32A32_SINT: d.x = 32; d.y = 32; d.z = 32; d.w = 32; d.f
cudaChannelFormatKindSigned; break;
case DXGI_FORMAT_R32G32B32A32_FLOAT: d.x = 32; d.y = 32; d.z = 32; d.w = 32; d.f
cudaChannelFormatKindFloat; break;
default: assert(0);
}
```

```txt
return d;
}

cudaExtent getCudaExtentForD3D11Extent(UINT64 width, UINT height, UINT16
    depthOrArraySize, D3D12_SRV_DIMENSION d3d11SRVDimension) {
    cudaExtent e = { 0, 0, 0 };

    switch (d3d11SRVDimension) {
    case D3D11_SRV_DIMENSION_TEXTURE1D:        e.width = width; e.height = 0;      e.
    depth = 0;                     break;
    (continues on next page)
```

```txt
case D3D11_SRV_DIMENSION_TEXTURE2D: e.width = width; e.height = height; e.
depth = 0; break;
case D3D11_SRV_DIMENSION_TEXTURE3D: e.width = width; e.height = height; e.
depth = depthOrArraySize; break;
case D3D11_SRV_DIMENSION_TEXTURECUBE: e.width = width; e.height = height; e.
depth = depthOrArraySize; break;
case D3D11_SRV_DIMENSION_TEXTURE1DARRAY: e.width = width; e.height = 0; e.
depth = depthOrArraySize; break;
case D3D11_SRV_DIMENSION_TEXTURE2DARRAY: e.width = width; e.height = height; e.
depth = depthOrArraySize; break;
case D3D11_SRV_DIMENSION_TEXTURECUBEARRAY: e.width = width; e.height = height; e.
depth = depthOrArraySize; break;
default: assert(0);
}
return e;
}

unsigned int getCudaMipmappedArrayFlagsForD3D12Resource(D3D11_SRV_DIMENSION
d3d11SRVDimension, D3D11_BIND_FLAG d3d11BindFlags, bool allowSurfaceLoadStore) {
    unsigned int flags = 0;

    switch (d3d11SRVDimension) {
        case D3D11_SRV_DIMENSION_TEXTURECUBE: flags |= cudaArrayCubemap;
            break;
        case D3D11_SRV_DIMENSION_TEXTURECUBEARRAY: flags |= cudaArrayCubemap |
cudaArrayLayered; break;
        case D3D11_SRV_DIMENSION_TEXTURE1DARRAY: flags |= cudaArrayLayered;
            break;
        case D3D11_SRV_DIMENSION_TEXTURE2DARRAY: flags |= cudaArrayLayered;
            break;
    default: break;
}

if (d3d11BindFlags & D3D11_BIND_RENDER_TARGET) {
    flags |= cudaArrayColorAttachment;
}

if (allowSurfaceLoadStore) {
    flags |= cudaArraySurfaceLoadStore;
}

return flags;
}
```
````
