# Warp Reduce Functions (__reduce_sync)

The `__reduce_sync` intrinsics perform a reduction operation on the data provided in `value` after synchronizing threads named in `mask` [CUDA_C_Programming_Guide:L8633-L8633]. These functions are supported by devices of compute capability 8.x or higher [CUDA_C_Programming_Guide:L8635-L8635].

## Supported Operations

The template type `T` determines the supported operations:

*   **Arithmetic Operations**: For `add`, `min`, and `max`, `T` can be either `unsigned` or `signed` (specifically `int`) [CUDA_C_Programming_Guide:L8633-L8633].
*   **Logical Operations**: For `and`, `or`, and `xor`, `T` must be `unsigned` [CUDA_C_Programming_Guide:L8633-L8633].

### Function Signatures

**Arithmetic Reductions**

```c
unsigned __reduce_add_sync(unsigned mask, unsigned value);
unsigned __reduce_min_sync(unsigned mask, unsigned value);
unsigned __reduce_max_sync(unsigned mask, unsigned value);
int __reduce_add_sync(unsigned mask, int value);
int __reduce_min_sync(unsigned mask, int value);
int __reduce_max_sync(unsigned mask, int value);
```

These functions return the result of applying an arithmetic add, min, or max reduction operation on the values provided in `value` by each thread named in `mask` [CUDA_C_Programming_Guide:L8641-L8646][CUDA_C_Programming_Guide:L8658-L8658].

**Logical Reductions**

```c
unsigned __reduce_and_sync(unsigned mask, unsigned value);
unsigned __reduce_or_sync(unsigned mask, unsigned value);
unsigned __reduce_xor_sync(unsigned mask, unsigned value);
```

These functions return the result of applying a logical AND, OR, or XOR reduction operation on the values provided in `value` by each thread named in `mask` [CUDA_C_Programming_Guide:L8649-L8651][CUDA_C_Programming_Guide:L8662-L8662].

## Mask and Convergence

The `mask` indicates the threads participating in the call. A bit, representing the thread’s lane id, must be set for each participating thread to ensure they are properly converged before the intrinsic is executed by the hardware [CUDA_C_Programming_Guide:L8664-L8664].

*   Each calling thread must have its own bit set in the mask.
*   All non-exited threads named in `mask` must execute the same intrinsic with the same mask, or the result is undefined [CUDA_C_Programming_Guide:L8664-L8664].

## Memory Ordering

These intrinsics do not imply a memory barrier. They do not guarantee any memory ordering [CUDA_C_Programming_Guide:L8666-L8666].
