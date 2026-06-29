# Interprocess Communication (IPC)

Device memory pointers and event handles created by a host thread are valid only within the same process. They cannot be directly referenced by threads belonging to a different process. To share device memory pointers and events across processes, an application must use the Inter Process Communication (IPC) API [CUDA_C_Programming_Guide:L3610-L3625].

## Supported Platforms and Requirements

The CUDA IPC API has specific platform and hardware requirements:

*   **OS and Architecture**: Supported only for 64-bit processes on Linux [CUDA_C_Programming_Guide:L3610-L3625].
*   **Compute Capability**: Supported for devices of compute capability 2.0 and higher [CUDA_C_Programming_Guide:L3610-L3625].
*   **CUDA Version Consistency**: Applications using CUDA IPC to communicate with each other should be compiled, linked, and run with the same CUDA driver and runtime [CUDA_C_Programming_Guide:L3610-L3625].

## API Usage

The IPC API enables sharing of device memory and events through the following mechanisms:

### Memory Sharing
An application can share device memory by performing these steps:
1.  Retrieve the IPC handle for a given device memory pointer using `cudaIpcGetMemHandle()` [CUDA_C_Programming_Guide:L3610-L3625].
2.  Pass the handle to another process using standard IPC mechanisms, such as interprocess shared memory or files [CUDA_C_Programming_Guide:L3610-L3625].
3.  In the receiving process, use `cudaIpcOpenMemHandle()` to retrieve a device pointer that is valid within that process [CUDA_C_Programming_Guide:L3610-L3625].

### Event Sharing
Event handles can be shared using similar entry points to those used for memory sharing [CUDA_C_Programming_Guide:L3610-L3625].

## Limitations and Security Considerations

### Managed Memory
The IPC API is not supported for allocations made with `cudaMallocManaged` [CUDA_C_Programming_Guide:L3610-L3625].

### Information Disclosure Risks
Allocations made by `cudaMalloc()` may be sub-allocated from a larger block of memory for performance reasons. When sharing such an allocation, the CUDA IPC APIs share the entire underlying memory block. This can cause other sub-allocations to be shared, potentially leading to information disclosure between processes [CUDA_C_Programming_Guide:L3610-L3625].

To prevent this behavior, it is recommended to only share allocations with a 2MiB aligned size [CUDA_C_Programming_Guide:L3610-L3625].

### Tegra Devices
Since CUDA 11.5, support for IPC on L4T and embedded Linux Tegra devices with compute capability 7.x and higher is limited:
*   **Supported**: Events-sharing IPC APIs [CUDA_C_Programming_Guide:L3610-L3625].
*   **Not Supported**: Memory-sharing IPC APIs [CUDA_C_Programming_Guide:L3610-L3625].

## Use Case Example

A common use case for IPC is a scenario where a single primary process generates a batch of input data and makes it available to multiple secondary processes. This allows the secondary processes to access the data without requiring regeneration or copying, improving efficiency [CUDA_C_Programming_Guide:L3610-L3625].
