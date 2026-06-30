# Synchronization Functions

Documentation for CUDA synchronization primitives including __syncthreads(), __syncthreads_count(), __syncthreads_and(), __syncthreads_or(), and __syncwarp(), detailing their behavior, usage constraints, and memory ordering guarantees.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L7017-L7057

Citation: [CUDA_C_Programming_Guide:L7017-L7057]

````text
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
````
