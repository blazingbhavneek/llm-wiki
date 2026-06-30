# Memory Fence Functions

Explains __threadfence_block(), __threadfence(), and __threadfence_system() for enforcing sequentially-consistent memory ordering across different scopes (block, device, system) to prevent data races.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L6870-L6953

Citation: [CUDA_C_Programming_Guide:L6870-L6953]

````text
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
````
