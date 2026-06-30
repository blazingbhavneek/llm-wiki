# Mapping Memory

Details cuMemMap to associate physical allocations with reserved virtual address ranges, and cuMemUnmap for decoupling.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L15197-L15210

Citation: [CUDA_C_Programming_Guide:L15197-L15210]

````text
## 14.6. Mapping Memory

The allocated physical memory and the carved out virtual address space from the previous two sections represent the memory and address distinction introduced by the Virtual Memory Management APIs. For the allocated memory to be useable, the user must first place the memory in the address space. The address range obtained from cuMemAddressReserve and the physical allocation obtained from cuMemCreate or cuMemImportFromShareableHandle must be associated with each other by using cuMemMap.

Users can associate allocations from multiple devices to reside in contiguous virtual address ranges as long as they have carved out enough address space. In order to decouple the physical allocation and the address range, users must unmap the address of the mapping by using cuMemUnmap. Users can map and unmap memory to the same address range as many times as they want, as long as they ensure that they don’t attempt to create mappings on VA range reservations that are already mapped. The following code snippet illustrates the usage for the function:

```javascript
CUdeviceptr ptr;
// `ptr`: address in the address range previously reserved by cuMemAddressReserve.
// `allocHandle`: CUmemGenericAllocationHandle obtained by a previous call to
    →cuMemCreate.
CUresult result = cuMemMap(ptr, size, 0, allocHandle, 0);
```
````
