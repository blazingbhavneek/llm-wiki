# CUDA Environment Variables

> **Warning:** This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA [CUDA_C_Programming_Guide:L20604-L20609].

The following table lists the CUDA environment variables. Environment variables related to the Multi-Process Service are documented in the Multi-Process Service section of the GPU Deployment and Management guide [CUDA_C_Programming_Guide:L20604-L20609].

## Device Enumeration

| Variable | Values | Description |
| :--- | :--- | :--- |
| `CUDA_VISIBLE_DEVICES` | A comma-separated sequence of GPU identifiers. MIG support: `MIG-//` | GPU identifiers are given as integer indices or as UUID strings. GPU UUID strings should follow the same format as given by `nvidia-smi`, such as `GPU-8932f937-d72c-4106-c12f-20bd9faed9f6`. However, for convenience, abbreviated forms are allowed; simply specify enough digits from the beginning of the GPU UUID to uniquely identify that GPU in the target system. For example, `CUDA_VISIBLE_DEVICES=GPU-8932f937` may be a valid way to refer to the above GPU UUID, assuming no other GPU in the system shares this prefix. Only the devices whose index is present in the sequence are visible to CUDA applications and they are enumerated in the order of the sequence. If one of the indices is invalid, only the devices whose index precedes the invalid index are visible to CUDA applications. For example, setting `CUDA_VISIBLE_DEVICES` to `2,1` causes device 0 to be invisible and device 2 to be enumerated before device 1. Setting `CUDA_VISIBLE_DEVICES` to `0,2,-1,1` causes devices 0 and 2 to be visible and device 1 to be invisible. MIG format starts with `MIG` keyword and GPU UUID should follow the same format as given by `nvidia-smi`. For example, `MIG-GPU-8932f937-d72c-4106-c12f-20bd9faed9f6/1/2`. Only single MIG instance enumeration is supported [CUDA_C_Programming_Guide:L20618-L20620]. |
| `CUDA_MANAGED_FORCE_DEVICE` | 0 or 1 (Default is 0) | Forces the driver to place all managed allocations in device memory [CUDA_C_Programming_Guide:L20618-L20620]. |
| `CUDA_DEVICE_ORDER` | `FASTEST_FIRST`, `PCI_BUS_ID` (default is `FASTEST_FIRST`) | `FASTEST_FIRST` causes CUDA to enumerate the available devices in fastest to slowest order using a simple heuristic. `PCI_BUS_ID` orders devices by PCI bus ID in ascending order [CUDA_C_Programming_Guide:L20623-L20625]. |

## Compilation

| Variable | Values | Description |
| :--- | :--- | :--- |
| `CUDA_CACHE_DISABLE` | 0 or 1 (default is 0) | Disables caching (when set to 1) or enables caching (when set to 0) for just-in-time-compilation. When disabled, no binary code is added to or retrieved from the cache [CUDA_C_Programming_Guide:L20623-L20625]. |
| `CUDA_CACHE_PATH` | filepath | Specifies the folder where the just-in-time compiler caches binary codes; the default values are: on Windows, `%APPDATA%\NVIDIA\ComputeCache`; on Linux, `~/.nv/ComputeCache` [CUDA_C_Programming_Guide:L20623-L20625]. |
| `CUDA_CACHE_MAXSIZE` | integer (default is 1073741824 (1 GiB) for desktop/server platforms and 268435456 (256 MiB) for embedded platforms and the maximum is 4294967296 (4 GiB)) | Specifies the size in bytes of the cache used by the just-in-time compiler. Binary codes whose size exceeds the cache size are not cached. Older binary codes are evicted from the cache to make room for newer binary codes if needed [CUDA_C_Programming_Guide:L20623-L20625]. |
| `CUDA_FORCE_PTX_JIT` | 0 or 1 (default is 0) | When set to 1, forces the device driver to ignore any binary code embedded in an application (see Application Compatibility) and to just-in-time compile embedded PTX code instead. If a kernel does not have embedded PTX code, it will fail to load. This environment variable can be used to validate that PTX code is embedded in an application and that its just-in-time compilation works as expected to guarantee application forward compatibility with future architectures (see Just-in-Time Compilation) [CUDA_C_Programming_Guide:L20628-L20631]. |
| `CUDA_DISABLE_PTX_JIT` | 0 or 1 (default is 0) | When set to 1, disables the just-in-time compilation of embedded PTX code and use the compatible binary code embedded in an application (see Application Compatibility). If a kernel does not have embedded binary code or the embedded binary was compiled for an incompatible architecture, then it will fail to load. This environment variable can be used to validate that an application has the compatible SASS code generated for each kernel (see Binary Compatibility) [CUDA_C_Programming_Guide:L20628-L20631]. |
| `CUDA_FORCE_JIT` | 0 or 1 (default is 0) | When set to 1, forces the device driver to ignore any binary code embedded in an application (see Application Compatibility) and to just-in-time compile embedded PTX code instead. If a kernel does not have embedded PTX code, it will fail to load. This environment variable can be used to validate that PTX code is embedded in an application and that its just-in-time compilation works as expected to guarantee application forward compatibility with future architectures (see Just-in-Time Compilation). The behavior can be overridden for embedded PTX by setting `CUDA_FORCE_PTX_JIT=0` [CUDA_C_Programming_Guide:L20634-L20637]. |
| `CUDA_DISABLE_JIT` | 0 or 1 (default is 0) | When set to 1, disables the just-in-time compilation of embedded PTX code and use the compatible binary code embedded in an application (see Application Compatibility). If a kernel does not have embedded binary code or the embedded binary was compiled for an incompatible architecture, then it will fail to load. This environment variable can be used to validate that an application has the compatible SASS code generated for each kernel (see Binary Compatibility). The behavior can be overridden for embedded PTX by setting `CUDA_DISABLE_PTX_JIT=0` [CUDA_C_Programming_Guide:L20634-L20637]. |

