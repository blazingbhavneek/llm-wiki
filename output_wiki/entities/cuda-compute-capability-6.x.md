# Compute Capability 6.x

Compute Capability 6.x devices belong to the Pascal architecture family. This family includes three specific sub-versions: 6.0, 6.1, and 6.2, which differ primarily in the number of CUDA cores, special function units, warp schedulers, and cache sizes within the Streaming Multiprocessor (SM).

## Architecture

The composition of an SM varies depending on the specific compute capability version [CUDA_C_Programming_Guide:L19606-L19657].

### Functional Units

The SM contains the following arithmetic and scheduling units [CUDA_C_Programming_Guide:L19606-L19657]:

*   **CUDA Cores**: Used for arithmetic operations.
    *   Compute Capability 6.0: 64 cores.
    *   Compute Capability 6.1 and 6.2: 128 cores.
*   **Special Function Units (SFUs)**: Used for single-precision floating-point transcendental functions.
    *   Compute Capability 6.0: 16 SFUs.
    *   Compute Capability 6.1 and 6.2: 32 SFUs.
*   **Warp Schedulers**: These distribute warps and issue instructions.
    *   Compute Capability 6.0: 2 schedulers.
    *   Compute Capability 6.1 and 6.2: 4 schedulers.

When an SM receives warps to execute, it first distributes them among its schedulers. At every instruction issue time, each scheduler issues one instruction for one of its assigned warps that is ready to execute, if any [CUDA_C_Programming_Guide:L19606-L19657].

### Cache Hierarchy

The Pascal architecture introduces a unified cache structure and specific sizing for shared memory [CUDA_C_Programming_Guide:L19606-L19657].

*   **Constant Cache**: A read-only constant cache shared by all functional units, which speeds up reads from the constant memory space residing in device memory.
*   **Unified L1/Texture Cache**: This cache is used for reads from global memory and is also utilized by the texture unit to implement various addressing modes and data filtering. The size varies by version [CUDA_C_Programming_Guide:L19606-L19657]:
    *   Compute Capability 6.0 and 6.2: 24 KB.
    *   Compute Capability 6.1: 48 KB.
*   **Shared Memory**: The size of the shared memory also varies by version [CUDA_C_Programming_Guide:L19606-L19657]:
    *   Compute Capability 6.0 and 6.2: 64 KB.
    *   Compute Capability 6.1: 96 KB.

Additionally, an L2 cache is shared by all SMs and is used to cache accesses to local or global memory, including temporary register spills. Applications may query the L2 cache size by checking the `l2CacheSize` device property [CUDA_C_Programming_Guide:L19606-L19657].

Cache behavior, such as whether reads are cached in both the unified L1/texture cache and L2 or in L2 only, can be partially configured on a per-access basis using modifiers to the load instruction [CUDA_C_Programming_Guide:L19606-L19657].

## Memory Behavior

The memory behaviors for global and shared memory in Compute Capability 6.x devices are consistent with those of Compute Capability 5.x devices [CUDA_C_Programming_Guide:L19606-L19657].

### Global Memory

Global memory behaves the same way as in devices of compute capability 5.x [CUDA_C_Programming_Guide:L19606-L19657].

### Shared Memory

Shared memory behaves the same way as in devices of compute capability 5.x [CUDA_C_Programming_Guide:L19606-L19657].

Shared memory accesses are organized into banks. Access patterns can result in bank conflicts or be conflict-free depending on the stride and addressing mode used by threads within a warp [CUDA_C_Programming_Guide:L19606-L19657].

*   **Strided Accesses**: Linear addressing with a stride of one 32-bit word results in no bank conflict. A stride of two 32-bit words results in a two-way bank conflict. A stride of three 32-bit words results in no bank conflict [CUDA_C_Programming_Guide:L19606-L19657].
*   **Irregular Accesses**: Accesses can be conflict-free via random permutation, since threads may access the same word within a bank (broadcast access) or access different words in a way that avoids conflict [CUDA_C_Programming_Guide:L19606-L19657].
