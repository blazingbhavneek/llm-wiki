# CUDA-Direct3D 12 Interoperability

Covers Direct3D 12 interoperability with CUDA, including device LUID matching, importing memory objects, mapping buffers and mipmapped arrays, and importing/signaling synchronization objects.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L4972-L5336

Citation: [CUDA_C_Programming_Guide:L4972-L5336]

````text
## 6.2.16.3 Direct3D 12 Interoperability

## 6.2.16.3.1 Matching Device LUIDs

When importing memory and synchronization objects exported by Direct3D 12, they must be imported and mapped on the same device as they were created on. The CUDA device that corresponds to the Direct3D 12 device on which the objects were created can be determined by comparing the LUID of a CUDA device with that of the Direct3D 12 device, as shown in the following code sample. Note that the Direct3D 12 device must not be created on a linked node adapter. I.e. the node count as returned by ID3D12Device::GetNodeCount must be 1.

```cpp
int getCudaDeviceForD3D12Device(ID3D12Device *d3d12Device) {
    LUID d3d12Luid = d3d12Device->GetAdapterLuid();

    int cudaDeviceCount;
    cudaGetDeviceCount(&cudaDeviceCount);

    for (int cudaDevice = 0; cudaDevice < cudaDeviceCount; cudaDevice++) {
        cudaDeviceProp deviceProp;
        cudaGetDeviceProperties(&deviceProp, cudaDevice);
        char *cudaLuid = deviceProp.luid;

        if (!memcmp(&d3d12Luid.LowPart, cudaLuid, sizeof(d3d12Luid.LowPart)) &&
            !memcmp(&d3d12Luid.HighPart, cudaLuid + sizeof(d3d12Luid.LowPart),
            sizeof(d3d12Luid.HighPart))) {
            return cudaDevice;
        }
    }
    return cudaInvalidDeviceId;
}
```

## 6.2.16.3.2 Importing Memory Objects

A shareable Direct3D 12 heap memory object, created by setting the flag D3D12\_HEAP\_FLAG\_SHARED in the call to ID3D12Device::CreateHeap, can be imported into CUDA using the NT handle associated with that object as shown below. Note that it is the application’s responsibility to close the NT handle when it is not required anymore. The NT handle holds a reference to the resource, so it must be explicitly freed before the underlying memory can be freed.

```txt
cudaExternalMemory_t importD3D12HeapFromNTHandle(HANDLE handle, unsigned long long
size) {
    cudaExternalMemory_t extMem = NULL;
    cudaExternalMemoryHandleDesc desc = {}

    memset(&desc, 0, sizeof(desc));
```

(continues on next page)

(continued from previous page)

```javascript
desc.type = cudaExternalMemoryHandleTypeD3D12Heap;
desc.handle.win32.handle = (void *)handle;
desc.size = size;

cudaImportExternalMemory(&extMem, &desc);

// Input parameter 'handle' should be closed if it's not needed anymore
CloseHandle(handle);

return extMem;
```

A shareable Direct3D 12 heap memory object can also be imported using a named handle if one exists as shown below.

```txt
cudaExternalMemory_t importD3D12HeapFromNamedNTHandle(LPCWSTR name, unsigned long
long size) {
    cudaExternalMemory_t extMem = NULL;
    cudaExternalMemoryHandleDesc desc = {}

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalMemoryHandleTypeD3D12Heap;
    desc.handle.win32.name = (void *)name;
    desc.size = size;

    cudaImportExternalMemory(&extMem, &desc);

    return extMem;
}
```

A shareable Direct3D 12 committed resource, created by setting the flag D3D12\_HEAP\_FLAG\_SHARED in the call to D3D12Device::CreateCommittedResource, can be imported into CUDA using the NT handle associated with that object as shown below. When importing a Direct3D 12 committed resource, the flag cudaExternalMemoryDedicated must be set. Note that it is the application’s responsibility to close the NT handle when it is not required anymore. The NT handle holds a reference to the resource, so it must be explicitly freed before the underlying memory can be freed.

```txt
cudaExternalMemory_t importD3D12CommittedResourceFromNTHandle(HANDLE handle, unsigned
long long size) {
    cudaExternalMemory_t extMem = NULL;
    cudaExternalMemoryHandleDesc desc = {}

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalMemoryHandleTypeD3D12Resource;
    desc.handle.win32.handle = (void *)handle;
    desc.size = size;
    desc.flags |= cudaExternalMemoryDedicated;

    cudaImportExternalMemory(&extMem, &desc);

    // Input parameter 'handle' should be closed if it's not needed anymore
    CloseHandle(handle);

    return extMem;
}
```

A shareable Direct3D 12 committed resource can also be imported using a named handle if one exists as shown below.

```txt
cudaExternalMemory_t importD3D12CommittedResourceFromNamedNTHandle(LPCWSTR name,
unsigned long long size) {
    cudaExternalMemory_t extMem = NULL;
    cudaExternalMemoryHandleDesc desc = {}

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalMemoryHandleTypeD3D12Resource;
    desc.handle.win32.name = (void *)name;
    desc.size = size;
    desc.flags |= cudaExternalMemoryDedicated;

    cudaImportExternalMemory(&extMem, &desc);

    return extMem;
}
```

