# Compute Capability 8.x

Architecture specifications for Compute Capability 8.x (Ampere) including third/fourth-gen Tensor Cores, unified cache/shared memory sizes (192KB/128KB), and shared memory carveout configurations.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L19847-L19894

Citation: [CUDA_C_Programming_Guide:L19847-L19894]

````text
## 20.7. Compute Capability 8.x

## 20.7.1. Architecture

A Streaming Multiprocessor (SM) consists of:

▶ 64 FP32 cores for single-precision arithmetic operations in devices of compute capability 8.0 and 128 FP32 cores in devices of compute capability 8.6, 8.7 and 8.9,

▶ 32 FP64 cores for double-precision arithmetic operations in devices of compute capability 8.0 and 2 FP64 cores in devices of compute capability 8.6, 8.7 and 8.9

64 INT32 cores for integer math,

4 mixed-precision Third-Generation Tensor Cores supporting half-precision (fp16), \_\_nv\_bfloat16, tf32, sub-byte and double precision (fp64) matrix arithmetic for compute capabilities 8.0, 8.6 and 8.7 (see Warp Matrix Functions for details),

▶ 4 mixed-precision Fourth-Generation Tensor Cores supporting fp8, fp16, \_\_nv\_bfloat16, tf32, sub-byte and fp64 for compute capability 8.9 (see Warp Matrix Functions for details),

▶ 16 special function units for single-precision floating-point transcendental functions,

## ▶ 4 warp schedulers.

An SM statically distributes its warps among its schedulers. Then, at every instruction issue time, each scheduler issues one instruction for one of its assigned warps that is ready to execute, if any.

## An SM has:

▶ a read-only constant cache that is shared by all functional units and speeds up reads from the constant memory space, which resides in device memory,

▶ a unified data cache and shared memory with a total size of 192 KB for devices of compute capability 8.0 and 8.7 (1.5x Volta’s 128 KB capacity) and 128 KB for devices of compute capabilities 8.6 and 8.9.

Shared memory is partitioned out of the unified data cache, and can be configured to various sizes (see Shared Memory). The remaining data cache serves as an L1 cache and is also used by the texture unit that implements the various addressing and data filtering modes mentioned in Texture and Surface Memory.

## 20.7.2. Global Memory

Global memory behaves the same way as for devices of compute capability 5.x (See Global Memory).

## 20.7.3. Shared Memory

Similar to the Volta architecture, the amount of the unified data cache reserved for shared memory is configurable on a per kernel basis. For the NVIDIA Ampere GPU Architecture, the unified data cache has a size of 192 KB for devices of compute capability 8.0 and 8.7 and 128 KB for devices of compute capabilities 8.6 and 8.9. The shared memory capacity can be set to 0, 8, 16, 32, 64, 100, 132 or 164 KB for devices of compute capability 8.0 and 8.7, and to 0, 8, 16, 32, 64 or 100 KB for devices of compute capabilities 8.6 and 8.9.

An application can set the carveout, i.e., the preferred shared memory capacity, with the cudaFunc-SetAttribute().

cudaFuncSetAttribute(kernel\_name, cudaFuncAttributePreferredSharedMemoryCarveout, , carveout);

The API can specify the carveout either as an integer percentage of the maximum supported shared memory capacity of 164 KB for devices of compute capability 8.0 and 8.7 and 100 KB for devices of compute capabilities 8.6 and 8.9 respectively, or as one of the following values: {cudaSharedmemCarveoutDefault, cudaSharedmemCarveoutMaxL1, or cudaSharedmemCarveoutMaxShared. When using a percentage, the carveout is rounded up to the nearest supported shared memory capacity. For example, for devices of compute capability 8.0, 50% will map to a 100 KB carveout instead of an 82 KB one. Setting the cudaFuncAttributePreferredSharedMemoryCarveout is considered a hint by the driver; the driver may choose a diferent configuration, if needed.

Devices of compute capability 8.0 and 8.7 allow a single thread block to address up to 163 KB of shared memory, while devices of compute capabilities 8.6 and 8.9 allow up to 99 KB of shared memory. Kernels relying on shared memory allocations over 48 KB per block are architecture-specific, and must use dynamic shared memory rather than statically sized shared memory arrays. These kernels require an explicit opt-in by using cudaFuncSetAttribute() to set the cudaFuncAttributeMaxDynamic-SharedMemorySize; see Shared Memory for the NVIDIA Volta GPU Architecture.

Note that the maximum amount of shared memory per thread block is smaller than the maximum shared memory partition available per SM. The 1 KB of shared memory not made available to a thread block is reserved for system use.
````
