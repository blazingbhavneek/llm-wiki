# Compute Capability 7.x

Architecture specifications for Compute Capability 7.x (Volta/Turing) including Tensor Cores, unified data cache/shared memory partitioning, independent thread scheduling changes, __syncwarp() usage, and dynamic shared memory carveout via cudaFuncSetAttribute().

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L19659-L19846

Citation: [CUDA_C_Programming_Guide:L19659-L19846]

````text
## 20.6. Compute Capability 7.x

## 20.6.1. Architecture

## An SM consists of:

▶ 64 FP32 cores for single-precision arithmetic operations,

▶ 32 FP64 cores for double-precision arithmetic operations,<sup>28</sup>

▶ 64 INT32 cores for integer math,

▶ 8 mixed-precision Tensor Cores for deep learning matrix arithmetic

1 16 special function units for single-precision floating-point transcendental functions,

▶ 4 warp schedulers.

An SM statically distributes its warps among its schedulers. Then, at every instruction issue time, each scheduler issues one instruction for one of its assigned warps that is ready to execute, if any.

## An SM has:

a read-only constant cache that is shared by all functional units and speeds up reads from the constant memory space, which resides in device memory,

a unified data cache and shared memory with a total size of 128 KB (Volta) or 96 KB (Turing).

Shared memory is partitioned out of unified data cache, and can be configured to various sizes (See Shared Memory.) The remaining data cache serves as an L1 cache and is also used by the texture unit that implements the various addressing and data filtering modes mentioned in Texture and Surface Memory.

## 20.6.2. Independent Thread Scheduling

The NVIDIA Volta GPU Architecture introduces Independent Thread Scheduling among threads in a warp, enabling intra-warp synchronization patterns previously unavailable and simplifying code changes when porting CPU code. However, this can lead to a rather diferent set of threads participating in the executed code than intended if the developer made assumptions about warp-synchronicity of previous hardware architectures.

Below are code patterns of concern and suggested corrective actions for Volta-safe code.

1. For applications using warp intrinsics (\_\_shfl\*, \_\_any, \_\_all, \_\_ballot), it is necessary that developers port their code to the new, safe, synchronizing counterpart, with the \*\_sync sufix. The new warp intrinsics take in a mask of threads that explicitly define which lanes (threads of a warp) must participate in the warp intrinsic. See Warp Vote Functions and Warp Shufle Functions for details.

Since the intrinsics are available with CUDA 9.0+, (if necessary) code can be executed conditionally with the following preprocessor macro:

```c
#if defined(CUDART_VERSION) && CUDART_VERSION >= 9000
// *_sync intrinsic
#endif
```

These intrinsics are available on all architectures, not just NVIDIA Volta GPU Architecture or NVIDIA Turing GPU Architecture, and in most cases a single code-base will sufice for all architectures. Note, however, that for Pascal and earlier architectures, all threads in mask must execute the same warp intrinsic instruction in convergence, and the union of all values in mask must be equal to the warp’s active mask. The following code pattern is valid on NVIDIA Volta GPU Architecture, but not on Pascal or earlier architectures.

```lisp
if (tid % warpSize < 16) {
    ...
    float swapped = __shfl_xor_sync(0xffffffff, val, 16);
    ...
} else {
    ...
    float swapped = __shfl_xor_sync(0xffffffff, val, 16);
    ...
}
```

The replacement for \_\_ballot(1) is \_\_activemask(). Note that threads within a warp can diverge even within a single code path. As a result, \_\_activemask() and \_\_ballot(1) may return only a subset of the threads on the current code path. The following invalid code example sets bit i of output to 1 when data[i] is greater than threshold. \_\_activemask() is used in an attempt to enable cases where dataLen is not a multiple of 32.

```txt
// Sets bit in output[] to 1 if the correspond element in data[i]
// is greater than 'threshold', using 32 threads in a warp.

for (int i = warpLane; i < dataLen; i += warpSize) {
    unsigned active = __activemask();
    unsigned bitPack = __ballot_sync(active, data[i] > threshold);
    if (warpLane == 0) {
        output[i / 32] = bitPack;
    }
}
```

This code is invalid because CUDA does not guarantee that the warp will diverge ONLY at the loop condition. When divergence happens for other reasons, conflicting results will be computed for the same 32-bit output element by diferent subsets of threads in the warp. A correct code might use a non-divergent loop condition together with \_\_ballot\_sync() to safely enumerate the set of threads in the warp participating in the threshold calculation as follows.

```txt
for (int i = warpLane; i - warpLane < dataLen; i += warpSize) {
    unsigned active = __ballot_sync(0xFFFFFF, i < dataLen);
    if (i < dataLen) {
        unsigned bitPack = __ballot_sync(active, data[i] > threshold);
        if (warpLane == 0) {
            output[i / 32] = bitPack;
        }
    }
}
```

Discovery Pattern demonstrates a valid use case for \_\_activemask().

