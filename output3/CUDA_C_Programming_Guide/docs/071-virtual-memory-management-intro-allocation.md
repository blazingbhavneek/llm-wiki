
Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

## 14.1. Introduction

The Virtual Memory Management APIs provide a way for the application to directly manage the unified virtual address space that CUDA provides to map physical memory to virtual addresses accessible by the GPU. Introduced in CUDA 10.2, these APIs additionally provide a new way to interop with other processes and graphics APIs like OpenGL and Vulkan, as well as provide newer memory attributes that a user can tune to fit their applications.

Historically, memory allocation calls (such as cudaMalloc()) in the CUDA programming model have returned a memory address that points to the GPU memory. The address thus obtained could be used with any CUDA API or inside a device kernel. However, the memory allocated could not be resized depending on the user’s memory needs. In order to increase an allocation’s size, the user had to explicitly allocate a larger bufer, copy data from the initial allocation, free it and then continue to keep track of the newer allocation’s address. This often leads to lower performance and higher peak memory utilization for applications. Essentially, users had a malloc-like interface for allocating GPU memory, but did not have a corresponding realloc to complement it. The Virtual Memory Management APIs decouple the idea of an address and memory and allow the application to handle them separately. The APIs allow applications to map and unmap memory from a virtual address range as they see fit.

In the case of enabling peer device access to memory allocations by using cudaEnablePeerAccess, all past and future user allocations are mapped to the target peer device. This lead to users unwittingly paying runtime cost of mapping all cudaMalloc allocations to peer devices. However, in most situations applications communicate by sharing only a few allocations with another device and not all allocations are required to be mapped to all the devices. With Virtual Memory Management, applications can specifically choose certain allocations to be accessible from target devices.

The CUDA Virtual Memory Management APIs expose fine grained control to the user for managing the GPU memory in applications. It provides APIs that let users:

▶ Place memory allocated on diferent devices into a contiguous VA range.

▶ Perform interprocess communication for memory sharing using platform-specific mechanisms.

▶ Opt into newer memory types on the devices that support them.

In order to allocate memory, the Virtual Memory Management programming model exposes the following functionality:

▶ Allocating physical memory.

▶ Reserving a VA range.

▶ Mapping allocated memory to the VA range.

▶ Controlling access rights on the mapped range.

Note that the suite of APIs described in this section require a system that supports UVA.

## 14.2. Query for Support

Before attempting to use Virtual Memory Management APIs, applications must ensure that the devices they want to use support CUDA Virtual Memory Management. The following code sample shows querying for Virtual Memory Management support:

```c
int deviceSupportsVmm;
CUresult result = cuDeviceGetAttribute(&deviceSupportsVmm, CU_DEVICE_ATTRIBUTE_
    VIRTUAL_MEMORY_MANAGEMENT_SUPPORTED, device);
if (deviceSupportsVmm != 0) {
    // `device` supports Virtual Memory Management
}
```

## 14.3. Allocating Physical Memory

The first step in memory allocation using Virtual Memory Management APIs is to create a physical memory chunk that will provide a backing for the allocation. In order to allocate physical memory, applications must use the cuMemCreate API. The allocation created by this function does not have any device or host mappings. The function argument CUmemGenericAllocationHandle describes the properties of the memory to allocate such as the location of the allocation, if the allocation is going to be shared to another process (or other Graphics APIs), or the physical attributes of the memory to be allocated. Users must ensure the requested allocation’s size must be aligned to appropriate granularity. Information regarding an allocation’s granularity requirements can be queried using cuMemGetAllocationGranularity. The following code snippet shows allocating physical memory with cuMemCreate:

```txt
CUmemGenericAllocationHandle allocatePhysicalMemory(int device, size_t size) {
    CUmemAllocationProp prop = {};
    prop.type = CU_MEM_ALLOCATION_TYPE_PINNED;
    prop.location.type = CU_MEM_LOCATION_TYPE_DEVICE;
    prop.location.id = device;

    size_t granularity = 0;
    cuMemGetAllocationGranularity(&granularity, &prop, CU_MEM_ALLOC_GRANULARITY_MINIMUM);

    // Ensure size matches granularity requirements for the allocation
    size_t padded_size = ROUND_UP(size, granularity);
```

(continues on next page)

```txt
// Allocate physical memory
CUmemGenericAllocationHandle allocHandle;
cuMemCreate(&allocHandle, padded_size, &prop, 0);

return allocHandle;
}
```

