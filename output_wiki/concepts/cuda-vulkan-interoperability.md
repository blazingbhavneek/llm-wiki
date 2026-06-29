# CUDA Vulkan Interoperability

CUDA Vulkan Interoperability enables the integration of CUDA and Vulkan by allowing memory and synchronization objects exported by Vulkan to be imported and used within CUDA. This interoperability requires strict device matching and specific handling of memory objects depending on the operating system and handle type.

## Device UUID Matching

When importing memory and synchronization objects exported by Vulkan, they must be imported and mapped on the same CUDA device as the Vulkan physical device on which the objects were created [CUDA_C_Programming_Guide:L4528-L4737]. The corresponding CUDA device can be identified by comparing the UUID of the CUDA device with the UUID of the Vulkan physical device [CUDA_C_Programming_Guide:L4528-L4737].

The Vulkan physical device used for this matching should not be part of a device group containing more than one Vulkan physical device; specifically, the device group returned by `vkEnumeratePhysicalDeviceGroups` must have a physical device count of 1 [CUDA_C_Programming_Guide:L4528-L4737]. The device UUID can be retrieved from the Vulkan physical device using `VkPhysicalDeviceIDProperties` and compared against CUDA device properties obtained via `cudaGetDeviceProperties` [CUDA_C_Programming_Guide:L4528-L4737].

## Importing Memory Objects

The ability to import Vulkan memory objects into CUDA depends on the operating system and whether the memory is dedicated or non-dedicated [CUDA_C_Programming_Guide:L4528-L4737].

### Platform Support

*   **Linux and Windows 10:** Both dedicated and non-dedicated memory objects exported by Vulkan can be imported into CUDA [CUDA_C_Programming_Guide:L4528-L4737].
*   **Windows 7:** Only dedicated memory objects can be imported [CUDA_C_Programming_Guide:L4528-L4737].

When importing a Vulkan dedicated memory object, the `cudaExternalMemoryDedicated` flag must be set in the import descriptor [CUDA_C_Programming_Guide:L4528-L4737].

### Handle Types

Vulkan memory objects can be imported into CUDA using several handle types, each with specific ownership and lifecycle semantics [CUDA_C_Programming_Guide:L4528-L4737].

#### Opaque FD (Linux)

A Vulkan memory object exported using `VK_EXTERNAL_MEMORY_HANDLE_TYPE_OPAQUE_FD_BIT` can be imported into CUDA using the associated file descriptor [CUDA_C_Programming_Guide:L4528-L4737].

*   **Ownership:** CUDA assumes ownership of the file descriptor once it is imported [CUDA_C_Programming_Guide:L4528-L4737].
*   **Usage Constraint:** Using the file descriptor after a successful import results in undefined behavior [CUDA_C_Programming_Guide:L4528-L4737].

#### Opaque Win32 (Windows)

A Vulkan memory object exported using `VK_EXTERNAL_MEMORY_HANDLE_TYPE_OPAQUE_WIN32_BIT` can be imported using an NT handle or a named handle [CUDA_C_Programming_Guide:L4528-L4737].

*   **NT Handle:**
    *   **Ownership:** CUDA does not assume ownership of the NT handle; the application is responsible for closing the handle when it is no longer required [CUDA_C_Programming_Guide:L4528-L4737].
    *   **Lifecycle:** The NT handle holds a reference to the resource, so it must be explicitly freed before the underlying memory can be freed [CUDA_C_Programming_Guide:L4528-L4737].
*   **Named Handle:**
    *   Imported using the `LPCWSTR` name associated with the handle [CUDA_C_Programming_Guide:L4528-L4737].

#### Opaque Win32 KMT (Windows)

A Vulkan memory object exported using `VK_EXTERNAL_MEMORY_HANDLE_TYPE_OPAQUE_WIN32_KMT_BIT` can be imported using the globally shared D3DKMT handle [CUDA_C_Programming_Guide:L4528-L4737].

*   **Lifecycle:** A globally shared D3DKMT handle does not hold a reference to the underlying memory; it is automatically destroyed when all other references to the resource are destroyed [CUDA_C_Programming_Guide:L4528-L4737].

## Mapping Memory Objects

Once a Vulkan memory object is imported into CUDA as an external memory object (`cudaExternalMemory_t`), it can be mapped to CUDA resources such as buffers or mipmapped arrays [CUDA_C_Programming_Guide:L4528-L4737].

### Mapping Buffers

A device pointer can be mapped onto an imported memory object using `cudaExternalMemoryGetMappedBuffer` [CUDA_C_Programming_Guide:L4528-L4737].

*   **Constraints:** The offset and size of the mapping must match those specified when creating the mapping in the corresponding Vulkan API [CUDA_C_Programming_Guide:L4528-L4737].
*   **Cleanup:** All mapped device pointers must be freed using `cudaFree()` [CUDA_C_Programming_Guide:L4528-L4737].

### Mapping Mipmapped Arrays

A CUDA mipmapped array can be mapped onto an imported memory object using `cudaExternalMemoryGetMappedMipmappedArray` [CUDA_C_Programming_Guide:L4528-L4737].

*   **Constraints:** The offset, dimensions, format, and number of mip levels must match those specified when creating the mapping in the corresponding Vulkan API [CUDA_C_Programming_Guide:L4528-L4737].
*   **Color Attachment:** If the mipmapped array is bound as a color target in Vulkan, the `cudaArrayColorAttachment` flag must be set [CUDA_C_Programming_Guide:L4528-L4737].
*   **Cleanup:** All mapped mipmapped arrays must be freed using `cudaFreeMipmappedArray()` [CUDA_C_Programming_Guide:L4528-L4737].

Vulkan format codes can be converted to CUDA channel format descriptions (`cudaChannelFormatDesc`) to facilitate this mapping [CUDA_C_Programming_Guide:L4528-L4737].