## 6.2.16.3.3 Mapping Bufers onto Imported Memory Objects

A device pointer can be mapped onto an imported memory object as shown below. The ofset and size of the mapping must match that specified when creating the mapping using the corresponding Direct3D 12 API. All mapped device pointers must be freed using cudaFree().

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

## 6.2.16.3.4 Mapping Mipmapped Arrays onto Imported Memory Objects

A CUDA mipmapped array can be mapped onto an imported memory object as shown below. The ofset, dimensions, format and number of mip levels must match that specified when creating the mapping using the corresponding Direct3D 12 API. Additionally, if the mipmapped array can be bound as a render target in Direct3D 12, the flag cudaArrayColorAttachment must be set. All mapped mipmapped arrays must be freed using cudaFreeMipmappedArray(). The following code sample shows how to convert Vulkan parameters into the corresponding CUDA parameters when mapping mipmapped arrays onto imported memory objects.

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

cudaChannelFormatDesc getCudaChannelFormatDescForDxgiFormat(DXGI_FORMAT dxgiFormat)
{
    cudaChannelFormatDesc d;

    memset(&d, 0, sizeof(d));

    switch (dxgiFormat) {
        case DXGI_FORMAT_R8_UINT:            d.x = 8; d.y = 0; d.z = 0; d.w = 0; d.f
        = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R8_SINT:            d.x = 8; d.y = 0; d.z = 0; d.w = 0; d.f
        = cudaChannelFormatKindSigned; break;
        case DXGI_FORMAT_R8G8_UINT:            d.x = 8; d.y = 8; d.z = 0; d.w = 0; d.f
        = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R8G8_SINT:            d.x = 8; d.y = 8; d.z = 0; d.w = 0; d.f
        = cudaChannelFormatKindSigned; break;
        case DXGI_FORMAT_R8G8B8A8_UINT:     d.x = 8; d.y = 8; d.z = 8; d.w = 8; d.f
        = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R8G8B8A8_SINT:     d.x = 8; d.y = 8; d.z = 8; d.w = 8; d.f
        = cudaChannelFormatKindSigned; break;
        case DXGI_FORMAT_R16_UINT:           d.x = 16; d.y = 0; d.z = 0; d.w = 0; d.f
        = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R16_SINT:           d.x = 16; d.y = 0; d.z = 0; d.w = 0; d.f
        = cudaChannelFormatKindSigned; break;
        case DXGI_FORMAT_R16G16_UINT:     d.x = 16; d.y = 16; d.z = 0; d.w = 0; d.f
        = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R16G16_SINT:     d.x = 16; d.y = 16; d.z = 0; d.w = 0; d.f
        = cudaChannelFormatKindSigned; break;
        case DXGI_FORMAT_R16G16B16A16_UINT:   d.x = 16; d.y = 16; d.z = 16; d.w = 16; d.f
        = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R16G16B16A16_SINT:   d.x = 16; d.y = 16; d.z = 16; d.w = 16; d.f
        = cudaChannelFormatKindSigned; break;
        case DXGI_FORMAT_R32_UINT:          d.x = 32; d.y = 0; d.z = 0; d.w = 0; d.f
        = cudaChannelFormatKindUnsigned; break;
        case DXGI_FORMAT_R32_SINT:          d.x = 32; d.y = 0; d.z = 0; d.w = 0; d.f
        = cudaChannelFormatKindSigned; break;
        case DXGI_FORMAT_R32_FLOAT:          d.x = 32; d.y = 0; d.z = 0; d.w = 0; d.f
        = cudaChannelFormatKindFloat; break;
```

```javascript
case DXGI_FORMAT_R32G32_UINT:        d.x = 32; d.y = 32; d.z = 0;   d.w = 0;   d.f
cudaChannelFormatKindUnsigned; break;
case DXGI_FORMAT_R32G32_SINT:        d.x = 32; d.y = 32; d.z = 0;   d.w = 0;   d.f
cudaChannelFormatKindSigned;     break;
case DXGI_FORMAT_R32G32_FLOAT:        d.x = 32; d.y = 32; d.z = 0;   d.w = 0;   d.f
cudaChannelFormatKindFloat;     break;
case DXGI_FORMAT_R32G32B32A32_UINT:   d.x = 32; d.y = 32; d.z = 32; d.w = 32; d.f
cudaChannelFormatKindUnsigned; break;
case DXGI_FORMAT_R32G32B32A32_SINT:   d.x = 32; d.y = 32; d.z = 32; d.w = 32; d.f
cudaChannelFormatKindSigned;     break;
case DXGI_FORMAT_R32G32B32A32_FLOAT: d.x = 32; d.y = 32; d.z = 32; d.w = 32; d.f
cudaChannelFormatKindFloat;     break;
default: assert(0);
```

```c
}
    return d;
}

