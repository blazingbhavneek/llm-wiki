# 10.19 Warp Vote Functions

Warp vote functions allow threads in a warp to perform reduction-and-broadcast operations on integer predicates. Includes __all_sync, __any_sync, __ballot_sync, and __activemask. Requires mask parameter specifying participating threads. Do not imply memory barriers.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8562-L8598

Citation: [CUDA_C_Programming_Guide:L8562-L8598]

````text

## 10.19. Warp Vote Functions

```c
int __all_sync(unsigned mask, int predicate);
int __any_sync(unsigned mask, int predicate);
unsigned __ballot_sync(unsigned mask, int predicate);
unsigned __activemask();
```

Deprecation notice: \_\_any, \_\_all, and \_\_ballot have been deprecated in CUDA 9.0 for all devices.

Removal notice: When targeting devices with compute capability 7.x or higher, \_\_any, \_\_all, and \_\_ballot are no longer available and their sync variants should be used instead.

The warp vote functions allow the threads of a given warp to perform a reduction-and-broadcast operation. These functions take as input an integer predicate from each thread in the warp and compare those values with zero. The results of the comparisons are combined (reduced) across the active threads of the warp in one of the following ways, broadcasting a single return value to each participating thread:

## \_\_all\_sync(unsigned mask, predicate):

Evaluate predicate for all non-exited threads in mask and return non-zero if and only if predicate evaluates to non-zero for all of them.

## \_\_any\_sync(unsigned mask, predicate):

Evaluate predicate for all non-exited threads in mask and return non-zero if and only if predicate evaluates to non-zero for any of them.

## \_\_ballot\_sync(unsigned mask, predicate):

Evaluate predicate for all non-exited threads in mask and return an integer whose Nth bit is set if and only if predicate evaluates to non-zero for the Nth thread of the warp and the Nth thread is active.

## \_\_activemask():

Returns a 32-bit integer mask of all currently active threads in the calling warp. The Nth bit is set if the Nth lane in the warp is active when \_\_activemask() is called. Inactive threads are represented by 0 bits in the returned mask. Threads which have exited the program are always marked as inactive. Note that threads that are convergent at an \_\_activemask() call are not guaranteed to be convergent at subsequent instructions unless those instructions are synchronizing warp-builtin functions.

For \_\_all\_sync, \_\_any\_sync, and \_\_ballot\_sync, a mask must be passed that specifies the threads participating in the call. A bit, representing the thread’s lane ID, must be set for each participating thread to ensure they are properly converged before the intrinsic is executed by the hardware.

Each calling thread must have its own bit set in the mask and all non-exited threads named in mask must execute the same intrinsic with the same mask, or the result is undefined.

These intrinsics do not imply a memory barrier. They do not guarantee any memory ordering.
````
