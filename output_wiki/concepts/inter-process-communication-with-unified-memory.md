# Inter-Process Communication (IPC) with Unified Memory

## Overview

Inter-Process Communication (IPC) with Unified Memory allows processes to share access to system-allocated memory regions. While many applications prefer managing one GPU per process, Unified Memory is often required for scenarios such as over-subscription or when accessing memory from multiple GPUs [CUDA_C_Programming_Guide:L21585-L21602].

## CUDA IPC Limitations

Standard CUDA IPC mechanisms do not support Managed Memory. Handles to Managed Memory cannot be shared through the mechanisms typically discussed for inter-process communication [CUDA_C_Programming_Guide:L21585-L21602].

## System-Allocated Memory Support

On systems with full CUDA Unified Memory support, System-Allocated Memory is Inter-Process Communication (IPC) capable. Once access to System-Allocated Memory has been shared with other processes, the same programming model applies, similar to File-backed Unified Memory [CUDA_C_Programming_Guide:L21585-L21602].

## Implementation Techniques

Various methods exist for creating IPC-capable System-Allocated Memory, particularly under Linux:

*   `mmap` with `MAP_SHARED`
*   POSIX IPC APIs
*   `memfd_create` [CUDA_C_Programming_Guide:L21585-L21602]

## Performance and Limitations

Using IPC with Unified Memory can have significant performance implications [CUDA_C_Programming_Guide:L21585-L21602]. Additionally, it is not possible to share memory between different hosts and their devices using these techniques [CUDA_C_Programming_Guide:L21585-L21602].
