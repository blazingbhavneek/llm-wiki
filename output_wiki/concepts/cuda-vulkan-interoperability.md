# CUDA-Vulkan Interoperability

Covers the interoperability between CUDA and Vulkan, including extent conversion, memory object importing, synchronization object importing, and signaling/waiting operations.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L4738-L4956

Citation: [CUDA_C_Programming_Guide:L4738-L4956]

````text
(continues on next page)

```solidity
case VK_FORMAT_R8_UINT:
cudaChannelFormatKindUnsigned; break;
case VK_FORMAT_R8_SINT:
cudaChannelFormatKindSigned; break;
case VK_FORMAT_R8G8_UINT:
cudaChannelFormatKindUnsigned; break;
case VK_FORMAT_R8G8_SINT:
cudaChannelFormatKindSigned; break;
case VK_FORMAT_R8G8B8A8_UINT:
cudaChannelFormatKindUnsigned; break;
case VK_FORMAT_R8G8B8A8_SINT:
cudaChannelFormatKindSigned; break;
case VK_FORMAT_R16_UINT:
cudaChannelFormatKindUnsigned; break;
case VK_FORMAT_R16_SINT:
cudaChannelFormatKindSigned; break;
case VK_FORMAT_R16G16_UINT:
cudaChannelFormatKindUnsigned; break;
case VK_FORMAT_R16G16_SINT:
cudaChannelFormatKindSigned; break;
case VK_FORMAT_R16G16B16A16_UINT:
cudaChannelFormatKindUnsigned; break;
case VK_FORMAT_R16G16B16A16_SINT:
cudaChannelFormatKindSigned; break;
case VK_FORMAT_R32_UINT:
cudaChannelFormatKindUnsigned; break;
case VK_FORMAT_R32_SINT:
cudaChannelFormatKindSigned; break;
case VK_FORMAT_R32_SFLOAT:
cudaChannelFormatKindFloat; break;
case VK_FORMAT_R32G32_UINT:
cudaChannelFormatKindUnsigned; break;
case VK_FORMAT_R32G32_SINT:
cudaChannelFormatKindSigned; break;
case VK_FORMAT_R32G32_SFLOAT:
cudaChannelFormatKindFloat; break;
case VK_FORMAT_R32G32B32A32_UINT:
cudaChannelFormatKindUnsigned; break;
case VK_FORMAT_R32G32B32A32_SINT:
cudaChannelFormatKindSigned; break;
case VK_FORMAT_R32G32B32A32_SFLOAT:
cudaChannelFormatKindFloat; break;
default: assert(0);
}
```

```txt
return d;
}

cudaExtent getCudaExtentForVulkanExtent(VkExtent3D vkExt, uint32_t arrayLayers,
VkImageViewType vkImageViewType) {
    cudaExtent e = { 0, 0, 0 };

    switch (vkImageViewType) {
        case VK_IMAGE_VIEW_TYPE_1D:          e.width = vkExt.width; e.height = 0;
        e.depth = 0;            break;
        case VK_IMAGE_VIEW_TYPE_2D:      e.width = vkExt.width; e.height = vkExt.
        height; e.depth = 0;            break;
```

```txt
case VK_IMAGE_VIEW_TYPE_3D: e.width = vkExt.width; e.height = vkExt.
height; e.depth = vkExt.depth; break;
case VK_IMAGE_VIEW_TYPE_CUBE: e.width = vkExt.width; e.height = vkExt.
height; e.depth = arrayLayers; break;
case VK_IMAGE_VIEW_TYPE_1D_ARRAY: e.width = vkExt.width; e.height = 0;
e.depth = arrayLayers; break;
case VK_IMAGE_VIEW_TYPE_2D_ARRAY: e.width = vkExt.width; e.height = vkExt.
height; e.depth = arrayLayers; break;
case VK_IMAGE_VIEW_TYPE_CUBE_ARRAY: e.width = vkExt.width; e.height = vkExt.
height; e.depth = arrayLayers; break;
default: assert(0);
}

return e;
}

unsigned int getCudaMipmappedArrayFlagsForVulkanImage(VkImageViewType vkImageViewType,
VkImageUsageFlags vkImageUsageFlags, bool allowSurfaceLoadStore) {
    unsigned int flags = 0;

    switch (vkImageViewType) {
        case VK_IMAGE_VIEW_TYPE_CUBE: flags |= cudaArrayCubemap;
        break;
        case VK_IMAGE_VIEW_TYPE_CUBE_ARRAY: flags |= cudaArrayCubemap | cudaArrayLayered;
        break;
        case VK_IMAGE_VIEW_TYPE_1D_ARRAY: flags |= cudaArrayLayered;
        break;
        case VK_IMAGE_VIEW_TYPE_2D_ARRAY: flags |= cudaArrayLayered;
        break;
        default: break;
    }

    if (vkImageUsageFlags & VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT) {
        flags |= cudaArrayColorAttachment;
    }

    if (allowSurfaceLoadStore) {
        flags |= cudaArraySurfaceLoadStore;
    }
    return flags;
}
```

