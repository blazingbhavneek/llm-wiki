# EGM: Using VMM APIs

## Overview

The first step in memory allocation using Virtual Memory Management APIs is to create a physical memory chunk that will provide a backing for the allocation [CUDA_C_Programming_Guide:L22262-L22262]. In the context of Explicit Global Memory (EGM), specific constraints apply to location types and alignment granularity [CUDA_C_Programming_Guide:L22262-L22262].

## Physical Memory Allocation

For EGM allocations, the user must explicitly provide `CU_MEM_LOCATION_TYPE_HOST_NUMA` as the location type and `numaId` as the location identifier [CUDA_C_Programming_Guide:L22262-L22262]. Additionally, allocations must be aligned to the appropriate granularity of the platform [CUDA_C_Programming_Guide:L22262-L22262].

The following code snippet demonstrates allocating physical memory using `cuMemCreate`:

```txt
CUmemAllocationProp prop{
prop.type = CU_MEM_ALLOCATION_TYPE_PINNED;
prop.location.type = CU_MEM_LOCATION_TYPE_HOST_NUMA;
prop.location.id = numaId;
size_t granularity = 0;
cuMemGetAllocationGranularity(&granularity, &prop, MEM_ALLOC_GRANULARITY_MINIMUM);
size_t padded_size = ROUND_UP(size, granularity);
CUmemGenericAllocationHandle allocHandle;
cuMemCreate(&allocHandle, padded_size, &prop, 0);
```

## Address Space Reservation and Mapping

After physical memory allocation, the user must reserve an address space and map it to a pointer [CUDA_C_Programming_Guide:L22276-L22276]. These procedures do not have EGM-specific changes compared to standard VMM usage [CUDA_C_Programming_Guide:L22276-L22276].

```txt
CUdeviceptr dptr;
cuMemAddressReserve(&dptr, padded_size, 0, 0, 0);
cuMemMap(dptr, padded_size, 0, allocHandle, 0);
```

## Access Protection

Finally, the user has to explicitly protect mapped virtual address ranges; otherwise, access to the mapped space would result in a crash [CUDA_C_Programming_Guide:L22284-L22284]. Similar to the memory allocation step, the user must provide `CU_MEM_LOCATION_TYPE_HOST_NUMA` as the location type and `numaId` as the location identifier for the host side [CUDA_C_Programming_Guide:L22284-L22284].

The following code snippet creates access descriptors for both the host node and the GPU, granting read and write access to the mapped memory for both entities:

```javascript
CUmemAccessDesc accessDesc[2]{{}};
accessDesc[0].location.type = CU_MEM_LOCATION_TYPE_HOST_NUMA;
accessDesc[0].location.id = numaId;
accessDesc[0].flags = CU_MEM_ACCESS_FLAGS_PROT_READWRITE;
accessDesc[1].location.type = CU_MEM_LOCATION_TYPE_DEVICE;
accessDesc[1].location.id = currentDev;
accessDesc[1].flags = CU_MEM_ACCESS_FLAGS_PROT_READWRITE;
cuMemSetAccess(dptr, size, accessDesc, 2);
```
