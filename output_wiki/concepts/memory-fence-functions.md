# Memory Fence Functions

The CUDA programming model assumes a device with a weakly-ordered memory model, meaning the order in which a CUDA thread writes data to shared memory, global memory, page-locked host memory, or the memory of a peer device is not necessarily the order in which the data is observed being written by another CUDA or host thread [CUDA_C_Programming_Guide:L6862-L6898]. It is undefined behavior for two threads to read from or write to the same memory location without synchronization [CUDA_C_Programming_Guide:L6862-L6898].

Memory fence functions can be used to enforce a sequentially-consistent ordering on memory accesses. These functions differ in the scope in which the orderings are enforced but are independent of the accessed memory space (shared memory, global memory, page-locked host memory, and the memory of a peer device) [CUDA_C_Programming_Guide:L6862-L6898].

## __threadfence_block

The `__threadfence_block()` function is equivalent to `cuda::atomic_thread_fence(cuda::memory_order_seq_cst, cuda::thread_scope_block)` [CUDA_C_Programming_Guide:L6899-L6908]. It ensures that:

*   All writes to all memory made by the calling thread before the call to `__threadfence_block()` are observed by all threads in the block of the calling thread as occurring before all writes to all memory made by the calling thread after the call to `__threadfence_block()` [CUDA_C_Programming_Guide:L6899-L6908].
*   All reads from all memory made by the calling thread before the call to `__threadfence_block()` are ordered before all reads from all memory made by the calling thread after the call to `__threadfence_block()` [CUDA_C_Programming_Guide:L6899-L6908].

## __threadfence

The `__threadfence()` function is equivalent to `cuda::atomic_thread_fence(cuda::memory_order_seq_cst, cuda::thread_scope_device)` [CUDA_C_Programming_Guide:L6909-L6914]. It ensures that no writes to all memory made by the calling thread after the call to `__threadfence()` are observed by any thread in the device as occurring before any write to all memory made by the calling thread before the call to `__threadfence()` [CUDA_C_Programming_Guide:L6909-L6914].

## __threadfence_system

The `__threadfence_system()` function is equivalent to `cuda::atomic_thread_fence(cuda::memory_order_seq_cst, cuda::thread_scope_system)` [CUDA_C_Programming_Guide:L6915-L6922]. It ensures that all writes to all memory made by the calling thread before the call to `__threadfence_system()` are observed by all threads in the device, host threads, and all threads in peer devices as occurring before all writes to all memory made by the calling thread after the call to `__threadfence_system()` [CUDA_C_Programming_Guide:L6915-L6922].

`__threadfence_system()` is only supported by devices of compute capability 2.x and higher [CUDA_C_Programming_Guide:L6915-L6922].

## Example Usage

Consider the following code where thread 1 executes `writeXY()` and thread 2 executes `readXY()`:

```cpp
__device__ int X = 1, Y = 2;

__device__ void writeXY()
{
    X = 10;
    __threadfence();
    Y = 20;
}

__device__ void readXY()
{
    int B = Y;
    __threadfence();
    int A = X;
}
```

For this code, the following outcomes can be observed:

*   A equal to 1 and B equal to 2
*   A equal to 10 and B equal to 2
*   A equal to 10 and B equal to 20

The fourth outcome (A equal to 1 and B equal to 20) is not possible, because the first write must be visible before the second write [CUDA_C_Programming_Guide:L6923-L6953].

If thread 1 and 2 belong to the same block, it is enough to use `__threadfence_block()` [CUDA_C_Programming_Guide:L6923-L6953]. If thread 1 and 2 do not belong to the same block, `__threadfence()` must be used if they are CUDA threads from the same device and `__threadfence_system()` must be used if they are CUDA threads from two different devices [CUDA_C_Programming_Guide:L6923-L6953].

## See Also

*   [blockDim](concept/blockdim)
*   [threadIdx](concept/threadidx)
*   [warpSize](concept/warpsize)
