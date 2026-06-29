# CUDA Pending Kernel Launches

When a kernel is launched, all associated configuration and parameter data is tracked until the kernel completes. This data is stored within a system-managed launch pool [CUDA_C_Programming_Guide:L14230-L14235].

The size of the fixed-size launch pool is configurable by calling `cudaDeviceSetLimit()` from the host and specifying `cudaLimitDevRuntimePendingLaunchCount` [CUDA_C_Programming_Guide:L14230-L14235].
