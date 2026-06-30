# Unified Virtual Address Space

In 64-bit processes, a single address space covers the host and all devices (compute capability 2.0+). Pointers can be queried for location using cudaPointerGetAttributes(), and cudaMemcpyDefault can be used for transfers. cudaHostAlloc() creates portable memory accessible directly by kernels without explicit device pointer conversion.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3598-L3609

Citation: [CUDA_C_Programming_Guide:L3598-L3609]

````text
## 6.2.10. Unified Virtual Address Space

When the application is run as a 64-bit process, a single address space is used for the host and all the devices of compute capability 2.0 and higher. All host memory allocations made via CUDA API calls and all device memory allocations on supported devices are within this virtual address range. As a consequence:

▶ The location of any memory on the host allocated through CUDA, or on any of the devices which use the unified address space, can be determined from the value of the pointer using cuda-PointerGetAttributes().

When copying to or from the memory of any device which uses the unified address space, the cudaMemcpyKind parameter of cudaMemcpy\*() can be set to cudaMemcpyDefault to determine locations from the pointers. This also works for host pointers not allocated through CUDA, as long as the current device uses unified addressing.

Allocations via cudaHostAlloc() are automatically portable (see Portable Memory) across all the devices for which the unified address space is used, and pointers returned by cudaHostAlloc() can be used directly from within kernels running on these devices (i.e., there is no need to obtain a device pointer via cudaHostGetDevicePointer() as described in Mapped Memory.

Applications may query if the unified address space is used for a particular device by checking that the unifiedAddressing device property (see Device Enumeration) is equal to 1.
````
