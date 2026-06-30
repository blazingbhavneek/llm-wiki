# Page-Locked Host Memory

Host memory allocated with cudaHostAlloc or cudaHostRegister that prevents paging, enabling concurrent transfers, device mapping, and higher bandwidth. Includes portable, write-combining, and mapped memory variants.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L1972-L2023

Citation: [CUDA_C_Programming_Guide:L1972-L2023]

````text
## 6.2.6. Page-Locked Host Memory

The runtime provides functions to allow the use of page-locked (also known as pinned) host memory (as opposed to regular pageable host memory allocated by malloc()):

▶ cudaHostAlloc() and cudaFreeHost() allocate and free page-locked host memory;

cudaHostRegister() page-locks a range of memory allocated by malloc() (see reference manual for limitations).

Using page-locked host memory has several benefits:

Copies between page-locked host memory and device memory can be performed concurrently with kernel execution for some devices as mentioned in Asynchronous Concurrent Execution.

▶ On some devices, page-locked host memory can be mapped into the address space of the device, eliminating the need to copy it to or from device memory as detailed in Mapped Memory.

On systems with a front-side bus, bandwidth between host memory and device memory is higher if host memory is allocated as page-locked and even higher if in addition it is allocated as writecombining as described in Write-Combining Memory.

Note: Page-locked host memory is not cached on non I/O coherent Tegra devices. Also, cuda-HostRegister() is not supported on non I/O coherent Tegra devices.

The simple zero-copy CUDA sample comes with a detailed document on the page-locked memory APIs.

## 6.2.6.1 Portable Memory

A block of page-locked memory can be used in conjunction with any device in the system (see Multi-Device System for more details on multi-device systems), but by default, the benefits of using pagelocked memory described above are only available in conjunction with the device that was current when the block was allocated (and with all devices sharing the same unified address space, if any, as described in Unified Virtual Address Space). To make these advantages available to all devices, the block needs to be allocated by passing the flag cudaHostAllocPortable to cudaHostAlloc() or page-locked by passing the flag cudaHostRegisterPortable to cudaHostRegister().

## 6.2.6.2 Write-Combining Memory

By default page-locked host memory is allocated as cacheable. It can optionally be allocated as writecombining instead by passing flag cudaHostAllocWriteCombined to cudaHostAlloc(). Writecombining memory frees up the host’s L1 and L2 cache resources, making more cache available to the rest of the application. In addition, write-combining memory is not snooped during transfers across the PCI Express bus, which can improve transfer performance by up to 40%.

Reading from write-combining memory from the host is prohibitively slow, so write-combining memory should in general be used for memory that the host only writes to.

Using CPU atomic instructions on WC memory should be avoided because not all CPU implementations guarantee that functionality.

## 6.2.6.3 Mapped Memory

A block of page-locked host memory can also be mapped into the address space of the device by passing flag cudaHostAllocMapped to cudaHostAlloc() or by passing flag cudaHostRegisterMapped to cudaHostRegister(). Such a block has therefore in general two addresses: one in host memory that is returned by cudaHostAlloc() or malloc(), and one in device memory that can be retrieved using cudaHostGetDevicePointer() and then used to access the block from within a kernel. The only exception is for pointers allocated with cudaHostAlloc() and when a unified address space is used for the host and the device as mentioned in Unified Virtual Address Space.

Accessing host memory directly from within a kernel does not provide the same bandwidth as device memory, but does have some advantages:

There is no need to allocate a block in device memory and copy data between this block and the block in host memory; data transfers are implicitly performed as needed by the kernel;

▶ There is no need to use streams (see Concurrent Data Transfers) to overlap data transfers with kernel execution; the kernel-originated data transfers automatically overlap with kernel execution.

Since mapped page-locked memory is shared between host and device however, the application must synchronize memory accesses using streams or events (see Asynchronous Concurrent Execution) to avoid any potential read-after-write, write-after-read, or write-after-write hazards.

To be able to retrieve the device pointer to any mapped page-locked memory, page-locked memory mapping must be enabled by calling cudaSetDeviceFlags() with the cudaDeviceMapHost flag before any other CUDA call is performed. Otherwise, cudaHostGetDevicePointer() will return an error.

cudaHostGetDevicePointer() also returns an error if the device does not support mapped pagelocked host memory. Applications may query this capability by checking the canMapHostMemory device property (see Device Enumeration), which is equal to 1 for devices that support mapped pagelocked host memory.

Note that atomic functions (see Atomic Functions) operating on mapped page-locked memory are not atomic from the point of view of the host or other devices.

Also note that CUDA runtime requires that 1-byte, 2-byte, 4-byte, 8-byte, and 16-byte naturally aligned loads and stores to host memory initiated from the device are preserved as single accesses from the point of view of the host and other devices. On some platforms, atomics to memory may be broken by the hardware into separate load and store operations. These component load and store operations have the same requirements on preservation of naturally aligned accesses. The CUDA runtime does not support a PCI Express bus topology where a PCI Express bridge splits 8-byte naturally aligned operations and NVIDIA is not aware of any topology that splits 16-byte naturally aligned operations.
````
