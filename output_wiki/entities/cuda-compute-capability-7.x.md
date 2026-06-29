# Compute Capability 7.x

Compute Capability 7.x refers to the GPU architectures introduced by NVIDIA, specifically the Volta architecture (Compute Capability 7.0) and the Turing architecture (Compute Capability 7.5) [CUDA_C_Programming_Guide:L19658-L19846]. These architectures introduced significant changes to the Streaming Multiprocessor (SM) design, including the introduction of Tensor Cores, Independent Thread Scheduling, and a unified data cache with configurable shared memory carveout [CUDA_C_Programming_Guide:L19658-L19846].

## Architecture

The Streaming Multiprocessor (SM) in Compute Capability 7.x devices consists of the following functional units [CUDA_C_Programming_Guide:L19658-L19846]:

*   64 FP32 cores for single-precision arithmetic operations [CUDA_C_Programming_Guide:L19658-L19846].
*   32 FP64 cores for double-precision arithmetic operations [CUDA_C_Programming_Guide:L19658-L19846].
*   64 INT32 cores for integer math [CUDA_C_Programming_Guide:L19658-L19846].
*   8 mixed-precision Tensor Cores for deep learning matrix arithmetic [CUDA_C_Programming_Guide:L19658-L19846].
*   16 special function units for single-precision floating-point transcendental functions [CUDA_C_Programming_Guide:L19658-L19846].
*   4 warp schedulers [CUDA_C_Programming_Guide:L19658-L19846].

An SM statically distributes its warps among its schedulers. At every instruction issue time, each scheduler issues one instruction for one of its assigned warps that is ready to execute, if any [CUDA_C_Programming_Guide:L19658-L19846].

The SM also includes a read-only constant cache shared by all functional units to speed up reads from the constant memory space in device memory [CUDA_C_Programming_Guide:L19658-L19846]. Additionally, it features a unified data cache and shared memory with a total size of 128 KB for Volta (CC 7.0) or 96 KB for Turing (CC 7.5) [CUDA_C_Programming_Guide:L19658-L19846]. Shared memory is partitioned out of the unified data cache and can be configured to various sizes [CUDA_C_Programming_Guide:L19658-L19846]. The remaining data cache serves as an L1 cache and is also used by the texture unit [CUDA_C_Programming_Guide:L19658-L19846].

## Independent Thread Scheduling

The NVIDIA Volta GPU Architecture introduces Independent Thread Scheduling among threads in a warp, enabling intra-warp synchronization patterns previously unavailable and simplifying code changes when porting CPU code [CUDA_C_Programming_Guide:L19658-L19846]. However, this can lead to a different set of threads participating in the executed code than intended if the developer made assumptions about warp-synchronicity of previous hardware architectures [CUDA_C_Programming_Guide:L19658-L19846].

### Warp Intrinsics

For applications using warp intrinsics (`__shfl*`, `__any`, `__all`, `__ballot`), it is necessary that developers port their code to the new, safe, synchronizing counterpart, with the `*_sync` suffix [CUDA_C_Programming_Guide:L19658-L19846]. The new warp intrinsics take in a mask of threads that explicitly define which lanes (threads of a warp) must participate in the warp intrinsic [CUDA_C_Programming_Guide:L19658-L19846].

Since the intrinsics are available with CUDA 9.0+, code can be executed conditionally with the following preprocessor macro [CUDA_C_Programming_Guide:L19658-L19846]:

```c
#if defined(CUDART_VERSION) && CUDART_VERSION >= 9000
// *_sync intrinsic
#endif
```

These intrinsics are available on all architectures, not just NVIDIA Volta GPU Architecture or NVIDIA Turing GPU Architecture, and in most cases a single code-base will suffice for all architectures [CUDA_C_Programming_Guide:L19658-L19846]. Note, however, that for Pascal and earlier architectures, all threads in mask must execute the same warp intrinsic instruction in convergence, and the union of all values in mask must be equal to the warp’s active mask [CUDA_C_Programming_Guide:L19658-L19846].

The replacement for `__ballot(1)` is `__activemask()` [CUDA_C_Programming_Guide:L19658-L19846]. Note that threads within a warp can diverge even within a single code path [CUDA_C_Programming_Guide:L19658-L19846]. As a result, `__activemask()` and `__ballot(1)` may return only a subset of the threads on the current code path [CUDA_C_Programming_Guide:L19658-L19846].

### Synchronization

If applications have warp-synchronous codes, they will need to insert the new `__syncwarp()` warp-wide barrier synchronization instruction between any steps where data is exchanged between threads via global or shared memory [CUDA_C_Programming_Guide:L19658-L19846]. Assumptions that code is executed in lockstep or that reads/writes from separate threads are visible across a warp without synchronization are invalid [CUDA_C_Programming_Guide:L19658-L19846].

Although `__syncthreads()` has been consistently documented as synchronizing all threads in the thread block, Pascal and prior architectures could only enforce synchronization at the warp level [CUDA_C_Programming_Guide:L19658-L19846]. In certain cases, this allowed a barrier to succeed without being executed by every thread as long as at least some thread in every warp reached the barrier [CUDA_C_Programming_Guide:L19658-L19846]. Starting with NVIDIA Volta GPU Architecture, the CUDA built-in `__syncthreads()` and PTX instruction `bar.sync` (and their derivatives) are enforced per thread and thus will not succeed until reached by all non-exited threads in the block [CUDA_C_Programming_Guide:L19658-L19846]. Code exploiting the previous behavior will likely deadlock and must be modified to ensure that all non-exited threads reach the barrier [CUDA_C_Programming_Guide:L19658-L19846].

