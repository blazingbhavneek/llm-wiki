# Compute Capability 5.x

Compute Capability 5.x devices are based on the Maxwell architecture. This architecture introduces specific structural changes to the Streaming Multiprocessor (SM) and a more flexible memory caching hierarchy compared to previous generations.

## Architecture

An SM in Compute Capability 5.x consists of the following functional units [CUDA_C_Programming_Guide:L19552-L19560]:

*   **128 CUDA cores**: Used for arithmetic operations [CUDA_C_Programming_Guide:L19552-L19554].
*   **32 Special Function Units (SFUs)**: Dedicated to single-precision floating-point transcendental functions [CUDA_C_Programming_Guide:L19554-L19556].
*   **4 Warp Schedulers**: These distribute warps among the schedulers. At every instruction issue time, each scheduler issues one instruction for one of its assigned warps that is ready to execute [CUDA_C_Programming_Guide:L19556-L19560].

## Memory Hierarchy

The memory hierarchy includes a constant cache, a unified L1/texture cache, shared memory, and a global L2 cache. The configuration of shared memory and caching behaviors varies slightly between Compute Capability 5.0 and 5.2 devices.

### Cache Structure

Each SM contains [CUDA_C_Programming_Guide:L19562-L19575]:

*   **Constant Cache**: A read-only cache shared by all functional units to speed up reads from the constant memory space in device memory.
*   **Unified L1/Texture Cache**: A 24 KB cache used to cache reads from global memory. It is also used by the texture unit for addressing modes and data filtering.
*   **Shared Memory**: The size depends on the specific compute capability:
    *   **64 KB** for devices of Compute Capability 5.0.
    *   **96 KB** for devices of Compute Capability 5.2.

All SMs share a global **L2 cache** used to cache accesses to local or global memory, including temporary register spills. The L2 cache size can be queried via the `l2CacheSize` device property.

### Global Memory Caching

Global memory accesses are always cached in the L2 cache [CUDA_C_Programming_Guide:L19577-L19579]. Caching in the unified L1/texture cache is subject to specific conditions and configurations:

*   **Read-Only Data**: Data that is read-only for the entire lifetime of the kernel can be cached in the unified L1/texture cache by using the `__ldg()` function. The compiler may automatically use `__ldg()` if it detects the read-only condition, but using `const` and `__restrict__` qualifiers on pointers increases the likelihood of detection [CUDA_C_Programming_Guide:L19579-L19590].
*   **Compute Capability 5.0**: Data that is not read-only for the entire lifetime of the kernel cannot be cached in the unified L1/texture cache [CUDA_C_Programming_Guide:L19590-L19592].
*   **Compute Capability 5.2**: By default, non-read-only data is not cached in the unified L1/texture cache. However, caching can be enabled using one of the following mechanisms [CUDA_C_Programming_Guide:L19592-L19605]:
    1.  Performing the read using inline assembly with the appropriate modifier as described in the PTX reference manual.
    2.  Compiling with the `-Xptxas -dlcm=ca` flag, which caches all reads except those using inline assembly with a modifier that disables caching.
    3.  Compiling with the `-Xptxas -fscm=ca` flag, which caches all reads, including those using inline assembly regardless of the modifier.

When caching is enabled on Compute Capability 5.2 devices, global memory reads are cached in the unified L1/texture cache for all kernel launches except those where thread blocks consume too much of the SM’s register file (these exceptions are reported by the profiler) [CUDA_C_Programming_Guide:L19592-L19605].

### Shared Memory

Shared memory is organized into 32 banks, with successive 32-bit words mapping to successive banks. Each bank provides a bandwidth of 32 bits per clock cycle [CUDA_C_Programming_Guide:L19607-L19610].

Bank conflict handling follows these rules [CUDA_C_Programming_Guide:L19610-L19616]:

*   A shared memory request for a warp does not generate a bank conflict between two threads accessing any address within the same 32-bit word, even if those addresses fall in the same bank.
*   For **read accesses**, the word is broadcast to the requesting threads.
*   For **write accesses**, each address is written by only one of the threads (the specific thread performing the write is undefined).

Strided access patterns and broadcast mechanisms are illustrated in the architecture documentation (Figures 39 and 40) [CUDA_C_Programming_Guide:L19616-L19620].
