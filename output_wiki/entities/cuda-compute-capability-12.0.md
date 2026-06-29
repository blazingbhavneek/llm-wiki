# Compute Capability 12.0

Compute Capability 12.0 is the compute capability identifier for devices based on the **Blackwell architecture (second gen)**, also known as **B200** [CUDA_C_Programming_Guide:L20058-L20154].

## Documentation Status

Information regarding Compute Capability 12.0 is currently subject to documentation transitions. The specific section of the CUDA C Programming Guide that previously detailed these devices has been replaced by a new CUDA Programming Guide [CUDA_C_Programming_Guide:L20058-L20154].

The legacy content, which includes details on the Driver API, is considered obsolete and is no longer being updated as of CUDA 13.0 [CUDA_C_Programming_Guide:L20058-L20154]. Users are advised to refer to the current CUDA Programming Guide for up-to-date information on CUDA features and architecture specifics [CUDA_C_Programming_Guide:L20058-L20154].

## Legacy Context: Driver API

The existing source material for this compute capability primarily covers the **CUDA Driver API**, which is implemented in the `cuda` dynamic library (`cuda.dll` or `cuda.so`) [CUDA_C_Programming_Guide:L20058-L20154].

### Key Concepts

*   **Handle-based API**: The Driver API is imperative, where most objects are referenced by opaque handles [CUDA_C_Programming_Guide:L20058-L20154].
*   **Initialization**: The API must be initialized with `cuInit()` before any function calls [CUDA_C_Programming_Guide:L20058-L20154].
*   **Context**: A CUDA context must be created and attached to a specific device [CUDA_C_Programming_Guide:L20058-L20154].

### Available Objects

The Driver API manages the following objects, summarized by their handle types:

| Object | Handle | Description |
| :--- | :--- | :--- |
| Device | `CUdevice` | CUDA-enabled device |
| Context | `CUcontext` | Roughly equivalent to a CPU process |
| Module | `CUmodule` | Roughly equivalent to a dynamic library |
| Function | `CUfunction` | Kernel |
| Heap memory | `CUdeviceptr` | Pointer to device memory |
| CUDA array | `CUarray` | Opaque container for 1D or 2D data on the device |
| Texture object | `CUtexref` | Object describing texture memory data interpretation |
| Surface reference | `CUsurfref` | Object describing how to read/write CUDA arrays |
| Stream | `CUstream` | Object describing a CUDA stream |
| Event | `CUevent` | Object describing a CUDA event |

### Execution Model

Within a CUDA context, kernels are explicitly loaded as PTX or binary objects by the host code [CUDA_C_Programming_Guide:L20058-L20154]. Kernels written in C++ must be compiled separately into PTX or binary objects [CUDA_C_Programming_Guide:L20058-L20154].

For compatibility with future device architectures, applications must load **PTX** code rather than binary code, as binary code is architecture-specific and incompatible with future hardware [CUDA_C_Programming_Guide:L20058-L20154]. PTX code is compiled to binary code at load time by the device driver [CUDA_C_Programming_Guide:L20058-L20154].

### Example Workflow

A typical Driver API workflow involves:
1.  Initializing the API with `cuInit(0)` [CUDA_C_Programming_Guide:L20058-L20154].
2.  Retrieving the device count and getting a handle for a specific device (e.g., device 0) using `cuDeviceGetCount` and `cuDeviceGet` [CUDA_C_Programming_Guide:L20058-L20154].
3.  Creating a context with `cuCtxCreate` [CUDA_C_Programming_Guide:L20058-L20154].
4.  Loading a module (e.g., `VecAdd.ptx`) with `cuModuleLoad` [CUDA_C_Programming_Guide:L20058-L20154].
5.  Allocating device memory using `cuMemAlloc` [CUDA_C_Programming_Guide:L20058-L20154].
6.  Copying data from host to device using `cuMemcpyHtoD` [CUDA_C_Programming_Guide:L20058-L20154].
7.  Retrieving the function handle with `cuModuleGetFunction` [CUDA_C_Programming_Guide:L20058-L20154].
8.  Launching the kernel with `cuLaunchKernel` [CUDA_C_Programming_Guide:L20058-L20154].

Full code examples for these operations can be found in the `vectorAddDrv` CUDA sample [CUDA_C_Programming_Guide:L20058-L20154].
