# Fabric Memory

Introduces CU_MEM_HANDLE_TYPE_FABRIC for intra-node and inter-node memory sharing via NVIDIA IMEX daemon and NVLINK fabric.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L15231-L15255

Citation: [CUDA_C_Programming_Guide:L15231-L15255]

````text
## 14.8. Fabric Memory

CUDA 12.4 introduced a new VMM allocation handle type CU\_MEM\_HANDLE\_TYPE\_FABRIC. On supported platforms and provided the NVIDIA IMEX daemon is running this allocation handle type enables sharing allocations not only intra node with any communication mechanism, e.g. MPI, but also inter node. This allows GPUs in a Multi Node NVLINK System to map the memory of all other GPUs part of the same NVLINK fabric even if they are in diferent nodes greatly increasing the scale of multi-GPU Programming with NVLINK.

## 14.8.1. Query for Support

Before attempting to use Fabric Memory, applications must ensure that the devices they want to use support Fabric Memory. The following code sample shows querying for Fabric Memory support:

```txt
int deviceSupportsFabricMem;
CUresult result = cuDeviceGetAttribute(&deviceSupportsFabricMem, CU_DEVICE_ATTRIBUTE_HANDLE_TYPE_FABRIC_SUPPORTED, device);
if (deviceSupportsFabricMem != 0) {
```

(continues on next page)

(continued from previous page)

```txt
// `device` supports Fabric Memory
}
```

Aside from using CU\_MEM\_HANDLE\_TYPE\_FABRIC as handle type and not requiring OS native mechanisms for inter process communication to exchange sharable handles there is no diference in using Fabric Memory compared to other allocation handle types.
````