1. If applications have warp-synchronous codes, they will need to insert the new \_\_syncwarp() warp-wide barrier synchronization instruction between any steps where data is exchanged between threads via global or shared memory. Assumptions that code is executed in lockstep or that reads/writes from separate threads are visible across a warp without synchronization are invalid.

```lisp
__shared__ float s_buff[BLOCK_SIZE];
s_buff[tid] = val;
__syncthreads();

// Inter-warp reduction
for (int i = BLOCK_SIZE / 2; i >= 32; i /= 2) {
    if (tid < i) {
        s_buff[tid] += s_buff[tid+i];
    }
    __syncthreads();
}

// Intra-warp reduction
// Butterfly reduction simplifies syncwarp mask
if (tid < 32) {
    float temp;
    temp = s_buff[tid ^ 16]; __syncwarp();
    s_buff[tid] += temp;      __syncwarp();
    temp = s_buff[tid ^ 8]; __syncwarp();
    s_buff[tid] += temp;      __syncwarp();
    temp = s_buff[tid ^ 4]; __syncwarp();
    s_buff[tid] += temp;      __syncwarp();
    temp = s_buff[tid ^ 2]; __syncwarp();
    s_buff[tid] += temp;      __syncwarp();
}

if (tid == 0) {
    *output = s_buff[0] + s_buff[1];
}
__syncthreads();
```

2. Although \_\_syncthreads() has been consistently documented as synchronizing all threads in the thread block, Pascal and prior architectures could only enforce synchronization at the warp level. In certain cases, this allowed a barrier to succeed without being executed by every thread as long as at least some thread in every warp reached the barrier. Starting with NVIDIA Volta GPU Architecture, the CUDA built-in \_\_syncthreads() and PTX instruction bar.sync (and their derivatives) are enforced per thread and thus will not succeed until reached by all non-exited threads in the block. Code exploiting the previous behavior will likely deadlock and must be modified to ensure that all non-exited threads reach the barrier.

The racecheck and synccheck tools provided by compute-saniter can help with locating violations.

To aid migration while implementing the above-mentioned corrective actions, developers can opt-in to the Pascal scheduling model that does not support independent thread scheduling. See Application Compatibility for details.

## 20.6.3. Global Memory

Global memory behaves the same way as in devices of compute capability 5.x (See Global Memory).

## 20.6.4. Shared Memory

The amount of the unified data cache reserved for shared memory is configurable on a per kernel basis. For the Volta architecture (compute capability 7.0), the unified data cache has a size of 128 KB, and the shared memory capacity can be set to 0, 8, 16, 32, 64 or 96 KB. For the Turing architecture (compute capability 7.5), the unified data cache has a size of 96 KB, and the shared memory capacity can be set to either 32 KB or 64 KB. Unlike Kepler, the driver automatically configures the shared memory capacity for each kernel to avoid shared memory occupancy bottlenecks while also allowing concurrent execution with already launched kernels where possible. In most cases, the driver’s default behavior should provide optimal performance.

Because the driver is not always aware of the full workload, it is sometimes useful for applications to provide additional hints regarding the desired shared memory configuration. For example, a kernel with little or no shared memory use may request a larger carveout in order to encourage concurrent execution with later kernels that require more shared memory. The new cudaFuncSetAttribute() API allows applications to set a preferred shared memory capacity, or carveout, as a percentage of the maximum supported shared memory capacity (96 KB for Volta, and 64 KB for Turing).

cudaFuncSetAttribute() relaxes enforcement of the preferred shared capacity compared to the legacy cudaFuncSetCacheConfig() API introduced with Kepler. The legacy API treated shared memory capacities as hard requirements for kernel launch. As a result, interleaving kernels with diferent shared memory configurations would needlessly serialize launches behind shared memory reconfigurations. With the new API, the carveout is treated as a hint. The driver may choose a diferent configuration if required to execute the function or to avoid thrashing.

```lisp
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
```

(continues on next page)

(continued from previous page)

```typescript
// carveout = cudaSharedmemCarveoutMaxL1;      //    (0)
// carveout = cudaSharedmemCarveoutMaxShared; // (100)
cudaFuncSetAttribute(MyKernel, cudaFuncAttributePreferredSharedMemoryCarveout,
    carveout);
MyKernel <<<gridDim, BLOCK_DIM>>>(...);
```

In addition to an integer percentage, several convenience enums are provided as listed in the code comments above. Where a chosen integer percentage does not map exactly to a supported capacity (SM 7.0 devices support shared capacities of 0, 8, 16, 32, 64, or 96 KB), the next larger capacity is used. For instance, in the example above, 50% of the 96 KB maximum is 48 KB, which is not a supported shared memory capacity. Thus, the preference is rounded up to 64 KB.

Compute capability 7.x devices allow a single thread block to address the full capacity of shared memory: 96 KB on Volta, 64 KB on Turing. Kernels relying on shared memory allocations over 48 KB per block are architecture-specific, as such they must use dynamic shared memory (rather than statically sized arrays) and require an explicit opt-in using cudaFuncSetAttribute() as follows.

```txt
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

Otherwise, shared memory behaves the same way as for devices of compute capability 5.x (See Shared Memory).
````