cudaExtent getCudaExtentForD3D12Extent(UINT64 width, UINT height, UINT16
depthOrArraySize, D3D12_SRV_DIMENSION d3d12SRVDimension) {
    cudaExtent e = { 0, 0, 0 };

    switch (d3d12SRVDimension) {
        case D3D12_SRV_DIMENSION_TEXTURE1D:            e.width = width; e.height = 0;      e.
        depth = 0;                  break;
        case D3D12_SRV_DIMENSION_TEXTURE2D:          e.width = width; e.height = height; e.
        depth = 0;                  break;
        case D3D12_SRV_DIMENSION_TEXTURE3D:          e.width = width; e.height = height; e.
        depth = depthOrArraySize; break;
        case D3D12_SRV_DIMENSION_TEXTURECUBE:       e.width = width; e.height = height; e.
        depth = depthOrArraySize; break;
        case D3D12_SRV_DIMENSION_TEXTURE1DARRAY:   e.width = width; e.height = 0;      e.
        depth = depthOrArraySize; break;
        case D3D12_SRV_DIMENSION_TEXTURE2DARRAY:   e.width = width; e.height = height; e.
        depth = depthOrArraySize; break;
        case D3D12_SRV_DIMENSION_TEXTURECUBEARRAY: e.width = width; e.height = height; e.
        depth = depthOrArraySize; break;
        default: assert(0);
    }

    return e;
}

unsigned int getCudaMipmappedArrayFlagsForD3D12Resource(D3D12_SRV_DIMENSION
d3d12SRVDimension, D3D12_RESOURCE_FLAGS d3d12ResourceFlags, bool
allowSurfaceLoadStore) {
    unsigned int flags = 0;

    switch (d3d12SRVDimension) {
        case D3D12_SRV_DIMENSION_TEXTURECUBE:       flags |= cudaArrayCubemap;
        break;
        case D3D12_SRV_DIMENSION_TEXTURECUBEARRAY: flags |= cudaArrayCubemap |
cudaArrayLayered; break;
        case D3D12_SRV_DIMENSION_TEXTURE1DARRAY:   flags |= cudaArrayLayered;
        break;
```

```txt
case D3D12_SRV_DIMENSION_TEXTURE2DARRAY: flags |= cudaArrayLayered;
    break;
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

## 6.2.16.3.5 Importing Synchronization Objects

A shareable Direct3D 12 fence object, created by setting the flag D3D12\_FENCE\_FLAG\_SHARED in the call to ID3D12Device::CreateFence, can be imported into CUDA using the NT handle associated with that object as shown below. Note that it is the application’s responsibility to close the handle when it is not required anymore. The NT handle holds a reference to the resource, so it must be explicitly freed before the underlying semaphore can be freed.

```txt
cudaExternalSemaphore_t importD3D12FenceFromNTHandle(HANDLE handle) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {}

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalSemaphoreHandleTypeD3D12Fence;
    desc.handle.win32.handle = handle;

    cudaImportExternalSemaphore(&extSem, &desc);

    // Input parameter 'handle' should be closed if it's not needed anymore
    CloseHandle(handle);

    return extSem;
}
```

A shareable Direct3D 12 fence object can also be imported using a named handle if one exists as shown below.

```txt
cudaExternalSemaphore_t importD3D12FenceFromNamedNTHandle(LPCWSTR name) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {}

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalSemaphoreHandleTypeD3D12Fence;
    desc.handle.win32.name = (void *)name;

    cudaImportExternalSemaphore(&extSem, &desc);
```

(continues on next page)

```txt
return extSem;
}
```

(continued from previous page)

## 6.2.16.3.6 Signaling/Waiting on Imported Synchronization Objects

An imported Direct3D 12 fence object can be signaled as shown below. Signaling such a fence object sets its value to the one specified. The corresponding wait that waits on this signal must be issued in Direct3D 12. Additionally, the wait that waits on this signal must be issued after this signal has been issued.

```javascript
void signalExternalSemaphore(cudaExternalSemaphore_t extSem, unsigned long long value,
    cudaStream_t stream) {
    cudaExternalSemaphoreSignalParams params = {}

    memset(&params, 0, sizeof(params));

    params.params.fence.value = value;

    cudaSignalExternalSemaphoresAsync(&extSem, &params, 1, stream);
}
```

An imported Direct3D 12 fence object can be waited on as shown below. Waiting on such a fence object waits until its value becomes greater than or equal to the specified value. The corresponding signal that this wait is waiting on must be issued in Direct3D 12. Additionally, the signal must be issued before this wait can be issued.

```javascript
void waitExternalSemaphore(cudaExternalSemaphore_t extSem, unsigned long long value,
→ cudaStream_t stream) {
    cudaExternalSemaphoreWaitParams params = {}

    memset(&params, 0, sizeof(params));

    params.params.fence.value = value;

    cudaWaitExternalSemaphoresAsync(&extSem, &params, 1, stream);
}
```
````