## Execution

| Variable | Values | Description |
| :--- | :--- | :--- |
| `CUDA_LAUNCH_BLOCKING` | 0 or 1 (default is 0) | Disables (when set to 1) or enables (when set to 0) asynchronous kernel launches [CUDA_C_Programming_Guide:L20634-L20637]. |
| `CUDA_DEVICE_MAX_CONNECTIONS` | 0 to 32 (default is 8) | Sets the number of compute and copy engine concurrent connections (work queues) from the host to each device of compute capability 3.5 and above [CUDA_C_Programming_Guide:L20640-L20643]. |
| `CUDA_DEVICE_MAX_COPY_CONNECTIONS` | 0 to 32 (default is 8) | Sets the number of copy engine concurrent connections (work queues) per async copy engine from the host to each device of compute capability 8.0 and above. When both `CUDA_DEVICE_MAX_CONNECTION` and `CUDA_DEVICE_MAX_COPY_CONNECTION` are set, only the number of copy connections set by `CUDA_DEVICE_MAX_CONNECTION` will be overwritten [CUDA_C_Programming_Guide:L20640-L20643]. |
| `CUDA_AUTO_BOOST` | 0 or 1 | Overrides the autoboost behavior set by the `-auto-boost-default` option of `nvidia-smi`. If an application requests via this environment variable a behavior that is different from `nvidia-smi`'s, its request is honored if there is no other application currently running on the same GPU that successfully requested a different behavior, otherwise it is ignored [CUDA_C_Programming_Guide:L20640-L20643]. |
| `CUDA_SCALE_LAUNCH_QUEUE` | "0.25x", "0.5x", "2x" or "4x" | Scales the size of the queues available for launching work by a fixed multiplier [CUDA_C_Programming_Guide:L20640-L20643]. |
| `CUDA_DEVICE_WAITS_ON_EXCEPTION` | Default is 0) | When set to 1, a CUDA application will halt when a device exception occurs, allowing a debugger to be attached for further debugging (cuda-gdb on Linux platform) [CUDA_C_Programming_Guide:L20640-L20643]. |
| `CUDA_DEVICE_DEFAULT_PERSISTING` | Range Percentages 100, default is 0) | Devices of compute capability 8.x allow, a portion of L2 cache to be set-aside for persisting data accesses to global memory. When using CUDA MPS service, the set-aside size can only be controlled using this environment variable, before starting CUDA MPS control daemon. I.e., the environment variable should be set before running the command `nvidia-cuda-mps-control -d` [CUDA_C_Programming_Guide:L20646-L20649]. |

## Module Loading

| Variable | Values | Description |
| :--- | :--- | :--- |
| `CUDA_MODULE_LOADING` | `DEFAULT`, `LAZY`, `EAGER` (default is `LAZY`) | Specifies the module loading mode for the application. When set to `EAGER`, all kernels and data from a cubin, fatbin or a PTX file are fully loaded upon corresponding `cuModuleLoad*` and `cuLibraryLoad*` API call. When set to `LAZY`, loading of specific kernels is delayed to the point a `CUfunc` handle is extracted with `cuModuleGetFunction` or `cuKernelGetFunction` API calls and data from the cubin is loaded at load of first kernel in the cubin or at first access of variables in the cubin. Default behavior may change in future CUDA releases [CUDA_C_Programming_Guide:L20646-L20649]. |
| `CUDA_MODULE_DATA_LOADING` | `DEFAULT`, `LAZY`, `EAGER` (default is `LAZY`) | Specifies the data loading mode for the application. When set to `EAGER`, all data from a cubin, fatbin or a PTX file are fully loaded to memory upon corresponding `cuLibraryLoad*`. This doesn't affect the `LAZY` or `EAGER` loading of kernels. When set to `LAZY`, loading of data is delayed to the point at which a handle is required. Default behavior may change in future CUDA releases. Data loading behavior is inherited from `CUDA_MODULE_LOADING` if this environment variable is not set [CUDA_C_Programming_Guide:L20652-L20653]. |
| `CUDA_BINARY_LOADER_THREAD` | COUNT (default is 0) | Sets the number of CPU threads to use when loading device binaries. When set to 0, the number of CPU threads used is set to a default value of 1. When this is set, `CU_JIT_BINARY_LOADER_THREAD` is ignored [CUDA_C_Programming_Guide:L20652-L20653]. |
| `CUDA_FORCE_PRELOAD_LIBRARIES` | 0 or 1 (default is 0) | When set to 1, forces the driver to preload the libraries required for NVVM and PTX just-in-time compilation during driver initialization. This will increase the memory footprint and the time taken for CUDA driver initialization. This environment variable needs to be set to avoid certain deadlock situations involving multiple CUDA threads [CUDA_C_Programming_Guide:L20652-L20653]. |

## CUDA Graphs

| Variable | Values | Description |
| :--- | :--- | :--- |
| `CUDA_GRAPHS_USE_NODE_PRIORITY` | 0 or 1 | Overrides the `cudaGraphInstantiateFlagUseNodePriority` flag on graph instantiation. When set to 1, the flag will be set for all graphs and when set to 0, the flag will be cleared for all graphs [CUDA_C_Programming_Guide:L20652-L20653]. |

## Error Log Management

| Variable | Values | Description |
| :--- | :--- | :--- |
| `CUDA_LOG_FILE` | `stdout`, `stderr`, or valid file path | Provides a location for printing error logs as they occur. See the Error Log Management section for more details [CUDA_C_Programming_Guide:L20656-L20659]. |
