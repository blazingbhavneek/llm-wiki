# Importing Direct3D 12 Fence Objects into CUDA

A shareable Direct3D 12 fence object can be imported into CUDA to enable synchronization between Direct3D 12 and CUDA contexts. To create a shareable fence, the application must set the flag `D3D12_FENCE_FLAG_SHARED` in the call to `ID3D12Device::CreateFence` [CUDA_C_Programming_Guide:L5257-L5301].

## Importing via NT Handle

A shareable Direct3D 12 fence can be imported into CUDA using the NT handle associated with that object. The import process involves configuring a `cudaExternalSemaphoreHandleDesc` structure and calling `cudaImportExternalSemaphore` [CUDA_C_Programming_Guide:L5257-L5301].

```cpp
cudaExternalSemaphore_t importD3D12FenceFromNTHandle(HANDLE handle) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalSemaphoreHandleTypeD3D12Fence;
    desc.handle.win32.handle = handle;

    cudaImportExternalSemaphore(&extSem, &desc);

    // Input parameter 'handle' should be closed if it's not needed anymore
    CloseHandle(handle);

    return extSem;
}
```

## Importing via Named NT Handle

A shareable Direct3D 12 fence object can also be imported using a named handle if one exists. This is achieved by specifying the name in the `cudaExternalSemaphoreHandleDesc` structure [CUDA_C_Programming_Guide:L5257-L5301].

```cpp
cudaExternalSemaphore_t importD3D12FenceFromNamedNTHandle(LPCWSTR name) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalSemaphoreHandleTypeD3D12Fence;
    desc.handle.win32.name = (void *)name;

    cudaImportExternalSemaphore(&extSem, &desc);

    return extSem;
}
```

## Resource Management

It is the application’s responsibility to close the NT handle when it is no longer required. The NT handle holds a reference to the resource, so it must be explicitly freed before the underlying semaphore can be freed [CUDA_C_Programming_Guide:L5257-L5301].

## See Also

- [CUDA C Programming Guide: Synchronization](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#synchronization)
- [Direct3D 12 Fence Documentation](https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nn-d3d12-id3d12fence)
