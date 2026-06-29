# Memory Fences and Synchronization in CUDA

Memory fences and synchronization primitives in CUDA are essential for coordinating data access between threads, particularly when threads consume data produced by other threads across different execution blocks. These mechanisms ensure that memory operations occur in the correct order and that their results are visible to other threads at the appropriate time.

## Memory Fence Functions

Memory fence functions, such as `__threadfence()`, affect the ordering of memory operations issued by a thread. They ensure that memory writes issued before the fence are globally visible (or visible to other blocks, depending on the scope) before memory writes issued after the fence. However, memory fences do not, by themselves, ensure that memory operations are visible to other threads; they only enforce ordering [CUDA_C_Programming_Guide:L6954-L7016].

For example, if a thread stores a result to global memory and then increments an atomic counter to signal completion, a fence is required between the store and the increment. Without the fence, the counter might increment before the partial sum is stored, causing a consumer thread to read stale or incomplete data [CUDA_C_Programming_Guide:L6954-L7016].

## Synchronization Functions

Synchronization functions, such as `__syncthreads()`, ensure that all threads within a block reach a specific point in execution before any of them proceed. This guarantees that memory operations performed by any thread in the block before the barrier are visible to all other threads in the block after the barrier [CUDA_C_Programming_Guide:L6954-L7016].

While `__syncthreads()` ensures visibility within a block, it does not synchronize across blocks. For cross-block synchronization, memory fences combined with atomic operations are typically used.

## Cross-Block Coordination Example

A common use case for combining memory fences and synchronization is when threads in one block consume data produced by threads in other blocks. Consider a kernel that computes the sum of an array of N numbers. Each block computes a partial sum and stores it in global memory. To determine which block is the last to finish, each block atomically increments a global counter. The last block is identified as the one that receives a counter value equal to `gridDim.x - 1` [CUDA_C_Programming_Guide:L6954-L7016].

The following code snippet illustrates this pattern:

```lisp
__device__ unsigned int count = 0;
__shared__ bool isLastBlockDone;
__global__ void sum(const float* array, unsigned int N,
                             volatile float* result)
{
    // Each block sums a subset of the input array.
    float partialSum = calculatePartialSum(array, N);

    if (threadIdx.x == 0) {

        // Thread 0 of each block stores the partial sum
        // to global memory. The compiler will use
        // a store operation that bypasses the L1 cache
        // since the "result" variable is declared as
        // volatile. This ensures that the threads of
        // the last block will read the correct partial
        // sums computed by all other blocks.
        result[blockIdx.x] = partialSum;

        // Thread 0 makes sure that the incrementing
        // of the "count" variable is only performed after
        // the partial sum has been written to global memory.
        __threadfence();

        // Thread 0 signals that it is done.
        unsigned int value = atomicInc(&count, gridDim.x);

        // Thread 0 determines if its block is the last
        // block to be done.
        isLastBlockDone = (value == (gridDim.x - 1));
    }

    // Synchronize to make sure that each thread reads
    // the correct value of isLastBlockDone.
    __syncthreads();

    if (isLastBlockDone) {

        // The last block sums the partial sums
        // stored in result[0 .. gridDim.x-1]
        float totalSum = calculateTotalSum(result);

        if (threadIdx.x == 0) {

            // Thread 0 of last block stores the total sum
            // to global memory and resets the count
            // variable, so that the next kernel call
            // works properly.
            result[0] = totalSum;
            count = 0;
        }
    }
}
```

In this example:
1. **Volatile Qualifier**: The `result` variable is declared as `volatile` to ensure that the store operation bypasses the L1 cache and writes directly to global memory, ensuring visibility to other blocks [CUDA_C_Programming_Guide:L6954-L7016].
2. **Memory Fence**: `__threadfence()` is called after storing the partial sum but before incrementing the atomic counter. This ensures that the partial sum is visible to other blocks before the counter is incremented [CUDA_C_Programming_Guide:L6954-L7016].
3. **Atomic Counter**: `atomicInc` is used to signal completion. The block that receives the value `gridDim.x - 1` is the last one to finish [CUDA_C_Programming_Guide:L6954-L7016].
4. **Block Synchronization**: `__syncthreads()` ensures that all threads in the block see the correct value of `isLastBlockDone` before proceeding [CUDA_C_Programming_Guide:L6954-L7016].

## Key Considerations

- **Visibility vs. Ordering**: Memory fences ensure ordering of memory operations by a thread but do not guarantee visibility to other threads. Visibility across blocks often requires additional mechanisms such as the `volatile` qualifier or specific memory scopes [CUDA_C_Programming_Guide:L6954-L7016].
- **Atomic Operations**: Atomic functions are commonly used in conjunction with memory fences to coordinate state changes across blocks, such as incrementing a completion counter [CUDA_C_Programming_Guide:L6954-L7016].
- **Cache Behavior**: Using `volatile` can force memory operations to bypass caches, ensuring that data is written to global memory immediately, which is critical for cross-block communication [CUDA_C_Programming_Guide:L6954-L7016].

## References

- CUDA C Programming Guide: Memory Fences and Synchronization [CUDA_C_Programming_Guide:L6954-L7016]