To aid migration while implementing the above-mentioned corrective actions, developers can opt-in to the Pascal scheduling model that does not support independent thread scheduling [CUDA_C_Programming_Guide:L19658-L19846].

## Global Memory

Global memory behaves the same way as in devices of compute capability 5.x [CUDA_C_Programming_Guide:L19658-L19846].

## Shared Memory

The amount of the unified data cache reserved for shared memory is configurable on a per kernel basis [CUDA_C_Programming_Guide:L19658-L19846]. For the Volta architecture (compute capability 7.0), the unified data cache has a size of 128 KB, and the shared memory capacity can be set to 0, 8, 16, 32, 64 or 96 KB [CUDA_C_Programming_Guide:L19658-L19846]. For the Turing architecture (compute capability 7.5), the unified data cache has a size of 96 KB, and the shared memory capacity can be set to either 32 KB or 64 KB [CUDA_C_Programming_Guide:L19658-L19846].

Unlike Kepler, the driver automatically configures the shared memory capacity for each kernel to avoid shared memory occupancy bottlenecks while also allowing concurrent execution with already launched kernels where possible [CUDA_C_Programming_Guide:L19658-L19846]. In most cases, the driver’s default behavior should provide optimal performance [CUDA_C_Programming_Guide:L19658-L19846].

Because the driver is not always aware of the full workload, it is sometimes useful for applications to provide additional hints regarding the desired shared memory configuration [CUDA_C_Programming_Guide:L19658-L19846]. For example, a kernel with little or no shared memory use may request a larger carveout in order to encourage concurrent execution with later kernels that require more shared memory [CUDA_C_Programming_Guide:L19658-L19846]. The new `cudaFuncSetAttribute()` API allows applications to set a preferred shared memory capacity, or carveout, as a percentage of the maximum supported shared memory capacity (96 KB for Volta, and 64 KB for Turing) [CUDA_C_Programming_Guide:L19658-L19846].

`cudaFuncSetAttribute()` relaxes enforcement of the preferred shared capacity compared to the legacy `cudaFuncSetCacheConfig()` API introduced with Kepler [CUDA_C_Programming_Guide:L19658-L19846]. The legacy API treated shared memory capacities as hard requirements for kernel launch [CUDA_C_Programming_Guide:L19658-L19846]. As a result, interleaving kernels with different shared memory configurations would needlessly serialize launches behind shared memory reconfigurations [CUDA_C_Programming_Guide:L19658-L19846]. With the new API, the carveout is treated as a hint [CUDA_C_Programming_Guide:L19658-L19846]. The driver may choose a different configuration if required to execute the function or to avoid thrashing [CUDA_C_Programming_Guide:L19658-L19846].

```c
// Device code
__global__ void MyKernel(...)
{
    __shared__ float buffer[BLOCK_DIM];
    ...
}

// Host code
int carveout = 50; // prefer shared memory capacity 50% of maximum
// Named Carveout Values:
// carveout = cudaSharedmemCarveoutDefault;   //  (-1)
// carveout = cudaSharedmemCarveoutMaxL1;      //    (0)
// carveout = cudaSharedmemCarveoutMaxShared; // (100)
cudaFuncSetAttribute(MyKernel, cudaFuncAttributePreferredSharedMemoryCarveout,
    carveout);
MyKernel <<<gridDim, BLOCK_DIM>>>(...);
```

In addition to an integer percentage, several convenience enums are provided as listed in the code comments above [CUDA_C_Programming_Guide:L19658-L19846]. Where a chosen integer percentage does not map exactly to a supported capacity (SM 7.0 devices support shared capacities of 0, 8, 16, 32, 64, or 96 KB), the next larger capacity is used [CUDA_C_Programming_Guide:L19658-L19846]. For instance, in the example above, 50% of the 96 KB maximum is 48 KB, which is not a supported shared memory capacity [CUDA_C_Programming_Guide:L19658-L19846]. Thus, the preference is rounded up to 64 KB [CUDA_C_Programming_Guide:L19658-L19846].

Compute capability 7.x devices allow a single thread block to address the full capacity of shared memory: 96 KB on Volta, 64 KB on Turing [CUDA_C_Programming_Guide:L19658-L19846]. Kernels relying on shared memory allocations over 48 KB per block are architecture-specific, as such they must use dynamic shared memory (rather than statically sized arrays) and require an explicit opt-in using `cudaFuncSetAttribute()` as follows [CUDA_C_Programming_Guide:L19658-L19846]:

```c
// Device code
__global__ void MyKernel(...)
{
    extern __shared__ float buffer[];
    ...
}

// Host code
int maxbytes = 98304; // 96 KB
cudaFuncSetAttribute(MyKernel, cudaFuncAttributeMaxDynamicSharedMemorySize, maxbytes);
MyKernel <<<gridDim, blockDim, maxbytes>>>(...);
```

Otherwise, shared memory behaves the same way as for devices of compute capability 5.x [CUDA_C_Programming_Guide:L19658-L19846].
