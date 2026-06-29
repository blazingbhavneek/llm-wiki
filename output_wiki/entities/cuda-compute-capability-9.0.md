# Compute Capability 9.0

Compute Capability 9.0 is the architecture identifier for NVIDIA's Hopper GPU architecture, which includes the H100 data center GPU. This architecture introduces significant enhancements in tensor processing, memory hierarchy, and specialized computation acceleration compared to previous generations.

## Architecture

A Streaming Multiprocessor (SM) in the Hopper architecture consists of the following components:

*   128 FP32 cores for single-precision arithmetic operations.
*   64 FP64 cores for double-precision arithmetic operations.
*   64 INT32 cores for integer math.
*   4 mixed-precision fifth-generation Tensor Cores.
*   16 special function units for single-precision floating-point transcendental functions.
*   4 warp schedulers.

The SM statically distributes its warps among its schedulers. At every instruction issue time, each scheduler issues one instruction for one of its assigned warps that is ready to execute, if any [CUDA_C_Programming_Guide:L19934-L20006].

### Tensor Cores

The fifth-generation Tensor Cores support a wide range of precision formats. They support FP8 input types in either E4M3 or E5M2 for exponent (E) and mantissa (M), as well as half-precision (fp16), __nv_bfloat16, tf32, INT8, and double precision (fp64) matrix arithmetic. These cores also support sparsity [CUDA_C_Programming_Guide:L19934-L20006].

## Memory Hierarchy

The Hopper architecture features a unified data cache and shared memory structure:

*   **Unified Cache/Shared Memory:** An SM has a unified data cache and shared memory with a total size of 256 KB [CUDA_C_Programming_Guide:L19934-L20006].
*   **Configuration:** Shared memory is partitioned out of the unified data cache and can be configured to various sizes. The shared memory capacity can be set to 0, 8, 16, 32, 64, 100, 132, 164, 196, or 228 KB [CUDA_C_Programming_Guide:L19934-L20006].
*   **Access Limits:** Devices of compute capability 9.0 allow a single thread block to address up to 227 KB of shared memory. The 1 KB of shared memory not made available to a thread block is reserved for system use [CUDA_C_Programming_Guide:L19934-L20006].
*   **Dynamic Allocation:** Kernels relying on shared memory allocations over 48 KB per block are architecture-specific and must use dynamic shared memory rather than statically sized shared memory arrays. These kernels require an explicit opt-in by using `cudaFuncSetAttribute()` to set the `cudaFuncAttributeMaxDynamicSharedMemorySize` [CUDA_C_Programming_Guide:L19934-L20006].
*   **Constant Cache:** An SM has a read-only constant cache that is shared by all functional units and speeds up reads from the constant memory space, which resides in device memory [CUDA_C_Programming_Guide:L19934-L20006].

## Global Memory

Global memory behaves the same way as for devices of compute capability 5.x [CUDA_C_Programming_Guide:L19934-L20006].

## Features Accelerating Specialized Computations

The NVIDIA Hopper GPU architecture includes specific features to accelerate matrix multiply-accumulate (MMA) computations:

*   Asynchronous execution of MMA instructions.
*   MMA instructions acting on large matrices spanning a warp-group.
*   Dynamic reassignment of register capacity among warp-groups to support even larger matrices.
*   Operand matrices accessed directly from shared memory [CUDA_C_Programming_Guide:L19934-L20006].

This feature set is only available within the CUDA compilation toolchain through inline PTX [CUDA_C_Programming_Guide:L19934-L20006].

It is strongly recommended that applications utilize this complex feature set through CUDA-X libraries such as cuBLAS, cuDNN, or cuFFT [CUDA_C_Programming_Guide:L19934-L20006]. Additionally, it is strongly recommended that device kernels utilize this complex feature set through CUTLASS, a collection of CUDA C++ template abstractions for implementing high-performance matrix multiplication (GEMM) and related computations at all levels and scales within CUDA [CUDA_C_Programming_Guide:L19934-L20006].

## See Also

*   Compute Capability 10.0 (Blackwell architecture), which extends the MMA features from Hopper.
*   PTX ISA for details on the specialized computation instructions.
*   Shared Memory configuration details.
*   Warp Matrix Functions for details on Tensor Core operations.
