# Importing Direct3D 12 Memory Objects into CUDA

CUDA allows applications to import shareable Direct3D 12 memory objects, enabling interoperability between Direct3D 12 and CUDA. This process involves importing memory from shareable heaps or committed resources using NT handles. There are two primary types of shareable Direct3D 12 memory objects that can be imported: heaps and committed resources.

## Importing Shareable Heaps

A shareable Direct3D 12 heap memory object is created by setting the `D3D12_HEAP_FLAG_SHARED` flag in the call to `ID3D12Device::CreateHeap` [CUDA_C_Programming_Guide:L4999-L5093]. This type of memory can be imported into CUDA using the associated NT handle [CUDA_C_Programming_Guide:L4999-L5093].

### Using an NT Handle

To import a shareable heap using an NT handle, the application must configure a `cudaExternalMemoryHandleDesc` structure with the following parameters:

*   `type`: Set to `cudaExternalMemoryHandleTypeD3D12Heap` [CUDA_C_Programming_Guide:L4999-L5093].
*   `handle.win32.handle`: Set to the NT handle obtained from the Direct3D 12 heap [CUDA_C_Programming_Guide:L4999-L5093].
*   `size`: The size of the memory region to import [CUDA_C_Programming_Guide:L4999-L5093].

The `cudaImportExternalMemory` function is then called to perform the import [CUDA_C_Programming_Guide:L4999-L5093].

### Using a Named NT Handle

If a named handle exists for the shareable heap, it can be used for import instead of a regular NT handle [CUDA_C_Programming_Guide:L4999-L5093]. The configuration is similar, but:

*   `handle.win32.name`: Set to the name of the handle [CUDA_C_Programming_Guide:L4999-L5093].
*   The `handle.win32.handle` field is not used [CUDA_C_Programming_Guide:L4999-L5093].

## Importing Committed Resources

A shareable Direct3D 12 committed resource is created by setting the `D3D12_HEAP_FLAG_SHARED` flag in the call to `ID3D12Device::CreateCommittedResource` [CUDA_C_Programming_Guide:L4999-L5093]. Importing committed resources requires an additional flag to indicate that the memory is dedicated to a specific resource [CUDA_C_Programming_Guide:L4999-L5093].

### Using an NT Handle

When importing a committed resource using an NT handle, the `cudaExternalMemoryHandleDesc` structure must be configured as follows:

*   `type`: Set to `cudaExternalMemoryHandleTypeD3D12Resource` [CUDA_C_Programming_Guide:L4999-L5093].
*   `handle.win32.handle`: Set to the NT handle [CUDA_C_Programming_Guide:L4999-L5093].
*   `size`: The size of the memory region [CUDA_C_Programming_Guide:L4999-L5093].
*   `flags`: The `cudaExternalMemoryDedicated` flag must be set [CUDA_C_Programming_Guide:L4999-L5093].

### Using a Named NT Handle

Committed resources can also be imported using a named handle [CUDA_C_Programming_Guide:L4999-L5093]. The configuration is similar to the regular NT handle import, but:

*   `handle.win32.name`: Set to the name of the handle [CUDA_C_Programming_Guide:L4999-L5093].
*   The `cudaExternalMemoryDedicated` flag must still be set in `flags` [CUDA_C_Programming_Guide:L4999-L5093].

## Handle Ownership and Management

Regardless of the type of memory object or handle used, the application is responsible for managing the lifecycle of the NT handle [CUDA_C_Programming_Guide:L4999-L5093].

*   **Closing Handles**: The application must close the NT handle using `CloseHandle` when it is no longer required [CUDA_C_Programming_Guide:L4999-L5093].
*   **Resource Lifetime**: The NT handle holds a reference to the underlying resource [CUDA_C_Programming_Guide:L4999-L5093]. Therefore, the handle must be explicitly freed before the underlying Direct3D 12 memory can be freed [CUDA_C_Programming_Guide:L4999-L5093].

## Example Implementations

### Importing a Heap from an NT Handle

```c
cudaExternalMemory_t importD3D12HeapFromNTHandle(HANDLE handle, unsigned long long size) {
    cudaExternalMemory_t extMem = NULL;
    cudaExternalMemoryHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));
    desc.type = cudaExternalMemoryHandleTypeD3D12Heap;
    desc.handle.win32.handle = (void *)handle;
    desc.size = size;

    cudaImportExternalMemory(&extMem, &desc);

    // Input parameter 'handle' should be closed if it's not needed anymore
    CloseHandle(handle);

    return extMem;
}
```

### Importing a Heap from a Named NT Handle

```c
cudaExternalMemory_t importD3D12HeapFromNamedNTHandle(LPCWSTR name, unsigned long long size) {
    cudaExternalMemory_t extMem = NULL;
    cudaExternalMemoryHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));
    desc.type = cudaExternalMemoryHandleTypeD3D12Heap;
    desc.handle.win32.name = (void *)name;
    desc.size = size;

    cudaImportExternalMemory(&extMem, &desc);

    return extMem;
}
```

### Importing a Committed Resource from an NT Handle

```c
cudaExternalMemory_t importD3D12CommittedResourceFromNTHandle(HANDLE handle, unsigned long long size) {
    cudaExternalMemory_t extMem = NULL;
    cudaExternalMemoryHandleDesc desc = {};

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

### Importing a Committed Resource from a Named NT Handle

```c
cudaExternalMemory_t importD3D12CommittedResourceFromNamedNTHandle(LPCWSTR name, unsigned long long size) {
    cudaExternalMemory_t extMem = NULL;
    cudaExternalMemoryHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));
    desc.type = cudaExternalMemoryHandleTypeD3D12Resource;
    desc.handle.win32.name = (void *)name;
    desc.size = size;
    desc.flags |= cudaExternalMemoryDedicated;

    cudaImportExternalMemory(&extMem, &desc);

    return extMem;
}
```
