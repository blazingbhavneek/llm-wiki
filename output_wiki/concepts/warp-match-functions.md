# 10.20 Warp Match Functions

Warp match functions perform broadcast-and-compare operations of a variable between threads within a warp. Supported by compute capability 7.x+. Includes __match_any_sync and __match_all_sync. Requires mask parameter. Do not imply memory barriers.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8599-L8630

Citation: [CUDA_C_Programming_Guide:L8599-L8630]

````text

## 10.20. Warp Match Functions

\_\_match\_any\_sync and \_\_match\_all\_sync perform a broadcast-and-compare operation of a variable between threads within a warp.

Supported by devices of compute capability 7.x or higher.

## 10.20.1. Synopsis

```c
unsigned int __match_any_sync(unsigned mask, T value);
unsigned int __match_all_sync(unsigned mask, T value, int *pred);
```

T can be int, unsigned int, long, unsigned long, long long, unsigned long long, float or double.

## 10.20.2. Description

The \_\_match\_sync() intrinsics permit a broadcast-and-compare of a value value across threads in a warp after synchronizing threads named in mask.

## \_\_match\_any\_sync

Returns mask of threads that have same value of value in mask

## \_\_match\_all\_sync

Returns mask if all threads in mask have the same value for value; otherwise 0 is returned. Predicate pred is set to true if all threads in mask have the same value of value; otherwise the predicate is set to false.

The new \*\_sync match intrinsics take in a mask indicating the threads participating in the call. A bit, representing the thread’s lane id, must be set for each participating thread to ensure they are properly converged before the intrinsic is executed by the hardware. Each calling thread must have its own bit set in the mask and all non-exited threads named in mask must execute the same intrinsic with the same mask, or the result is undefined.

These intrinsics do not imply a memory barrier. They do not guarantee any memory ordering.
````
