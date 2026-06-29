# CUDA Direct3D 11 Synchronization Object Import

CUDA allows the import of shareable Direct3D 11 synchronization objects, such as fences and keyed mutexes, into the CUDA runtime. This is achieved by providing the appropriate handle type (NT handle, named handle, or KMT handle) to the `cudaImportExternalSemaphore` function.

## Importing Direct3D 11 Fences

A shareable Direct3D 11 fence object is created by setting the `D3D11_FENCE_FLAG_SHARED` flag in the call to `ID3D11Device5::CreateFence` [CUDA_C_Programming_Guide:L5620-L5620]. This object can be imported into CUDA using the associated NT handle [CUDA_C_Programming_Guide:L5620-L5620].

### Using an NT Handle

To import a fence using an NT handle, configure a `cudaExternalSemaphoreHandleDesc` structure with `type` set to `cudaExternalSemaphoreHandleTypeD3D11Fence` and `handle.win32.handle` set to the NT handle [CUDA_C_Programming_Guide:L5622-L5664].

```cpp
cudaExternalSemaphore_t importD3D11FenceFromNTHandle(HANDLE handle) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));
    desc.type = cudaExternalSemaphoreHandleTypeD3D11Fence;
    desc.handle.win32.handle = handle;

    cudaImportExternalSemaphore(&extSem, &desc);

    // Input parameter 'handle' should be closed if it's not needed anymore
    CloseHandle(handle);

    return extSem;
}
```

### Using a Named Handle

A shareable Direct3D 11 fence can also be imported using a named handle if one exists [CUDA_C_Programming_Guide:L5622-L5664]. In this case, `handle.win32.name` is set to the name of the handle [CUDA_C_Programming_Guide:L5622-L5664].

```cpp
cudaExternalSemaphore_t importD3D11FenceFromNamedNTHandle(LPCWSTR name) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));
    desc.type = cudaExternalSemaphoreHandleTypeD3D11Fence;
    desc.handle.win32.name = (void *)name;

    cudaImportExternalSemaphore(&extSem, &desc);

    return extSem;
}
```

## Importing Direct3D 11 Keyed Mutexes

Keyed mutexes can be imported using either an NT handle or a named handle. The handle type is specified as `cudaExternalSemaphoreHandleTypeKeyedMutex` [CUDA_C_Programming_Guide:L5668-L5685] or `cudaExternalSemaphoreHandleTypeKeyedMutexKmt` [CUDA_C_Programming_Guide:L5709-L5726].

### Using an NT Handle

```cpp
cudaExternalSemaphore_t importD3D11KeyedMutexFromNTHandle(HANDLE handle) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));
    desc.type = cudaExternalSemaphoreHandleTypeKeyedMutex;
    desc.handle.win32.handle = handle;

    cudaImportExternalSemaphore(&extSem, &desc);

    // Input parameter 'handle' should be closed if it's not needed anymore
    CloseHandle(handle);

    return extSem;
}
```

### Using a Named Handle

```cpp
cudaExternalSemaphore_t importD3D11KeyedMutexFromNamedNTHandle(LPCWSTR name) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));
    desc.type = cudaExternalSemaphoreHandleTypeKeyedMutex;
    desc.handle.win32.name = (void *)name;

    cudaImportExternalSemaphore(&extSem, &desc);

    return extSem;
}
```

### Using a KMT Handle

Importing via a KMT (Kernel Mode Tracker) handle uses the type `cudaExternalSemaphoreHandleTypeKeyedMutexKmt` [CUDA_C_Programming_Guide:L5709-L5726].

```cpp
cudaExternalSemaphore_t importD3D11FenceFromKMTHandle(HANDLE handle) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));
    desc.type = cudaExternalSemaphoreHandleTypeKeyedMutexKmt;
    desc.handle.win32.handle = handle;

    cudaImportExternalSemaphore(&extSem, &desc);

    // Input parameter 'handle' should be closed if it's not needed anymore
    CloseHandle(handle);

    return extSem;
}
```

## Handle Management and Reference Counting

It is the application's responsibility to close the handle when it is no longer required [CUDA_C_Programming_Guide:L5620-L5620]. The NT handle holds a reference to the resource, so it must be explicitly freed before the underlying semaphore can be freed [CUDA_C_Programming_Guide:L5620-L5620]. When importing via an NT handle, the application should call `CloseHandle` on the input handle after the import is complete, provided the handle is no longer needed by the application [CUDA_C_Programming_Guide:L5622-L5664] [CUDA_C_Programming_Guide:L5668-L5685] [CUDA_C_Programming_Guide:L5709-L5726].

## See Also

- `cudaImportExternalSemaphore`
- `cudaExternalSemaphoreHandleDesc`
- `cudaExternalSemaphoreHandleType`
- Direct3D 11 Fence and Keyed Mutex documentation
