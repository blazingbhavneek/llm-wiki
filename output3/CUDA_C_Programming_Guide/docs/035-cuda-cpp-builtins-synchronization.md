
Built-in variables specify the grid and block dimensions and the block and thread indices. They are only valid within functions that are executed on the device.

## 10.4.1. gridDim

This variable is of type dim3 (see dim3) and contains the dimensions of the grid.

## 10.4.2. blockIdx

This variable is of type uint3 (see char, short, int, long, longlong, float, double) and contains the block index within the grid.

## 10.4.3. blockDim

This variable is of type dim3 (see dim3) and contains the dimensions of the block.

## 10.4.4. threadIdx

This variable is of type uint3 (see char, short, int, long, longlong, float, double) and contains the thread index within the block.

## 10.4.5. warpSize

This variable is of type int and contains the warp size in threads (see SIMT Architecture for the definition of a warp).

## 10.5. Memory Fence Functions

The CUDA programming model assumes a device with a weakly-ordered memory model, that is the order in which a CUDA thread writes data to shared memory, global memory, page-locked host memory, or the memory of a peer device is not necessarily the order in which the data is observed being written by another CUDA or host thread. It is undefined behavior for two threads to read from or write to the same memory location without synchronization.

In the following example, thread 1 executes writeXY(), while thread 2 executes readXY().

```txt
__device__ int X = 1, Y = 2;

__device__ void writeXY()
{
    X = 10;
    Y = 20;
}

__device__ void readXY()
{
    int B = Y;
    int A = X;
}
```

The two threads read and write from the same memory locations X and Y simultaneously. Any datarace is undefined behavior, and has no defined semantics. The resulting values for A and B can be anything.

Memory fence functions can be used to enforce a sequentially-consistent ordering on memory accesses. The memory fence functions difer in the scope in which the orderings are enforced but they are independent of the accessed memory space (shared memory, global memory, page-locked host memory, and the memory of a peer device).

```javascript
void __threadfence_block();
```

is equivalent to cuda::atomic\_thread\_fence(cuda::memory\_order\_seq\_cst, cuda::thread\_scope\_block) and ensures that:

All writes to all memory made by the calling thread before the call to \_\_threadfence\_block() are observed by all threads in the block of the calling thread as occurring before all writes to all memory made by the calling thread after the call to \_\_threadfence\_block();

▶ All reads from all memory made by the calling thread before the call to \_\_threadfence\_block() are ordered before all reads from all memory made by the calling thread after the call to \_\_threadfence\_block().

```javascript
void __threadfence();
```

is equivalent to cuda::atomic\_thread\_fence(cuda::memory\_order\_seq\_cst, cuda::thread\_scope\_device) and ensures that no writes to all memory made by the calling thread after the call to \_\_threadfence() are observed by any thread in the device as occurring before any write to all memory made by the calling thread before the call to \_\_threadfence().

```javascript
void __threadfence_system();
```

is equivalent to cuda::atomic\_thread\_fence(cuda::memory\_order\_seq\_cst, cuda::thread\_scope\_system) and ensures that all writes to all memory made by the calling thread before the call to \_\_threadfence\_system() are observed by all threads in the device, host threads, and all threads in peer devices as occurring before all writes to all memory made by the calling thread after the call to \_\_threadfence\_system().

\_\_threadfence\_system() is only supported by devices of compute capability 2.x and higher.

In the previous code sample, we can insert fences in the codes as follows:

```lisp
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

▶ A equal to 1 and B equal to 2,

▶ A equal to 10 and B equal to 2,

A equal to 10 and B equal to 20.

The fourth outcome is not possible, because the first write must be visible before the second write. If thread 1 and 2 belong to the same block, it is enough to use \_\_threadfence\_block(). If thread 1 and 2 do not belong to the same block, \_\_threadfence() must be used if they are CUDA threads from the same device and \_\_threadfence\_system() must be used if they are CUDA threads from two diferent devices.

A common use case is when threads consume some data produced by other threads as illustrated by the following code sample of a kernel that computes the sum of an array of N numbers in one call. Each block first sums a subset of the array and stores the result in global memory. When all blocks are done, the last block done reads each of these partial sums from global memory and sums them to obtain the final result. In order to determine which block is finished last, each block atomically increments a counter to signal that it is done with computing and storing its partial sum (see Atomic Functions about atomic functions). The last block is the one that receives the counter value equal to gridDim. x-1. If no fence is placed between storing the partial sum and incrementing the counter, the counter might increment before the partial sum is stored and therefore, might reach gridDim.x-1 and let the last block start reading partial sums before they have been actually updated in memory.

Memory fence functions only afect the ordering of memory operations by a thread; they do not, by themselves, ensure that these memory operations are visible to other threads (like \_\_syncthreads() does for threads within a block; see Synchronization Functions). In the code sample below, the visibility of memory operations on the result variable is ensured by declaring it as volatile (see Volatile Qualifier).

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
```

```txt
// works properly.
result[0] = totalSum;
count = 0;
}
}
}
```

## 10.6. Synchronization Functions

```javascript
void __syncthreads();
```

waits until all threads in the thread block have reached this point and all global and shared memory accesses made by these threads prior to \_\_syncthreads() are visible to all threads in the block.

\_syncthreads() is used to coordinate communication between the threads of the same block. When some threads within a block access the same addresses in shared or global memory, there are potential read-after-write, write-after-read, or write-after-write hazards for some of these memory accesses. These data hazards can be avoided by synchronizing threads in-between these accesses.

syncthreads() is allowed in conditional code but only if the conditional evaluates identically across the entire thread block, otherwise the code execution is likely to hang or produce unintended side efects.

Devices of compute capability 2.x and higher support three variations of \_\_syncthreads() described below.

```txt
int __syncthreads_count(int predicate);
```

is identical to \_\_syncthreads() with the additional feature that it evaluates predicate for all threads of the block and returns the number of threads for which predicate evaluates to non-zero.

int \_\_syncthreads\_and(int predicate);

is identical to \_\_syncthreads() with the additional feature that it evaluates predicate for all threads of the block and returns non-zero if and only if predicate evaluates to non-zero for all of them.

```txt
int __syncthreads_or(int predicate);
```

is identical to \_\_syncthreads() with the additional feature that it evaluates predicate for all threads of the block and returns non-zero if and only if predicate evaluates to non-zero for any of them.

```javascript
void __syncwarp(unsigned mask=0xffffffff);
```

will cause the executing thread to wait until all warp lanes named in mask have executed a \_\_syncwarp() (with the same mask) before resuming execution. Each calling thread must have its own bit set in the mask and all non-exited threads named in mask must execute a corresponding \_\_syncwarp() with the same mask, or the result is undefined.

Executing \_\_syncwarp() guarantees memory ordering among threads participating in the barrier. Thus, threads within a warp that wish to communicate via memory can store to memory, execute \_\_syncwarp(), and then safely read values stored by other threads in the warp.

Note: For .target sm\_6x or below, all threads in mask must execute the same \_\_syncwarp() in convergence, and the union of all values in mask must be equal to the active mask. Otherwise, the behavior is undefined.

## 10.7. Mathematical Functions
