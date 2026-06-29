# Mapping Memory

The Virtual Memory Management APIs in CUDA introduce a distinction between physical memory and virtual address space. This separation allows for flexible memory management where allocated physical memory and carved-out virtual address ranges are handled independently.

## Associating Physical Memory with Virtual Address Space

For allocated physical memory to be usable, it must first be placed into the virtual address space. This is achieved by associating an address range, obtained via `cuMemAddressReserve`, with a physical allocation obtained from `cuMemCreate` or `cuMemImportFromShareableHandle` using the `cuMemMap` function [CUDA_C_Programming_Guide:L15197-L15210].

### Mapping Syntax

The `cuMemMap` function takes a device pointer representing an address within the previously reserved range, the size of the mapping, and the generic allocation handle. The following code snippet illustrates the basic usage:

```javascript
CUdeviceptr ptr;
// `ptr`: address in the address range previously reserved by cuMemAddressReserve.
// `allocHandle`: CUmemGenericAllocationHandle obtained by a previous call to
    →cuMemCreate.
CUresult result = cuMemMap(ptr, size, 0, allocHandle, 0);
```

## Multiple Devices and Contiguous Ranges

Users can associate allocations from multiple devices to reside in contiguous virtual address ranges, provided that sufficient address space has been carved out [CUDA_C_Programming_Guide:L15197-L15210].

## Unmapping and Remapping

To decouple a physical allocation from a virtual address range, users must unmap the address using `cuMemUnmap` [CUDA_C_Programming_Guide:L15197-L15210]. 

Memory can be mapped and unmapped to the same virtual address range multiple times. However, users must ensure that they do not attempt to create mappings on virtual address range reservations that are already mapped [CUDA_C_Programming_Guide:L15197-L15210].
