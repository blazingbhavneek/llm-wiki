# Compute Capability 8.x

Compute Capability 8.x devices belong to the NVIDIA Ampere architecture. The architecture defines specific Streaming Multiprocessor (SM) compositions, memory hierarchies, and shared memory configurations that vary between the 8.0, 8.6, 8.7, and 8.9 variants.

## Architecture

A Streaming Multiprocessor (SM) statically distributes its warps among its schedulers. At every instruction issue time, each scheduler issues one instruction for one of its assigned warps that is ready to execute, if any [CUDA_C_Programming_Guide:L19847-L19933].

### SM Composition

The functional unit composition of an SM depends on the specific compute capability version [CUDA_C_Programming_Guide:L19847-L19933]:

*   **FP32 Cores:**
    *   Compute Capability 8.0: 64 cores [CUDA_C_Programming_Guide:L19847-L19933].
    *   Compute Capability 8.6, 8.7, and 8.9: 128 cores [CUDA_C_Programming_Guide:L19847-L19933].
*   **FP64 Cores:**
    *   Compute Capability 8.0: 32 cores [CUDA_C_Programming_Guide:L19847-L19933].
    *   Compute Capability 8.6, 8.7, and 8.9: 2 cores [CUDA_C_Programming_Guide:L19847-L19933].
*   **INT32 Cores:** 64 cores for integer math [CUDA_C_Programming_Guide:L19847-L19933].
*   **Special Function Units:** 16 units for single-precision floating-point transcendental functions [CUDA_C_Programming_Guide:L19847-L19933].
*   **Warp Schedulers:** 4 schedulers [CUDA_C_Programming_Guide:L19847-L19933].
*   **Tensor Cores:**
    *   Compute Capability 8.0, 8.6, and 8.7: 4 mixed-precision Third-Generation Tensor Cores supporting half-precision (fp16), \_\_nv\_bfloat16, tf32, sub-byte, and double precision (fp64) matrix arithmetic [CUDA_C_Programming_Guide:L19847-L19933].
    *   Compute Capability 8.9: 4 mixed-precision Fourth-Generation Tensor Cores supporting fp8, fp16, \_\_nv\_bfloat16, tf32, sub-byte, and fp64 [CUDA_C_Programming_Guide:L19847-L19933].

### Memory Hierarchy

Each SM includes a read-only constant cache shared by all functional units to speed up reads from the constant memory space in device memory [CUDA_C_Programming_Guide:L19847-L19933].

The SM also features a unified data cache and shared memory with a total size that varies by compute capability [CUDA_C_Programming_Guide:L19847-L19933]:

*   **Compute Capability 8.0 and 8.7:** 192 KB total (1.5x Volta’s 128 KB capacity) [CUDA_C_Programming_Guide:L19847-L19933].
*   **Compute Capability 8.6 and 8.9:** 128 KB total [CUDA_C_Programming_Guide:L19847-L19933].

Shared memory is partitioned out of the unified data cache. The remaining data cache serves as an L1 cache and is also used by the texture unit [CUDA_C_Programming_Guide:L19847-L19933].

## Global Memory

Global memory behaves the same way as for devices of compute capability 5.x [CUDA_C_Programming_Guide:L19847-L19933].

## Shared Memory Configuration

The amount of the unified data cache reserved for shared memory is configurable on a per-kernel basis [CUDA_C_Programming_Guide:L19847-L19933].

### Carveout Sizes

The shared memory capacity can be set to specific values depending on the compute capability [CUDA_C_Programming_Guide:L19847-L19933]:

*   **Compute Capability 8.0 and 8.7:** 0, 8, 16, 32, 64, 100, 132, or 164 KB [CUDA_C_Programming_Guide:L19847-L19933].
*   **Compute Capability 8.6 and 8.9:** 0, 8, 16, 32, 64, or 100 KB [CUDA_C_Programming_Guide:L19847-L19933].

### Configuration API

An application can set the preferred shared memory capacity (carveout) using `cudaFuncSetAttribute()` [CUDA_C_Programming_Guide:L19847-L19933]:

```c
cudaFuncSetAttribute(kernel_name, cudaFuncAttributePreferredSharedMemoryCarveout, carveout);
```

The API can specify the carveout either as an integer percentage of the maximum supported shared memory capacity (164 KB for 8.0/8.7 and 100 KB for 8.6/8.9) or as one of the following values: `cudaSharedmemCarveoutDefault`, `cudaSharedmemCarveoutMaxL1`, or `cudaSharedmemCarveoutMaxShared` [CUDA_C_Programming_Guide:L19847-L19933]. When using a percentage, the carveout is rounded up to the nearest supported shared memory capacity (e.g., 50% for compute capability 8.0 maps to 100 KB instead of 82 KB) [CUDA_C_Programming_Guide:L19847-L19933]. Setting `cudaFuncAttributePreferredSharedMemoryCarveout` is considered a hint by the driver; the driver may choose a different configuration if needed [CUDA_C_Programming_Guide:L19847-L19933].

### Thread Block Limits

*   **Compute Capability 8.0 and 8.7:** A single thread block can address up to 163 KB of shared memory [CUDA_C_Programming_Guide:L19847-L19933].
*   **Compute Capability 8.6 and 8.9:** A single thread block can address up to 99 KB of shared memory [CUDA_C_Programming_Guide:L19847-L19933].

The maximum amount of shared memory per thread block is smaller than the maximum shared memory partition available per SM; the 1 KB of shared memory not made available to a thread block is reserved for system use [CUDA_C_Programming_Guide:L19847-L19933].

Kernels relying on shared memory allocations over 48 KB per block are architecture-specific and must use dynamic shared memory rather than statically sized shared memory arrays. These kernels require an explicit opt-in by using `cudaFuncSetAttribute()` to set the `cudaFuncAttributeMaxDynamicSharedMemorySize` [CUDA_C_Programming_Guide:L19847-L19933].
