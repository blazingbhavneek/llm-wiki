# CUDA Synchronization Functions

CUDA provides several built-in functions to synchronize threads within a thread block or warp. These functions are essential for coordinating communication between threads, particularly when accessing shared or global memory to avoid data hazards.

## Block Synchronization

### __syncthreads()

```c
void __syncthreads();
```

`__syncthreads()` acts as a barrier that waits until all threads in the thread block have reached this point. Additionally, it ensures that all global and shared memory accesses made by these threads prior to the call to `__syncthreads()` are visible to all threads in the block [CUDA_C_Programming_Guide:L7017-L7056].

This function is used to coordinate communication between threads of the same block. When threads within a block access the same addresses in shared or global memory, potential read-after-write, write-after-read, or write-after-write hazards may occur. Synchronizing threads between these accesses avoids such data hazards [CUDA_C_Programming_Guide:L7017-L7056].

**Constraints:**
*   `__syncthreads()` is allowed in conditional code, but only if the conditional evaluates identically across the entire thread block. If the condition varies across threads, the code execution is likely to hang or produce unintended side effects [CUDA_C_Programming_Guide:L7017-L7056].

## Block Synchronization with Predicates

Devices with compute capability 2.x and higher support three variations of `__syncthreads()` that evaluate a predicate for all threads in the block [CUDA_C_Programming_Guide:L7017-L7056].

### __syncthreads_count()

```c
int __syncthreads_count(int predicate);
```

This function is identical to `__syncthreads()` with the additional feature that it evaluates `predicate` for all threads of the block and returns the number of threads for which the predicate evaluates to non-zero [CUDA_C_Programming_Guide:L7017-L7056].

### __syncthreads_and()

```c
int __syncthreads_and(int predicate);
```

This function is identical to `__syncthreads()` with the additional feature that it evaluates `predicate` for all threads of the block and returns non-zero if and only if the predicate evaluates to non-zero for all of them [CUDA_C_Programming_Guide:L7017-L7056].

### __syncthreads_or()

```c
int __syncthreads_or(int predicate);
```

This function is identical to `__syncthreads()` with the additional feature that it evaluates `predicate` for all threads of the block and returns non-zero if and only if the predicate evaluates to non-zero for any of them [CUDA_C_Programming_Guide:L7017-L7056].

## Warp Synchronization

### __syncwarp()

```c
void __syncwarp(unsigned mask=0xffffffff);
```

`__syncwarp()` causes the executing thread to wait until all warp lanes named in `mask` have executed a `__syncwarp()` (with the same mask) before resuming execution [CUDA_C_Programming_Guide:L7017-L7056].

**Requirements:**
*   Each calling thread must have its own bit set in the mask.
*   All non-exited threads named in the mask must execute a corresponding `__syncwarp()` with the same mask. If these conditions are not met, the result is undefined [CUDA_C_Programming_Guide:L7017-L7056].

**Memory Ordering:**
Executing `__syncwarp()` guarantees memory ordering among threads participating in the barrier. Threads within a warp that wish to communicate via memory can store to memory, execute `__syncwarp()`, and then safely read values stored by other threads in the warp [CUDA_C_Programming_Guide:L7017-L7056].

**Target-Specific Behavior:**
For `.target sm_6x` or below, all threads in the mask must execute the same `__syncwarp()` in convergence, and the union of all values in the mask must be equal to the active mask. Otherwise, the behavior is undefined [CUDA_C_Programming_Guide:L7017-L7056].
