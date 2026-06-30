# Compute Capability 9.0

Architecture specifications for Compute Capability 9.0 (Hopper) including fourth-gen Tensor Cores with FP8 support, 256KB unified cache/shared memory, and specialized MMA acceleration features.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L19895-L19954

Citation: [CUDA_C_Programming_Guide:L19895-L19954]

````text
## 20.8. Compute Capability 9.0

## 20.8.1. Architecture

A Streaming Multiprocessor (SM) consists of:

▶ 128 FP32 cores for single-precision arithmetic operations,

▶ 64 FP64 cores for double-precision arithmetic operations,

1 64 INT32 cores for integer math,

4 mixed-precision fourth-generation Tensor Cores supporting the new FP8 input type in either E4M3 or E5M2 for exponent (E) and mantissa (M), half-precision (fp16), \_\_nv\_bfloat16, tf32, INT8 and double precision (fp64) matrix arithmetic (see Warp Matrix Functions for details) with sparsity support,

▶ 16 special function units for single-precision floating-point transcendental functions,

▶ 4 warp schedulers.

An SM statically distributes its warps among its schedulers. Then, at every instruction issue time, each scheduler issues one instruction for one of its assigned warps that is ready to execute, if any.

## An SM has:

▶ a read-only constant cache that is shared by all functional units and speeds up reads from the constant memory space, which resides in device memory,

▶ a unified data cache and shared memory with a total size of 256 KB for devices of compute capability 9.0 (1.33x NVIDIA Ampere GPU Architecture’s 192 KB capacity).

Shared memory is partitioned out of the unified data cache, and can be configured to various sizes (see Shared Memory). The remaining data cache serves as an L1 cache and is also used by the texture unit that implements the various addressing and data filtering modes mentioned in Texture and Surface Memory.

## 20.8.2. Global Memory

Global memory behaves the same way as for devices of compute capability 5.x (See Global Memory).

## 20.8.3. Shared Memory

Similar to the NVIDIA Ampere GPU architecture, the amount of the unified data cache reserved for shared memory is configurable on a per kernel basis. For the NVIDIA H100 Tensor Core GPU architecture, the unified data cache has a size of 256 KB for devices of compute capability 9.0. The shared memory capacity can be set to 0, 8, 16, 32, 64, 100, 132, 164, 196 or 228 KB.

As with the NVIDIA Ampere GPU architecture, an application can configure its preferred shared memory capacity, i.e., the carveout. Devices of compute capability 9.0 allow a single thread block to address up to 227 KB of shared memory. Kernels relying on shared memory allocations over 48 KB per block are architecture-specific, and must use dynamic shared memory rather than statically sized shared memory arrays. These kernels require an explicit opt-in by using cudaFuncSetAttribute() to set the cudaFuncAttributeMaxDynamicSharedMemorySize; see Shared Memory for the NVIDIA Volta GPU Architecture.

Note that the maximum amount of shared memory per thread block is smaller than the maximum shared memory partition available per SM. The 1 KB of shared memory not made available to a thread block is reserved for system use.

## 20.8.4. Features Accelerating Specialized Computations

The NVIDIA Hopper GPU architecture includes features to accelerate matrix multiply-accumulate (MMA) computations with:

▶ asynchronous execution of MMA instructions

▶ MMA instructions acting on large matrices spanning a warp-group

dynamic reassignment of register capacity among warp-groups to support even larger matrices, and

▶ operand matrices accessed directly from shared memory

See the PTX ISA for more details.

This feature set is only available within the CUDA compilation toolchain through inline PTX.

It is strongly recommended that applications utilize this complex feature set through CUDA-X libraries such as cuBLAS, cuDNN, or cuFFT.

It is strongly recommended that device kernels utilize this complex feature set through CUT-LASS, a collection of CUDA C++ template abstractions for implementing high-performance matrixmultiplication (GEMM) and related computations at all levels and scales within CUDA.
````