The memory allocated by cuMemCreate is referenced by the CUmemGenericAllocationHandle it returns. This is a departure from the cudaMalloc-style of allocation, which returns a pointer to the GPU memory, which was directly accessible by CUDA kernel executing on the device. The memory allocated cannot be used for any operations other than querying properties using cuMemGetAllocationPropertiesFromHandle. In order to make this memory accessible, applications must map this memory into a VA range reserved by cuMemAddressReserve and provide suitable access rights to it. Applications must free the allocated memory using the cuMemRelease API.

## 14.3.1. Shareable Memory Allocations

With cuMemCreate users now have the facility to indicate to CUDA, at allocation time, that they have earmarked a particular allocation for Inter process communication and graphics interop purposes. Applications can do this by setting CUmemAllocationProp::requestedHandleTypes to a platform-specific field. On Windows, when CUmemAllocationProp::requestedHandleTypes is set to CU\_MEM\_HANDLE\_TYPE\_WIN32 applications must also specify an LPSECURITYATTRIBUTES attribute in CUmemAllocationProp::win32HandleMetaData. This security attribute defines the scope of which exported allocations may be transferred to other processes.

The CUDA Virtual Memory Management API functions do not support the legacy interprocess communication functions with their memory. Instead, they expose a new mechanism for interprocess communication that uses OS-specific handles. Applications can obtain these OS-specific handles corresponding to the allocations by using cuMemExportToShareableHandle. The handles thus obtained can be transferred by using the usual OS native mechanisms for inter process communication. The recipient process should import the allocation by using cuMemImportFromShareableHandle.

Users must ensure they query for support of the requested handle type before attempting to export memory allocated with cuMemCreate. The following code snippet illustrates query for handle type support in a platform-specific way.

```cpp
int deviceSupportsIpcHandle;
#if defined(__linux__)
    cuDeviceGetAttribute(&deviceSupportsIpcHandle, CU_DEVICE_ATTRIBUTE_HANDLE_TYPE_POSIX_FILE_DESCRIPTOR_SUPPORTED, device));
#else
    cuDeviceGetAttribute(&deviceSupportsIpcHandle, CU_DEVICE_ATTRIBUTE_HANDLE_TYPE_WIN32_HANDLE_SUPPORTED, device));
#endif
```

Users should set the CUmemAllocationProp::requestedHandleTypes appropriately as shown below:

```txt
#if defined(__linux__)
    prop.requiredHandleTypes = CU_MEM_HANDLE_TYPE_POSIX_FILE_DESCRIPTOR;
#else
    prop.requiredHandleTypes = CU_MEM_HANDLE_TYPE_WIN32;
```

(continues on next page)

```cpp
(continued from previous page)
    prop.win32HandleMetaData = // Windows specific LPSECURITYATTRIBUTES attribute.
#endif
```

The memMapIpcDrv sample can be used as an example for using IPC with Virtual Memory Management allocations.

## 14.3.2. Memory Type

Before CUDA 10.2, applications had no user-controlled way of allocating any special type of memory that certain devices may support. With cuMemCreate, applications can additionally specify memory type requirements using the CUmemAllocationProp::allocFlags to opt into any specific memory features. Applications must also ensure that the requested memory type is supported on the device of allocation.

## 14.3.2.1 Compressible Memory

Compressible memory can be used to accelerate accesses to data with unstructured sparsity and other compressible data patterns. Compression can save DRAM bandwidth, L2 read bandwidth and L2 capacity depending on the data being operated on. Applications that want to allocate compressible memory on devices that support Compute Data Compression can do so by setting CUmemAllocationProp::allocFlags::compressionType to CU\_MEM\_ALLOCATION\_COMP\_GENERIC. Users must query if device supports Compute Data Compression by using CU\_DEVICE\_ATTRIBUTE\_GENERIC\_COMPRESSION\_SUPPORTED. The following code snippet illustrates querying compressible memory support cuDeviceGetAttribute.

```txt
int compressionSupported = 0;
cuDeviceGetAttribute(&compressionSupported, CU_DEVICE_ATTRIBUTE_GENERIC_COMPRESSION_
→SUPPORTED, device);
```

On devices that support Compute Data Compression, users must opt in at allocation time as shown below:

```javascript
prop.allocFlags.compressionType = CU_MEM_ALLOCATION_COMP_GENERIC;
```

Due to various reasons such as limited HW resources, the allocation may not have compression attributes, the user is expected to query back the properties of the allocated memory using cuMemGetAllocationPropertiesFromHandle and check for compression attribute.

```javascript
CUmemAllocationProp allocationProp = {};
cuMemGetAllocationPropertiesFromHandle(&allocationProp, allocationHandle);

if (allocationProp.allocFlags.compressionType == CU_MEM_ALLOCATION_COMP_GENERIC)
{
    // Obtained compressible memory allocation
}
```