## 6.2.16.1.5 Importing Synchronization Objects

A Vulkan semaphore object exported using VK\_EXTERNAL\_SEMAPHORE\_HANDLE\_TYPE\_OPAQUE\_FD\_BITcan be imported into CUDA using the file descriptor associated with that object as shown below. Note that CUDA assumes ownership of the file descriptor once it is imported. Using the file descriptor after a successful import results in undefined behavior.

```txt
cudaExternalSemaphore_t importVulkanSemaphoreObjectFromFileDescriptor(int fd) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {}

    memset(&desc, 0, sizeof(desc));
```

(continues on next page)

(continued from previous page)

```txt
desc.type = cudaExternalSemaphoreHandleTypeOpaqueFd;
    desc.handle.fd = fd;

    cudaImportExternalSemaphore(&extSem, &desc);

    // Input parameter 'fd' should not be used beyond this point as CUDA has assumed ownership of it

    return extSem;
}
```

A Vulkan semaphore object exported using VK\_EXTERNAL\_SEMAPHORE\_HANDLE\_TYPE\_OPAQUE\_WIN32\_BIT can be imported into CUDA using the NT handle associated with that object as shown below. Note that CUDA does not assume ownership of the NT handle and it is the application’s responsibility to close the handle when it is not required anymore. The NT handle holds a reference to the resource, so it must be explicitly freed before the underlying semaphore can be freed.

```txt
cudaExternalSemaphore_t importVulkanSemaphoreObjectFromNTHandle(HANDLE handle) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {}

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalSemaphoreHandleTypeOpaqueWin32;
    desc.handle.win32.handle = handle;

    cudaImportExternalSemaphore(&extSem, &desc);

    // Input parameter 'handle' should be closed if it's not needed anymore
    CloseHandle(handle);

    return extSem;
}
```

A Vulkan semaphore object exported using VK\_EXTERNAL\_SEMAPHORE\_HANDLE\_TYPE\_OPAQUE\_WIN32\_BIT can also be imported using a named handle if one exists as shown below.

```txt
cudaExternalSemaphore_t importVulkanSemaphoreObjectFromNamedNTHandle(LPCWSTR name) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {}

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalSemaphoreHandleTypeOpaqueWin32;
    desc.handle.win32.name = (void *)name;

    cudaImportExternalSemaphore(&extSem, &desc);

    return extSem;
}
```

A Vulkan semaphore object exported using VK\_EXTERNAL\_SEMAPHORE\_HANDLE\_TYPE\_OPAQUE\_WIN32\_KMT\_BIT can be imported into CUDA using the globally shared D3DKMT handle associated with that object as shown below. Since a globally shared D3DKMT handle does not hold a reference to the underlying semaphore it is automatically destroyed when all other references to the resource are destroyed.

```objectivec
cudaExternalSemaphore_t importVulkanSemaphoreObjectFromKMTHandle(HANDLE handle) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {}

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalSemaphoreHandleTypeOpaqueWin32Kmt;
    desc.handle.win32.handle = (void *)handle;

    cudaImportExternalSemaphore(&extSem, &desc);

    return extSem;
}
```

## 6.2.16.1.6 Signaling/Waiting on Imported Synchronization Objects

An imported Vulkan semaphore object can be signaled as shown below. Signaling such a semaphore object sets it to the signaled state. The corresponding wait that waits on this signal must be issued in Vulkan. Additionally, the wait that waits on this signal must be issued after this signal has been issued.

```txt
void signalExternalSemaphore(cudaExternalSemaphore_t extSem, cudaStream_t stream) {
    cudaExternalSemaphoreSignalParams params = {}

    memset(&params, 0, sizeof(params));

    cudaSignalExternalSemaphoresAsync(&extSem, &params, 1, stream);
}
```

An imported Vulkan semaphore object can be waited on as shown below. Waiting on such a semaphore object waits until it reaches the signaled state and then resets it back to the unsignaled state. The corresponding signal that this wait is waiting on must be issued in Vulkan. Additionally, the signal must be issued before this wait can be issued.

```cpp
void waitExternalSemaphore(cudaExternalSemaphore_t extSem, cudaStream_t stream) {
    cudaExternalSemaphoreWaitParams params = {}

    memset(&params, 0, sizeof(params));

    cudaWaitExternalSemaphoresAsync(&extSem, &params, 1, stream);
}
```
````
