# Direct3D 11 Memory Object Import

Imports shareable Direct3D 11 textures and buffers into CUDA using NT handles, named handles, or KMT handles.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L5380-L5453

Citation: [CUDA_C_Programming_Guide:L5380-L5453]

````text

## 6.2.16.4.2 Importing Memory Objects

A shareable Direct3D 11 texture resource, viz, ID3D11Texture1D, ID3D11Texture2D or ID3D11Texture3D, can be created by setting either the D3D11\_RESOURCE\_MISC\_SHARED or D3D11\_RESOURCE\_MISC\_SHARED\_KEYEDMUTEX (on Windows 7) or D3D11\_RESOURCE\_MISC\_SHARED\_NTHANDLE (on Windows 10) when calling ID3D11Device:CreateTexture1D, ID3D11Device:CreateTexture2D or ID3D11Device:CreateTexture3D respectively. A shareable Direct3D 11 bufer resource, ID3D11Buffer, can be created by specifying either of the above flags when calling ID3D11Device::CreateBuffer. A shareable resource created by specifying the D3D11\_RESOURCE\_MISC\_SHARED\_NTHANDLE can be imported into CUDA using the NT handle associated with that object as shown below. Note that it is the application’s responsibility to close the NT handle when it is not required anymore. The NT handle holds a reference to the resource, so it must be explicitly freed before the underlying memory can be freed. When importing a Direct3D 11 resource, the flag cudaExternalMemoryDedicated must be set.

```txt
cudaExternalMemory_t importD3D11ResourceFromNTHandle(HANDLE handle, unsigned long
long size) {
    cudaExternalMemory_t extMem = NULL;
    cudaExternalMemoryHandleDesc desc = {}

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalMemoryHandleTypeD3D11Resource;
    desc.handle.win32.handle = (void *)handle;
    desc.size = size;
    desc.flags |= cudaExternalMemoryDedicated;

    cudaImportExternalMemory(&extMem, &desc);
```

(continues on next page)

```txt
(continued from previous page)

// Input parameter 'handle' should be closed if it's not needed anymore
CloseHandle(handle);

return extMem;
}
```

A shareable Direct3D 11 resource can also be imported using a named handle if one exists as shown below.

```txt
cudaExternalMemory_t importD3D11ResourceFromNamedNTHandle(LPCWSTR name, unsigned long
long size) {
    cudaExternalMemory_t extMem = NULL;
    cudaExternalMemoryHandleDesc desc = {}

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalMemoryHandleTypeD3D11Resource;
    desc.handle.win32.name = (void *)name;
    desc.size = size;
    desc.flags |= cudaExternalMemoryDedicated;

    cudaImportExternalMemory(&extMem, &desc);

    return extMem;
}
```

A shareable Direct3D 11 resource, created by specifying the D3D11\_RESOURCE\_MISC\_SHARED or D3D11\_RESOURCE\_MISC\_SHARED\_KEYEDMUTEX, can be imported into CUDA using the globally shared D3DKMT handle associated with that object as shown below. Since a globally shared D3DKMT handle does not hold a reference to the underlying memory it is automatically destroyed when all other references to the resource are destroyed.

```txt
cudaExternalMemory_t importD3D11ResourceFromKMTHandle(HANDLE handle, unsigned long
long size) {
    cudaExternalMemory_t extMem = NULL;
    cudaExternalMemoryHandleDesc desc = {}

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalMemoryHandleTypeD3D11ResourceKmt;
    desc.handle.win32.handle = (void *)handle;
    desc.size = size;
    desc.flags |= cudaExternalMemoryDedicated;

    cudaImportExternalMemory(&extMem, &desc);

    return extMem;
}
```
````
