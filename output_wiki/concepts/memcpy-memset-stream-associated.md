# Memcpy/Memset Behavior with Stream-Associated Unified Memory

This section details the specific behaviors of `cudaMemcpy*` and `cudaMemset*` operations on devices where the `concurrentManagedAccess` device attribute is not set (i.e., is zero). On such devices, memory coherency between the CPU and GPU is not guaranteed automatically, and access rules depend heavily on stream associations and visibility flags.

## General Overview

For a general overview of `cudaMemcpy*` / `cudaMemset*` behavior on devices where `concurrentManagedAccess` is set, see the section on Memcpy/Memset Behavior With Unified Memory. The rules below apply specifically when concurrent access is **not** enabled.

## Copy Rules for Unified Memory

When performing memory copies involving unified memory on devices without `concurrentManagedAccess`, the source and destination of the data are determined by coherency rules relative to the copy stream.

### cudaMemcpyHostTo* (Host to Device/Host)

If `cudaMemcpyHostTo*` is specified and the source data is unified memory:
- The data will be accessed from the **host** if it is coherently accessible from the host in the copy stream.
- Otherwise, the data will be accessed from the **device**.

Similar rules apply to the destination when `cudaMemcpy*ToHost` is specified and the destination is unified memory.

### cudaMemcpyDeviceTo* (Device to Host/Device)

If `cudaMemcpyDeviceTo*` is specified and the source data is unified memory:
- The data will be accessed from the **device**.
- The source **must** be coherently accessible from the device in the copy stream; otherwise, an error is returned.

Similar rules apply to the destination when `cudaMemcpy*ToDevice` is specified and the destination is unified memory.

### cudaMemcpyDefault

If `cudaMemcpyDefault` is specified, the system determines the access location based on the following logic:
- The unified memory will be accessed from the **host** if:
  - It cannot be coherently accessed from the device in the copy stream; **OR**
  - The preferred location for the data is `cudaCpuDeviceId` **and** it can be coherently accessed from the host in the copy stream.
- Otherwise, it will be accessed from the **device**.

## Memset Rules

When using `cudaMemset*()` with unified memory:
- The data **must** be coherently accessible from the device in the stream being used for the `cudaMemset()` operation.
- If this condition is not met, an error is returned.

## CPU Access and Synchronization

When data is accessed from the device either by `cudaMemcpy*` or `cudaMemset*`, the stream of operation is considered to be active on the GPU. 

On devices where `concurrentManagedAccess` is zero:
- Any CPU access of data that is associated with that stream or data that has global visibility will result in a **segmentation fault** if the GPU is still accessing it.
- The program **must** synchronize appropriately to ensure the operation has completed before accessing any associated data from the CPU.

## Definitions of Coherency

The terms "coherently accessible" are defined relative to a given stream as follows:

1. **Coherently accessible from the host** in a given stream means that the memory neither has global visibility nor is it associated with the given stream.
2. **Coherently accessible from the device** in a given stream means that the memory either has global visibility or is associated with the given stream.

## References

- CUDA C Programming Guide, Section 24.3.2.4.7 [CUDA_C_Programming_Guide:L22056-L22074]
