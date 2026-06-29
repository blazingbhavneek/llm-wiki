# Texture and Surface Memory

CUDA supports a subset of the texturing hardware that the GPU uses for graphics to access texture and surface memory. Reading data from texture or surface memory instead of global memory can have several performance benefits [CUDA_C_Programming_Guide:L3644-L3648].

## Overview

The texture and surface memory spaces reside in device memory and are cached in the texture cache. Consequently, a texture fetch or surface read costs one memory read from device memory only on a cache miss; otherwise, it costs only one read from the texture cache [CUDA_C_Programming_Guide:L6502-L6515].

The texture cache is optimized for 2D spatial locality. Threads of the same warp that read texture or surface addresses that are close together in 2D will achieve the best performance [CUDA_C_Programming_Guide:L6502-L6515]. Additionally, the cache is designed for streaming fetches with constant latency; a cache hit reduces DRAM bandwidth demand but does not reduce fetch latency [CUDA_C_Programming_Guide:L6502-L6515].

## Benefits

Reading device memory through texture or surface fetching presents several benefits that can make it an advantageous alternative to reading device memory from global or constant memory [CUDA_C_Programming_Guide:L6502-L6515]:

*   **Irregular Access Patterns:** If memory reads do not follow the access patterns required for global or constant memory to achieve good performance, higher bandwidth can be achieved provided there is locality in the texture fetches or surface reads [CUDA_C_Programming_Guide:L6502-L6515].
*   **Offloaded Addressing:** Addressing calculations are performed outside the kernel by dedicated units [CUDA_C_Programming_Guide:L6502-L6515].
*   **Data Broadcasting:** Packed data may be broadcast to separate variables in a single operation [CUDA_C_Programming_Guide:L6502-L6515].
*   **Data Conversion:** 8-bit and 16-bit integer input data may be optionally converted to 32-bit floating-point values in the range [0.0, 1.0] or [-1.0, 1.0] [CUDA_C_Programming_Guide:L6502-L6515].

## Texture Memory

Texture memory is a specific type of texture and surface memory space within CUDA [CUDA_C_Programming_Guide:L3644-L3648].
