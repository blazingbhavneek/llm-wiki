# CUDA Direct3D 11 Memory Import

CUDA allows applications to import memory from Direct3D 11 (D3D11) resources, enabling interoperability between D3D11 rendering and CUDA compute operations. This process involves creating shareable D3D11 resources with specific flags and importing them into CUDA using the `cudaImportExternalMemory` function.

## Creating Shareable D3D11 Resources

To make a Direct3D 11 resource shareable with CUDA, specific miscellaneous flags must be set during resource creation. The available flags depend on the resource type and the Windows version.

### Texture Resources

Shareable texture resources (`ID3D11Texture1D`, `ID3D11Texture2D`, or `ID3D11Texture3D`) can be created by setting one of the following flags when calling `ID3D11Device::CreateTexture1D`, `ID3D11Device::CreateTexture2D`, or `ID3D11Device::CreateTexture3D`:

*   `D3D11_RESOURCE_MISC_SHARED`: A general shared flag.
*   `D3D11_RESOURCE_MISC_SHARED_KEYEDMUTEX`: Available on Windows 7, this flag enables keyed mutex synchronization.
*   `D3D11_RESOURCE_MISC_SHARED_NTHANDLE`: Available on Windows 10, this flag creates an NT handle associated with the resource.

### Buffer Resources

Shareable buffer resources (`ID3D11Buffer`) can be created by specifying any of the above flags (`D3D11_RESOURCE_MISC_SHARED`, `D3D11_RESOURCE_MISC_SHARED_KEYEDMUTEX`, or `D3D11_RESOURCE_MISC_SHARED_NTHANDLE`) when calling `ID3D11Device::CreateBuffer`.

## Importing Resources into CUDA

Once a shareable D3D11 resource is created, it can be imported into CUDA using `cudaImportExternalMemory`. The import method depends on the type of handle associated with the resource.

### Importing via NT Handle (Windows 10)

Resources created with the `D3D11_RESOURCE_MISC_SHARED_NTHANDLE` flag can be imported using the associated NT handle. When importing such a resource, the flag `cudaExternalMemoryDedicated` must be set in the `cudaExternalMemoryHandleDesc` structure.

The application is responsible for managing the lifecycle of the NT handle. The NT handle holds a reference to the resource, so it must be explicitly closed (freed) before the underlying memory can be freed by D3D11. However, the CUDA external memory object must remain valid as long as it is used by CUDA.

```cpp
cudaExternalMemory_t importD3D11ResourceFromNTHandle(HANDLE handle, unsigned long long size) {
    cudaExternalMemory_t extMem = NULL;
    cudaExternalMemoryHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalMemoryHandleTypeD3D11Resource;
    desc.handle.win32.handle = (void *)handle;
    desc.size = size;
    desc.flags |= cudaExternalMemoryDedicated;

    cudaImportExternalMemory(&extMem, &desc);

    // The NT handle is no longer needed after import, so it can be closed.
    // Note: The resource memory remains valid as long as the CUDA external memory object exists.
    CloseHandle(handle);

    return extMem;
}
```

### Importing via Named NT Handle

If a shareable D3D11 resource has a name, it can be imported using that name instead of a direct handle.

```cpp
cudaExternalMemory_t importD3D11ResourceFromNamedNTHandle(LPCWSTR name, unsigned long long size) {
    cudaExternalMemory_t extMem = NULL;
    cudaExternalMemoryHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalMemoryHandleTypeD3D11Resource;
    desc.handle.win32.name = (void *)name;
    desc.size = size;
    desc.flags |= cudaExternalMemoryDedicated;

    cudaImportExternalMemory(&extMem, &desc);

    return extMem;
}
```

### Importing via KMT Handle

Resources can also be imported using a Kernel-Mode Table (KMT) handle. This method uses the handle type `cudaExternalMemoryHandleTypeD3D11ResourceKmt`.

```cpp
cudaExternalMemory_t importD3D11ResourceFromKMTHandle(HANDLE handle, unsigned long long size) {
    cudaExternalMemory_t extMem = NULL;
    cudaExternalMemoryHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalMemoryHandleTypeD3D11ResourceKmt;
    desc.handle.win32.handle = (void *)handle;
    desc.size = size;
    desc.flags |= cudaExternalMemoryDedicated;

    cudaImportExternalMemory(&extMem, &desc);

    return extMem;
}
```

## Important Considerations

*   **Dedicated Memory Flag**: When importing a Direct3D 11 resource, the flag `cudaExternalMemoryDedicated` must always be set in the `cudaExternalMemoryHandleDesc` structure.
*   **Handle Management**: For NT handle imports, the application must close the NT handle using `CloseHandle` after importing the resource, as the handle is no longer required for CUDA operations. However, the underlying resource memory is not freed until the CUDA external memory object is destroyed and the D3D11 resource is released.

[doc_id:L5383-L5383]
[doc_id:L5385-L5432]
[doc_id:L5436-L5453]
