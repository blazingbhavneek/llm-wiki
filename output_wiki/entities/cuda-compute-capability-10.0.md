# Compute Capability 10.0

Compute Capability 10.0 is the architecture identifier for the first-generation NVIDIA Blackwell GPU architecture, associated with devices such as the GB200 [CUDA_C_Programming_Guide:L20007-L20057]. This architecture extends features from the NVIDIA Hopper GPU architecture to accelerate specialized computations, particularly matrix multiply-accumulate (MMA) operations [CUDA_C_Programming_Guide:L20007-L20057].

## Architecture

A Streaming Multiprocessor (SM) in the Compute Capability 10.0 architecture consists of the following components [CUDA_C_Programming_Guide:L20007-L20057]:

*   **128 FP32 cores** for single-precision arithmetic operations.
*   **2 FP64 cores** for double-precision arithmetic operations.
*   **64 INT32 cores** for integer math.
*   **Mixed-precision fifth-generation Tensor Cores** supporting FP8 input types in either E4M3 or E5M2 for exponent (E) and mantissa (M), as well as half-precision (fp16), `__nv_bfloat16`, tf32, INT8, and double precision (fp64) matrix arithmetic [CUDA_C_Programming_Guide:L20007-L20057]. These cores support sparsity [CUDA_C_Programming_Guide:L20007-L20057].
*   **16 special function units** for single-precision floating-point transcendental functions.
*   **4 warp schedulers** [CUDA_C_Programming_Guide:L20007-L20057].

An SM statically distributes its warps among its schedulers. At every instruction issue time, each scheduler issues one instruction for one of its assigned warps that is ready to execute, if any [CUDA_C_Programming_Guide:L20007-L20057].

## Memory Hierarchy

The SM includes a read-only constant cache shared by all functional units to speed up reads from the constant memory space, which resides in device memory [CUDA_C_Programming_Guide:L20007-L20057].

### Unified Data Cache and Shared Memory

The architecture features a unified data cache and shared memory with a total size of 100 KB [CUDA_C_Programming_Guide:L20007-L20057]. Shared memory is partitioned out of this unified data cache and can be configured to various sizes [CUDA_C_Programming_Guide:L20007-L20057]. The remaining data cache serves as an L1 cache and is also used by the texture unit, which implements various addressing and data filtering modes [CUDA_C_Programming_Guide:L20007-L20057].

The amount of the unified data cache reserved for shared memory is configurable on a per-kernel basis [CUDA_C_Programming_Guide:L20007-L20057]. The shared memory capacity can be set to 0, 8, 16, 32, 64, or 100 KB [CUDA_C_Programming_Guide:L20007-L20057]. As with the NVIDIA Ampere GPU architecture, an application can configure its preferred shared memory capacity (carveout) [CUDA_C_Programming_Guide:L20007-L20057].

Devices of compute capability 10.0 allow a single thread block to address up to 99 KB of shared memory [CUDA_C_Programming_Guide:L20007-L20057]. Kernels relying on shared memory allocations over 48 KB per block are architecture-specific and must use dynamic shared memory rather than statically sized shared memory arrays [CUDA_C_Programming_Guide:L20007-L20057]. These kernels require an explicit opt-in by using `cudaFuncSetAttribute()` to set the `cudaFuncAttributeMaxDynamicSharedMemorySize` [CUDA_C_Programming_Guide:L20007-L20057].

Note that the maximum amount of shared memory per thread block (99 KB) is smaller than the maximum shared memory partition available per SM (100 KB); the 1 KB of shared memory not made available to a thread block is reserved for system use [CUDA_C_Programming_Guide:L20007-L20057].

### Global Memory

Global memory behaves the same way as for devices of compute capability 5.x [CUDA_C_Programming_Guide:L20007-L20057].

## Specialized Computations

The NVIDIA Blackwell GPU architecture extends features to accelerate matrix multiply-accumulate (MMA) from the NVIDIA Hopper GPU architecture [CUDA_C_Programming_Guide:L20007-L20057]. This feature set is only available within the CUDA compilation toolchain through inline PTX [CUDA_C_Programming_Guide:L20007-L20057].

It is strongly recommended that applications utilize this complex feature set through CUDA-X libraries such as cuBLAS, cuDNN, or cuFFT [CUDA_C_Programming_Guide:L20007-L20057]. Additionally, it is strongly recommended that device kernels utilize this complex feature set through CUTLASS, a collection of CUDA C++ template abstractions for implementing high-performance matrix multiplication (GEMM) and related computations at all levels and scales within CUDA [CUDA_C_Programming_Guide:L20007-L20057].

## See Also

*   Warp Matrix Functions
*   Shared Memory
*   Texture and Surface Memory
*   PTX ISA
