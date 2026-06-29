# CUDA Compute Capability Technical Specifications

This page details the technical specifications and feature support matrix for NVIDIA GPU architectures defined by CUDA Compute Capabilities 7.5 through 12.0. The specifications cover hardware limits, memory constraints, register files, and specific instruction set support as defined in the CUDA C++ Programming Guide.

## Feature Support Matrix

The following features are supported based on the specific Compute Capability version. Unlisted features are generally supported across all compute capabilities unless noted otherwise.

### Atomic Operations and Data Types

Support for advanced atomic operations and data types varies significantly between generations:

*   **128-bit Integer Atomics:** Atomic functions operating on 128-bit integer values in global memory are supported starting from Compute Capability 9.0 [CUDA_C_Programming_Guide:L19485-L19523].
    *   **7.x / 8.x:** No support.
    *   **9.0 - 12.0:** Supported.
*   **Shared Memory 128-bit Atomics:** Atomic functions operating on 128-bit integer values in shared memory are supported starting from Compute Capability 9.0 [CUDA_C_Programming_Guide:L19485-L19523].
    *   **7.x / 8.x:** No support.
    *   **9.0 - 12.0:** Supported.
*   **Floating Point Vector Atomics:** Atomic addition (`atomicAdd`) operating on `float2` and `float4` floating-point vectors in global memory is supported starting from Compute Capability 9.0 [CUDA_C_Programming_Guide:L19485-L19523].
    *   **7.x / 8.x:** No support.
    *   **9.0 - 12.0:** Supported.
*   **Bfloat16 Precision:** Hardware support for Bfloat16-precision floating-point operations (addition, subtraction, multiplication, comparison, warp shuffle functions, and conversion) is available starting from Compute Capability 9.0 [CUDA_C_Programming_Guide:L19485-L19523].
    *   **7.x / 8.x:** No support.
    *   **9.0 - 12.0:** Supported.

### Asynchronous Operations and Memory Management

*   **memcpy_async:** Hardware-accelerated asynchronous data copies using `cuda::pipeline` are supported starting from Compute Capability 9.0 [CUDA_C_Programming_Guide:L19485-L19523].
    *   **7.x / 8.x:** No support.
    *   **9.0 - 12.0:** Supported.
*   **Split Arrive/Wait Barrier:** Hardware-accelerated Split Arrive/Wait Barrier support is available starting from Compute Capability 9.0 [CUDA_C_Programming_Guide:L19485-L19523].
    *   **7.x / 8.x:** No support.
    *   **9.0 - 12.0:** Supported.
*   **L2 Cache Residency Management:** Device Memory L2 Access Management is supported starting from Compute Capability 9.0 [CUDA_C_Programming_Guide:L19485-L19523].
    *   **7.x / 8.x:** No support.
    *   **9.0 - 12.0:** Supported.

### Advanced Architecture Features (Compute Capability 9.0+)

Starting with Compute Capability 9.0, several advanced architectural features are introduced:

*   **DPX Instructions:** Accelerated Dynamic Programming instructions are supported [CUDA_C_Programming_Guide:L19485-L19523].
*   **Distributed Shared Memory:** Supported [CUDA_C_Programming_Guide:L19485-L19523].
*   **Thread Block Cluster:** Supported [CUDA_C_Programming_Guide:L19485-L19523].
*   **Tensor Memory Accelerator (TMA):** The TMA unit is supported [CUDA_C_Programming_Guide:L19485-L19523].

## Technical Specifications

The following tables outline the hardware limits and resource allocations for Compute Capabilities 7.5 through 12.0. Note that `K` and `KB` units correspond to 1024 and 1024 bytes (KiB) respectively [CUDA_C_Programming_Guide:L19485-L19523].

### General Grid and Block Limits

These limits are consistent across all listed compute capabilities (7.5, 8.0, 8.6, 8.7, 8.9, 9.0, 10.0, 11.0, 12.0) [CUDA_C_Programming_Guide:L19485-L19523]:

| Specification | Value |
| :--- | :--- |
| Maximum number of resident grids per device | 128 |
| Maximum dimensionality of grid of thread blocks | 3 |
| Maximum x-dimension of a grid of thread blocks | $2^{31}-1$ |
| Maximum y- or z-dimension of a grid of thread blocks | 65535 |
| Maximum dimensionality of thread block | 3 |
| Maximum x- or y-dimensionality of a block | 1024 |
| Maximum z-dimension of a block | 64 |
| Maximum number of threads per block | 1024 |
| Warp size | 32 |

