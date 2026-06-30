# Reserving a Virtual Address Range

Explains cuMemAddressReserve for carving out virtual address space independent of physical memory, analogous to mmap/VirtualAlloc.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L15129-L15141

Citation: [CUDA_C_Programming_Guide:L15129-L15141]

````text
## 14.4. Reserving a Virtual Address Range

Since with Virtual Memory Management the notions of address and memory are distinct, applications must carve out an address range that can hold the memory allocations made by cuMemCreate. The address range reserved must be at least as large as the sum of the sizes of all the physical memory allocations the user plans to place in them.

Applications can reserve a virtual address range by passing appropriate parameters to cuMemAddressReserve. The address range obtained will not have any device or host physical memory associated with it. The reserved virtual address range can be mapped to memory chunks belonging to any device in the system, thus providing the application a continuous VA range backed and mapped by memory belonging to diferent devices. Applications are expected to return the virtual address range back to CUDA using cuMemAddressFree. Users must ensure that the entire VA range is unmapped before calling cuMemAddressFree. These functions are conceptually similar to mmap/munmap (on Linux) or VirtualAlloc/VirtualFree (on Windows) functions. The following code snippet illustrates the usage for the function:

```txt
CUdeviceptr ptr;
// `ptr` holds the returned start of virtual address range reserved.
CUresult result = cuMemAddressReserve(&ptr, size, 0, 0, 0); // alignment = 0 for
    default alignment
```
````
