# Importing Vulkan Synchronization Objects into CUDA

CUDA provides the `cudaImportExternalSemaphore` function to import Vulkan synchronization objects, specifically semaphores, into the CUDA environment. This allows for interoperability between Vulkan and CUDA execution streams. The method of import depends on the type of handle used to export the semaphore from Vulkan.

## Opaque File Descriptor (FD)

A Vulkan semaphore object exported using `VK_EXTERNAL_SEMAPHORE_HANDLE_TYPE_OPAQUE_FD_BIT` can be imported into CUDA using the associated file descriptor [CUDA_C_Programming_Guide:L4846-L4929].

**Ownership Semantics:**
*   CUDA assumes ownership of the file descriptor once it is imported [CUDA_C_Programming_Guide:L4846-L4929].
*   Using the file descriptor after a successful import results in undefined behavior [CUDA_C_Programming_Guide:L4846-L4929].

**Example:**

```c
cudaExternalSemaphore_t importVulkanSemaphoreObjectFromFileDescriptor(int fd) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));
    desc.type = cudaExternalSemaphoreHandleTypeOpaqueFd;
    desc.handle.fd = fd;

    cudaImportExternalSemaphore(&extSem, &desc);

    // Input parameter 'fd' should not be used beyond this point as CUDA has assumed ownership of it

    return extSem;
}
```

## Opaque Win32 NT Handle

A Vulkan semaphore object exported using `VK_EXTERNAL_SEMAPHORE_HANDLE_TYPE_OPAQUE_WIN32_BIT` can be imported using the NT handle associated with that object [CUDA_C_Programming_Guide:L4846-L4929].

**Ownership Semantics:**
*   CUDA does **not** assume ownership of the NT handle [CUDA_C_Programming_Guide:L4846-L4929].
*   It is the application’s responsibility to close the handle when it is no longer required [CUDA_C_Programming_Guide:L4846-L4929].
*   The NT handle holds a reference to the resource, so it must be explicitly freed before the underlying semaphore can be freed [CUDA_C_Programming_Guide:L4846-L4929].

**Example:**

```c
cudaExternalSemaphore_t importVulkanSemaphoreObjectFromNTHandle(HANDLE handle) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalSemaphoreHandleTypeOpaqueWin32;
    desc.handle.win32.handle = handle;

    cudaImportExternalSemaphore(&extSem, &desc);

    // Input parameter 'handle' should be closed if it's not needed anymore
    CloseHandle(handle);

    return extSem;
}
```

## Named NT Handle

A Vulkan semaphore object exported using `VK_EXTERNAL_SEMAPHORE_HANDLE_TYPE_OPAQUE_WIN32_BIT` can also be imported using a named handle if one exists [CUDA_C_Programming_Guide:L4846-L4929].

**Example:**

```c
cudaExternalSemaphore_t importVulkanSemaphoreObjectFromNamedNTHandle(LPCWSTR name) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalSemaphoreHandleTypeOpaqueWin32;
    desc.handle.win32.name = (void *)name;

    cudaImportExternalSemaphore(&extSem, &desc);

    return extSem;
}
```

## Opaque Win32 KMT Handle

A Vulkan semaphore object exported using `VK_EXTERNAL_SEMAPHORE_HANDLE_TYPE_OPAQUE_WIN32_KMT_BIT` can be imported using the globally shared D3DKMT handle associated with that object [CUDA_C_Programming_Guide:L4846-L4929].

**Ownership Semantics:**
*   A globally shared D3DKMT handle does not hold a reference to the underlying semaphore [CUDA_C_Programming_Guide:L4846-L4929].
*   The semaphore is automatically destroyed when all other references to the resource are destroyed [CUDA_C_Programming_Guide:L4846-L4929].

**Example:**

```c
cudaExternalSemaphore_t importVulkanSemaphoreObjectFromKMTHandle(HANDLE handle) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalSemaphoreHandleTypeOpaqueWin32Kmt;
    desc.handle.win32.handle = (void *)handle;

    cudaImportExternalSemaphore(&extSem, &desc);

    return extSem;
}
```