### SM Resource Limits

Resource limits per Streaming Multiprocessor (SM) vary by architecture generation [CUDA_C_Programming_Guide:L19485-L19523]:

| Specification | 7.5 | 8.0 | 8.6 | 8.7 | 8.9 | 9.0 / 10.0 | 11.0 | 12.0 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Max resident blocks per SM | 16 | 32 | 16 | 24 | 32 | 24 | 24 | 24 |
| Max resident warps per SM | 32 | 64 | 48 | 48 | 64 | 48 | 48 | 48 |
| Max resident threads per SM | 1024 | 2048 | 1536 | 1536 | 2048 | 1536 | 1536 | 1536 |
| Number of 32-bit registers per SM | 64 K | 64 K | 64 K | 64 K | 64 K | 64 K | 64 K | 64 K |
| Max 32-bit registers per thread block | 64 K | 64 K | 64 K | 64 K | 64 K | 64 K | 64 K | 64 K |
| Max 32-bit registers per thread | 255 | 255 | 255 | 255 | 255 | 255 | 255 | 255 |
| Max shared memory per SM | 64 KB | 164 KB | 100 KB | 164 KB | 100 KB | 228 KB | 100 KB | 100 KB |
| Max shared memory per thread block | 64 KB | 163 KB | 99 KB | 163 KB | 99 KB | 227 KB | 99 KB | 99 KB |
| Number of shared memory banks | 32 | 32 | 32 | 32 | 32 | 32 | 32 | 32 |

*Note: Shared memory values above 48 KB require dynamic shared memory allocation [CUDA_C_Programming_Guide:L19485-L19523].*

### Memory and Cache Limits

| Specification | Value |
| :--- | :--- |
| Max local memory per thread | 512 KB |
| Constant memory size | 64 KB |
| Cache working set per SM for constant memory | 8 KB |
| Cache working set per SM for texture memory | Varies by architecture (see below) |

**Cache Working Set for Texture Memory:**
*   **7.5:** 32 or 64 KB
*   **8.0:** 28 KB ~ 192 KB
*   **8.6:** 28 KB ~ 128 KB
*   **8.7:** 28 KB ~ 192 KB
*   **8.9:** 28 KB ~ 128 KB
*   **9.0:** 28 KB ~ 256 KB
*   **10.0:** 28 KB ~ 128 KB

## Texture and Surface Object Limits

These limits apply to texture and surface objects bound to kernels. The maximum number of textures that can be bound to a kernel is 256, and the maximum number of surfaces is 32 [CUDA_C_Programming_Guide:L19485-L19523].

### 1D Objects

| Object Type | Configuration | Maximum Dimension |
| :--- | :--- | :--- |
| Texture | 1D using CUDA array | Width: 131,072 |
| Texture | 1D using linear memory | Width: $2^{28}$ |
| Texture | 1D layered | Width: 32,768; Layers: 2,048 |
| Surface | 1D using CUDA array | Width: 32,768 |
| Surface | 1D layered | Width: 32,768; Layers: 2,048 |

### 2D Objects

| Object Type | Configuration | Maximum Dimensions |
| :--- | :--- | :--- |
| Texture | 2D using CUDA array | Width: 131,072; Height: 65,536 |
| Texture | 2D using linear memory | Width: 131,072; Height: 65,000 |
| Texture | 2D using CUDA array (with gather) | Width: 32,768; Height: 32,768 |
| Texture | 2D layered | Width: 32,768; Height: 32,768; Layers: 2,048 |
| Surface | 2D using CUDA array | Width: 131,072; Height: 65,536 |
| Surface | 2D layered | Width: 32,768; Height: 32,768; Layers: 1,048 |

### 3D Objects

| Object Type | Configuration | Maximum Dimensions |
| :--- | :--- | :--- |
| Texture | 3D using CUDA array | Width: 16,384; Height: 16,384; Depth: 16,384 |
| Surface | 3D using CUDA array | Width: 16,384; Height: 16,384; Depth: 16,384 |

### Cubemap Objects

| Object Type | Configuration | Maximum Dimensions |
| :--- | :--- | :--- |
| Texture | Cubemap | Width (and Height): 32,768 |
| Texture | Cubemap layered | Width (and Height): 32,768; Layers: 2,046 |
| Surface | Cubemap using CUDA array | Width (and Height): 32,768 |
| Surface | Cubemap layered | Width (and Height): 32,768; Layers: 2,046 |
