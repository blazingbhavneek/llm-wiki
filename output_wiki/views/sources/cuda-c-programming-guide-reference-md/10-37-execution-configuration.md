# 10.37. Execution Configuration

Part of [Cuda C Programming Guide Reference](README.md). Source lines L11533-L11916.

- [Execution Configuration](../../../concepts/execution-configuration.md) — The execution configuration defines the grid and block dimensions, optional shared memory allocation, and stream for a __global__ function call.
- [__cluster_dims__](../../../concepts/cluster-dims.md) — A compile-time specifier for thread block cluster dimensions in CUDA kernels, available for Compute Capability 9.0 and above.
- [cudaLaunchKernelEx](../../../entities/cudalaunchkernelex.md)
- [__launch_bounds__](../../../concepts/launch-bounds.md) — The __launch_bounds__ qualifier allows developers to specify maximum threads per block, minimum blocks per multiprocessor, and maximum blocks per cluster to guide the compiler's register allocation and optimization heuristics.
- [__maxnreg__](../../../concepts/maxnreg.md) — The __maxnreg__ qualifier is a CUDA C++ function attribute used to specify the maximum number of registers to be allocated to a single thread, serving as a low-level performance tuning mechanism.
- [#pragma unroll](../../../concepts/pragma-unroll.md) — A compiler directive used to control the unrolling of loops in CUDA C/C++ code.
- [SIMD Video Instructions](../../../concepts/simd-video-instructions.md) — PTX ISA v3.0+ SIMD video instructions for 16-bit and 8-bit values.
- [Diagnostic Pragmas](../../../concepts/diagnostic-pragma.md) — Diagnostic pragmas in CUDA control the severity of compiler messages and manage state, with modern usage requiring the `nv_` prefix.
- [#pragma nv_abi](../../../concepts/nv-abi-pragma.md) — The #pragma nv_abi directive allows applications compiled in separate compilation mode to achieve performance similar to whole program compilation by specifying custom Application Binary Interface (ABI) properties.
