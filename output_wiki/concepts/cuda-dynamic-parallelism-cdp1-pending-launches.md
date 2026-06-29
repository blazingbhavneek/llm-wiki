# CUDA Dynamic Parallelism (CDP1) Pending Kernel Launches

In CUDA Dynamic Parallelism version 1 (CDP1), the management of pending kernel launches is handled through a system-managed launch pool. When a kernel is launched, all associated configuration and parameter data is tracked until the kernel completes [CUDA_C_Programming_Guide:L14942-L14951].

## Launch Pool Structure

The launch pool is divided into two distinct components:

1.  **Fixed-size pool**: This is the primary storage for launch data. The device runtime system software attempts to track launch data in the fixed-size pool first [CUDA_C_Programming_Guide:L14942-L14951].
2.  **Virtualized pool**: This component has lower performance and is used to track new launches only when the fixed-size pool is full [CUDA_C_Programming_Guide:L14942-L14951].

## Configuration

The size of the fixed-size launch pool is configurable. Developers can adjust this limit by calling `cudaDeviceSetLimit()` from the host and specifying the `cudaLimitDevRuntimePendingLaunchCount` parameter [CUDA_C_Programming_Guide:L14942-L14951].

## Note on CDP2

For information regarding pending kernel launches in CUDA Dynamic Parallelism version 2 (CDP2), refer to the separate "Pending Kernel Launches" section in the documentation [CUDA_C_Programming_Guide:L14942-L14951].
