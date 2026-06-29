# Reserving a Virtual Address Range

In CUDA Virtual Memory Management, the notions of address and memory are distinct. Applications must explicitly carve out a virtual address range that can hold the memory allocations made via `cuMemCreate`.

## Reservation

Applications reserve a virtual address range by passing appropriate parameters to the `cuMemAddressReserve` function. The reserved address range must be at least as large as the sum of the sizes of all physical memory allocations the user plans to place within it.

Upon reservation, the obtained address range does not have any device or host physical memory associated with it. The following code snippet illustrates the usage:

```txt
CUdeviceptr ptr;
// `ptr` holds the returned start of virtual address range reserved.
CUresult result = cuMemAddressReserve(&ptr, size, 0, 0, 0); // alignment = 0 for default alignment
```

## Mapping and Unmapping

The reserved virtual address range can be mapped to memory chunks belonging to any device in the system. This capability allows the application to maintain a continuous virtual address (VA) range that is backed and mapped by memory belonging to different devices.

Applications are expected to return the virtual address range back to CUDA using `cuMemAddressFree`. Users must ensure that the entire VA range is unmapped before calling `cuMemAddressFree`.

## Conceptual Similarity

These functions are conceptually similar to `mmap`/`munmap` (on Linux) or `VirtualAlloc`/`VirtualFree` (on Windows) functions.

[cuda:CUDA_C_Programming_Guide:L15129-L15141]
