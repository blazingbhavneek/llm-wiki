# Page-Locked Host Memory

Page-locked host memory (also known as pinned host memory) is a memory allocation type provided by the CUDA runtime that offers several performance advantages over regular pageable host memory (allocated by `malloc()`). Unlike pageable memory, page-locked memory cannot be swapped out to disk by the operating system, allowing the GPU to access it directly.

## Allocation and Deallocation

Page-locked host memory can be managed using the following CUDA runtime functions:

*   **`cudaHostAlloc()`**: Allocates new page-locked host memory. The corresponding deallocation function is `cudaFreeHost()`.
*   **`cudaHostRegister()`**: Locks a range of memory that was previously allocated by `malloc()`. Note that there are limitations on the use of this function; refer to the CUDA Reference Manual for details.

## Benefits

Using page-locked host memory provides several key benefits:

1.  **Concurrent Execution**: On some devices, copies between page-locked host memory and device memory can be performed concurrently with kernel execution [CUDA_C_Programming_Guide:L1972-L1994].
2.  **Mapped Memory (Zero-Copy)**: On some devices, page-locked host memory can be mapped into the device's address space. This eliminates the need to explicitly copy data to or from device memory, allowing kernels to access host memory directly [CUDA_C_Programming_Guide:L1972-L1994].
3.  **Higher Bandwidth**: On systems with a front-side bus, bandwidth between host and device memory is higher when host memory is page-locked. This bandwidth can be further increased if the memory is also allocated as write-combining [CUDA_C_Programming_Guide:L1972-L1994].

### Portable Memory

By default, the benefits of page-locked memory (such as concurrent copies and mapped access) are only available in conjunction with the device that was current at the time of allocation, and with all devices sharing the same unified address space [CUDA_C_Programming_Guide:L1972-L1994].

To make these advantages available to all devices in a multi-device system, the memory must be allocated as **portable**:
*   Pass the flag `cudaHostAllocPortable` to `cudaHostAlloc()`.
*   Pass the flag `cudaHostRegisterPortable` to `cudaHostRegister()`.

## Write-Combining Memory

By default, page-locked host memory is allocated as cacheable. It can optionally be allocated as **write-combining** by passing the flag `cudaHostAllocWriteCombined` to `cudaHostAlloc()` [CUDA_C_Programming_Guide:L1995-L2003].

### Characteristics and Use Cases

*   **Cache Resources**: Write-combining memory frees up the host’s L1 and L2 cache resources, making more cache available to the rest of the application [CUDA_C_Programming_Guide:L1995-L2003].
*   **Performance**: Write-combining memory is not snooped during transfers across the PCI Express bus, which can improve transfer performance by up to 40% [CUDA_C_Programming_Guide:L1995-L2003].
*   **Read Performance**: Reading from write-combining memory from the host is prohibitively slow. Therefore, write-combining memory should generally be used for memory that the host only writes to [CUDA_C_Programming_Guide:L1995-L2003].
*   **Atomic Instructions**: Using CPU atomic instructions on write-combining memory should be avoided because not all CPU implementations guarantee this functionality [CUDA_C_Programming_Guide:L1995-L2003].

## Mapped Memory

A block of page-locked host memory can be mapped into the address space of the device by passing the flag `cudaHostAllocMapped` to `cudaHostAlloc()` or `cudaHostRegisterMapped` to `cudaHostRegister()` [CUDA_C_Programming_Guide:L2004-L2023].

### Accessing Mapped Memory

Mapped memory generally has two addresses:
1.  A host address returned by `cudaHostAlloc()` or `malloc()`.
2.  A device address retrieved using `cudaHostGetDevicePointer()`, which can be used to access the block from within a kernel [CUDA_C_Programming_Guide:L2004-L2023].

**Exception**: If a unified address space is used for the host and device, and the pointer was allocated with `cudaHostAlloc()`, the host and device addresses may be identical [CUDA_C_Programming_Guide:L2004-L2023].

### Advantages of Mapped Memory

*   **Implicit Data Transfer**: There is no need to allocate device memory or explicitly copy data between host and device blocks. Data transfers are implicitly performed as needed by the kernel [CUDA_C_Programming_Guide:L2004-L2023].
*   **Automatic Overlap**: There is no need to use streams to overlap data transfers with kernel execution; the kernel-originated data transfers automatically overlap with kernel execution [CUDA_C_Programming_Guide:L2004-L2023].

### Requirements and Limitations

*   **Enable Mapping**: To retrieve the device pointer using `cudaHostGetDevicePointer()`, page-locked memory mapping must be enabled by calling `cudaSetDeviceFlags()` with the `cudaDeviceMapHost` flag before any other CUDA call is performed. Otherwise, `cudaHostGetDevicePointer()` will return an error [CUDA_C_Programming_Guide:L2004-L2023].
*   **Device Support**: `cudaHostGetDevicePointer()` returns an error if the device does not support mapped page-locked host memory. Applications can query this capability by checking the `canMapHostMemory` device property, which is equal to 1 for supported devices [CUDA_C_Programming_Guide:L2004-L2023].
*   **Synchronization**: Since mapped page-locked memory is shared between host and device, the application must synchronize memory accesses using streams or events to avoid read-after-write, write-after-read, or write-after-write hazards [CUDA_C_Programming_Guide:L2004-L2023].
*   **Atomic Operations**: Atomic functions operating on mapped page-locked memory are not atomic from the point of view of the host or other devices [CUDA_C_Programming_Guide:L2004-L2023].
*   **Alignment Requirements**: The CUDA runtime requires that 1-byte, 2-byte, 4-byte, 8-byte, and 16-byte naturally aligned loads and stores to host memory initiated from the device are preserved as single accesses from the perspective of the host and other devices. On some platforms, atomics may be broken into separate load and store operations, which also require naturally aligned accesses [CUDA_C_Programming_Guide:L2004-L2023].

## Platform-Specific Notes

*   **Tegra Devices**: Page-locked host memory is not cached on non-I/O coherent Tegra devices. Additionally, `cudaHostRegister()` is not supported on non-I/O coherent Tegra devices [CUDA_C_Programming_Guide:L1972-L1994].

## See Also

*   [Asynchronous Concurrent Execution](concept/asynchronous-concurrent-execution)
*   [Mapped Memory](concept/mapped-memory)
*   [Write-Combining Memory](concept/write-combining-memory)
*   [Portable Memory](concept/portable-memory)
*   [Unified Virtual Address Space](concept/unified-virtual-address-space)
*   [Concurrent Data Transfers](concept/concurrent-data-transfers)
*   [Device Enumeration](concept/device-enumeration)
*   [Atomic Functions](concept/atomic-functions)

The simple zero-copy CUDA sample comes with a detailed document on the page-locked memory APIs.
