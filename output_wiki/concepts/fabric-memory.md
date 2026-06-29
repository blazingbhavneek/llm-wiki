# Fabric Memory

Fabric Memory is a feature introduced in CUDA 12.4 that provides a new Virtual Memory Management (VMM) allocation handle type, `CU_MEM_HANDLE_TYPE_FABRIC` [CUDA_C_Programming_Guide:L15231-L15255]. This handle type enables the sharing of memory allocations not only within a single node (intra-node) using various communication mechanisms such as MPI, but also across different nodes (inter-node) [CUDA_C_Programming_Guide:L15231-L15255].

## Key Capabilities

*   **Multi-Node NVLINK Support**: Fabric Memory allows GPUs within a Multi Node NVLINK system to map the memory of all other GPUs part of the same NVLINK fabric, even if those GPUs reside on different physical nodes [CUDA_C_Programming_Guide:L15231-L15255].
*   **Scalability**: This capability greatly increases the scale of multi-GPU programming with NVLINK by facilitating seamless memory access across nodes [CUDA_C_Programming_Guide:L15231-L15255].
*   **Simplified Handle Exchange**: Unlike other allocation handle types, using `CU_MEM_HANDLE_TYPE_FABRIC` does not require operating system native mechanisms for inter-process communication to exchange sharable handles [CUDA_C_Programming_Guide:L15231-L15255].

## Prerequisites

To use Fabric Memory, the following conditions must be met:

1.  **Supported Platforms**: The underlying hardware platform must support Fabric Memory [CUDA_C_Programming_Guide:L15231-L15255].
2.  **NVIDIA IMEX Daemon**: The NVIDIA IMEX daemon must be running on the system [CUDA_C_Programming_Guide:L15231-L15255].
3.  **Device Support**: The specific devices intended for use must support Fabric Memory [CUDA_C_Programming_Guide:L15231-L15255].

## Querying for Support

Before attempting to use Fabric Memory, applications must verify that the target devices support this feature. This is done by querying the `CU_DEVICE_ATTRIBUTE_HANDLE_TYPE_FABRIC_SUPPORTED` attribute [CUDA_C_Programming_Guide:L15231-L15255].

```cpp
int deviceSupportsFabricMem;
CUresult result = cuDeviceGetAttribute(&deviceSupportsFabricMem, CU_DEVICE_ATTRIBUTE_HANDLE_TYPE_FABRIC_SUPPORTED, device);
if (deviceSupportsFabricMem != 0) {
    // `device` supports Fabric Memory
}
```

## Usage

Aside from specifying `CU_MEM_HANDLE_TYPE_FABRIC` as the handle type and the absence of a need for OS native inter-process communication mechanisms, the usage of Fabric Memory is identical to other allocation handle types [CUDA_C_Programming_Guide:L15231-L15255].
