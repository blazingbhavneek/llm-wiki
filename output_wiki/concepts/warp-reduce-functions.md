# Warp Reduce Functions

Verbatim source-backed fallback page for Warp Reduce Functions.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8631-L8667

Citation: [CUDA_C_Programming_Guide:L8631-L8667]

````text
## 10.21. Warp Reduce Functions

The \_\_reduce\_sync(unsigned mask, T value) intrinsics perform a reduction operation on the data provided in value after synchronizing threads named in mask. T can be unsigned or signed for {add, min, max} and unsigned only for {and, or, xor} operations.

Supported by devices of compute capability 8.x or higher.

## 10.21.1. Synopsis

```c
// add/min/max
unsigned __reduce_add_sync(unsigned mask, unsigned value);
unsigned __reduce_min_sync(unsigned mask, unsigned value);
unsigned __reduce_max_sync(unsigned mask, unsigned value);
int __reduce_add_sync(unsigned mask, int value);
int __reduce_min_sync(unsigned mask, int value);
int __reduce_max_sync(unsigned mask, int value);

// and/or/xor
unsigned __reduce_and_sync(unsigned mask, unsigned value);
unsigned __reduce_or_sync(unsigned mask, unsigned value);
unsigned __reduce_xor_sync(unsigned mask, unsigned value);
```

## 10.21.2. Description

## \_\_reduce\_add\_sync, \_\_reduce\_min\_sync, \_\_reduce\_max\_sync

Returns the result of applying an arithmetic add, min, or max reduction operation on the values provided in value by each thread named in mask

## \_\_reduce\_and\_sync, \_\_reduce\_or\_sync, \_\_reduce\_xor\_sync

Returns the result of applying a logical AND, OR, or XOR reduction operation on the values provided in value by each thread named in mask.

The mask indicates the threads participating in the call. A bit, representing the thread’s lane id, must be set for each participating thread to ensure they are properly converged before the intrinsic is executed by the hardware. Each calling thread must have its own bit set in the mask and all non-exited threads named in mask must execute the same intrinsic with the same mask, or the result is undefined.

These intrinsics do not imply a memory barrier. They do not guarantee any memory ordering.
````
