# Warp Shuffle Functions

Verbatim source-backed fallback page for Warp Shuffle Functions.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8668-L8813

Citation: [CUDA_C_Programming_Guide:L8668-L8813]

````text
## 10.22. Warp Shufle Functions

\_\_shfl\_sync, \_\_shfl\_up\_sync, \_\_shfl\_down\_sync, and \_\_shfl\_xor\_sync exchange a variable between threads within a warp.

Supported by devices of compute capability 5.0 or higher.

Deprecation Notice: \_\_shfl, \_\_shfl\_up, \_\_shfl\_down, and \_\_shfl\_xor have been deprecated in CUDA 9.0 for all devices.

Removal Notice: When targeting devices with compute capability 7.x or higher, \_\_shfl, \_\_shfl\_up, \_\_shfl\_down, and \_\_shfl\_xor are no longer available and their sync variants should be used instead.

## 10.22.1. Synopsis

```c
T __shfl_sync(unsigned mask, T var, int srcLane, int width=warpSize);
T __shfl_up_sync(unsigned mask, T var, unsigned int delta, int width=warpSize);
T __shfl_down_sync(unsigned mask, T var, unsigned int delta, int width=warpSize);
T __shfl_xor_sync(unsigned mask, T var, int laneMask, int width=warpSize);
```

T can be int, unsigned int, long, unsigned long, long long, unsigned long long, float or double. With the cuda\_fp16.h header included, T can also be \_\_half or \_\_half2. Similarly, with the cuda\_bf16.h header included, T can also be \_\_nv\_bfloat16 or \_\_nv\_bfloat162.

## 10.22.2. Description

The \_\_shfl\_sync() intrinsics permit exchanging of a variable between threads within a warp without use of shared memory. The exchange occurs simultaneously for all active threads within the warp (and named in mask), moving 4 or 8 bytes of data per thread depending on the type.

Threads within a warp are referred to as lanes, and may have an index between 0 and warpSize-1 (inclusive). Four source-lane addressing modes are supported:

\_\_shfl\_sync()

Direct copy from indexed lane

\_\_shfl\_up\_sync()

Copy from a lane with lower ID relative to caller

\_\_shfl\_down\_sync()

Copy from a lane with higher ID relative to caller

\_\_shfl\_xor\_sync()

Copy from a lane based on bitwise XOR of own lane ID

Threads may only read data from another thread which is actively participating in the \_\_shfl\_sync() command. If the target thread is inactive, the retrieved value is undefined.

All of the \_\_shfl\_sync() intrinsics take an optional width parameter which alters the behavior of the intrinsic. width must have a value which is a power of two in the range [1, warpSize] (i.e., 1, 2, 4, 8, 16 or 32). Results are undefined for other values.

\_\_shfl\_sync() returns the value of var held by the thread whose ID is given by srcLane. If width is less than warpSize then each subsection of the warp behaves as a separate entity with a starting logical lane ID of 0. If srcLane is outside the range [0:width-1], the value returned corresponds to the value of var held by the srcLane modulo width (i.e. within the same subsection).

\_shfl\_up\_sync() calculates a source lane ID by subtracting delta from the caller’s lane ID. The value of var held by the resulting lane ID is returned: in efect, var is shifted up the warp by delta lanes. If width is less than warpSize then each subsection of the warp behaves as a separate entity with a starting logical lane ID of 0. The source lane index will not wrap around the value of width, so efectively the lower delta lanes will be unchanged.

\_\_shfl\_down\_sync() calculates a source lane ID by adding delta to the caller’s lane ID. The value of var held by the resulting lane ID is returned: this has the efect of shifting var down the warp by delta lanes. If width is less than warpSize then each subsection of the warp behaves as a separate entity with a starting logical lane ID of 0. As for \_\_shfl\_up\_sync(), the ID number of the source lane will not wrap around the value of width and so the upper delta lanes will remain unchanged.

shfl\_xor\_sync() calculates a source line ID by performing a bitwise XOR of the caller’s lane ID with laneMask: the value of var held by the resulting lane ID is returned. If width is less than warpSize then each group of width consecutive threads are able to access elements from earlier groups of threads, however if they attempt to access elements from later groups of threads their own value of var will be returned. This mode implements a butterfly addressing pattern such as is used in tree reduction and broadcast.

The new \*\_sync shfl intrinsics take in a mask indicating the threads participating in the call. A bit, representing the thread’s lane id, must be set for each participating thread to ensure they are properly converged before the intrinsic is executed by the hardware. Each calling thread must have its own bit set in the mask and all non-exited threads named in mask must execute the same intrinsic with the same mask, or the result is undefined.

Threads may only read data from another thread which is actively participating in the \_\_shfl\_sync() command. If the target thread is inactive, the retrieved value is undefined.

These intrinsics do not imply a memory barrier. They do not guarantee any memory ordering.

## 10.22.3. Examples

## 10.22.3.1 Broadcast of a single value across a warp

```c
#include <stdio.h>

__global__ void bcast(int arg) {
    int laneId = threadIdx.x & 0x1f;
    int value;
    if (laneId == 0)          // Note unused variable for
        value = arg;         // all threads except lane 0
    value = __shfl_sync(0xffffffff, value, 0);   // Synchronize all threads in warp,
and get "value" from lane 0
    if (value != arg)
        printf("Thread %d failed.\n", threadIdx.x);
}

int main() {
    bcast<<< 1, 32 >>>(1234);
    cudaDeviceSynchronize();

    return 0;
}
```

## 10.22.3.2 Inclusive plus-scan across sub-partitions of 8 threads

```cpp
#include <stdio.h>

__global__ void scan4() {
    int laneId = threadIdx.x & 0x1f;
    // Seed sample starting value (inverse of lane ID)
    int value = 31 - laneId;

    // Loop to accumulate scan within my partition.
    // Scan requires log2(n) == 3 steps for 8 threads
    // It works by an accumulated sum up the warp
    // by 1, 2, 4, 8 etc. steps.
    for (int i=1; i<=4; i*=2) {
        // We do the __shfl_sync unconditionally so that we
        // can read even from threads which won't do a
        // sum, and then conditionally assign the result.
        int n = __shfl_up_sync(0xffffffff, value, i, 8);
        if ((laneId & 7) >= i)
            value += n;
    }

    printf("Thread %d final value = %d\n", threadIdx.x, value);
}

int main() {
    scan4<<< 1, 32 >>>();
    cudaDeviceSynchronize();

    return 0;
}
```

## 10.22.3.3 Reduction across a warp

```c
#include <stdio.h>

__global__ void warpReduce() {
    int laneId = threadIdx.x & 0x1f;
    // Seed starting value as inverse lane ID
    int value = 31 - laneId;

    // Use XOR mode to perform butterfly reduction
    for (int i=16; i>=1; i/=2)
        value += __shfl_xor_sync(0xffffffff, value, i, 32);

    // "value" now contains the sum across all threads
    printf("Thread %d final value = %d\n", threadIdx.x, value);
}

int main() {
    warpReduce<<< 1, 32 >>>();
    cudaDeviceSynchronize();

    return 0;
}
```
````
