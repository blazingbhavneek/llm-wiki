# EGM: Multi-Node, Single-GPU

## Overview

In a multi-node, single-GPU configuration, the CUDA Extensible Graphics Memory (EGM) API allows for memory allocation and access across different nodes. Beyond the specific memory allocation steps, remote peer access in this context does not require EGM-specific modifications and adheres to the standard CUDA Inter-Process Communication (IPC) protocol [CUDA_C_Programming_Guide:L22331-L22331].

## Memory Allocation and Sharing

To enable multi-node access, physical memory must be allocated on a specific node (e.g., Node A) using the EGM API, specifically `cuMemCreate`. The allocation must be configured with specific properties to ensure compatibility with remote nodes.

### Prerequisites and Configuration

1.  **Location Type**: The user must explicitly provide `CU_MEM_LOCATION_TYPE_HOST_NUMA` as the location type [CUDA_C_Programming_Guide:L22333-L22333].
2.  **Location Identifier**: The `numaID` must be provided as the location identifier to specify the exact NUMA node where the memory resides [CUDA_C_Programming_Guide:L22333-L22333] [CUDA_C_Programming_Guide:L22340-L22340].
3.  **Handle Type**: The requested handle type must be defined as `CU_MEM_HANDLE_TYPE_FABRIC` [CUDA_C_Programming_Guide:L22333-L22333] [CUDA_C_Programming_Guide:L22337-L22338].

### Implementation Steps

The following steps outline the process for allocating memory on Node A and exporting it for use on Node B.

#### 1. Configure Allocation Properties

Define the allocation properties to specify pinned memory and fabric handle requirements [CUDA_C_Programming_Guide:L22337-L22338]:

```c
prop.type = CU_MEM_ALLOCATION_TYPE_PINNED;
prop.requestedHandleTypes = CU_MEM_HANDLE_TYPE_FABRIC;
prop.location.id = numaId;
```

#### 2. Determine Granularity and Size

Query the minimum allocation granularity required for the properties and calculate the padded size to ensure it meets page size alignment requirements [CUDA_C_Programming_Guide:L22342-L22346]:

```c
cuMemGetAllocationGranularity(&granularity, &prop, MEM_ALLOC_GRANULARITY_MINIMUM);
size_t padded_size = ROUND_UP(size, granularity);
size_t page_size = ...;
assert(padded_size % page_size == 0);
```

#### 3. Create the Allocation

Allocate the memory on Node A using the calculated properties [CUDA_C_Programming_Guide:L22348-L22348]:

```c
cuMemCreate(&allocHandle, padded_size, &prop, 0);
```

#### 4. Export the Handle

Export the allocation handle to a shareable fabric handle, which can then be transmitted to the remote node (Node B) via a communication channel such as TCP/IP [CUDA_C_Programming_Guide:L22354-L22363]:

```c
cuMemExportToShareableHandle(&fabricHandle, allocHandle, CU_MEM_HANDLE_TYPE_FABRIC, 0);
// At this point, fabricHandle should be sent to Node B via TCP/IP.
```

#### 5. Import on Remote Node

On Node B, the received fabric handle is imported back into an EGM allocation handle using `cuMemImportFromShareableHandle`. Once imported, it is treated as any other fabric handle, allowing the GPU on Node B to access the memory allocated on Node A [CUDA_C_Programming_Guide:L22354-L22363]:

```c
// At this point, fabricHandle should be received from Node A via TCP/IP.
CUMemGenericAllocationHandle allocHandle;
cuMemImportFromShareableHandle(&allocHandle, fabricHandle, CU_MEM_HANDLE_TYPE_FABRIC);
```

## Caveats

*   This configuration relies on the underlying IPC protocol for remote peer access mechanisms beyond the initial memory allocation [CUDA_C_Programming_Guide:L22331-L22331].
*   The fabric handle must be successfully transmitted between nodes (e.g., via TCP/IP) to enable the import process on the remote node [CUDA_C_Programming_Guide:L22354-L22363].
