# SIMT Architecture and Warps

Single Instruction, Multiple Threads (SIMT) is a parallel computing model where threads execute in groups of 32 parallel threads called **warps** [CUDA_C_Programming_Guide:L6136-L6156]. The term "warp" originates from weaving, the first parallel thread technology [CUDA_C_Programming_Guide:L6136-L6156].

## Warp Structure and Scheduling

The multiprocessor creates, manages, schedules, and executes threads in groups of 32 parallel threads called warps [CUDA_C_Programming_Guide:L6136-L6156]. When a multiprocessor is given one or more thread blocks to execute, it partitions them into warps, and each warp is scheduled by a warp scheduler for execution [CUDA_C_Programming_Guide:L6136-L6156].

### Thread Partitioning

The partitioning of a block into warps is deterministic: each warp contains threads of consecutive, increasing thread IDs, with the first warp containing thread 0 [CUDA_C_Programming_Guide:L6136-L6156]. Individual threads composing a warp start together at the same program address, but they have their own instruction address counter and register state, allowing them to branch and execute independently [CUDA_C_Programming_Guide:L6136-L6156].

Sub-units of a warp include:
*   **Half-warp**: Either the first or second half of a warp (16 threads) [CUDA_C_Programming_Guide:L6136-L6156].
*   **Quarter-warp**: Either the first, second, third, or fourth quarter of a warp (8 threads) [CUDA_C_Programming_Guide:L6136-L6156].

### Active and Inactive Threads

Threads participating in the current instruction are called **active threads**, while threads not on the current instruction are **inactive** (disabled) [CUDA_C_Programming_Guide:L6136-L6156]. Threads may become inactive for several reasons:
*   Exiting earlier than other threads in their warp [CUDA_C_Programming_Guide:L6136-L6156].
*   Taking a different branch path than the one currently executed by the warp [CUDA_C_Programming_Guide:L6136-L6156].
*   Being the last threads of a block where the total number of threads is not a multiple of the warp size [CUDA_C_Programming_Guide:L6136-L6156].

## SIMT vs. SIMD

The SIMT architecture is akin to SIMD (Single Instruction, Multiple Data) vector organizations in that a single instruction controls multiple processing elements [CUDA_C_Programming_Guide:L6136-L6156]. However, key differences exist:
*   **SIMD**: Exposes the SIMD width to the software; software must coalesce loads into vectors and manage divergence manually [CUDA_C_Programming_Guide:L6136-L6156].
*   **SIMT**: Instructions specify the execution and branching behavior of a single thread, enabling programmers to write thread-level parallel code for independent, scalar threads, as well as data-parallel code for coordinated threads [CUDA_C_Programming_Guide:L6136-L6156].

For correctness, programmers can essentially ignore SIMT behavior, but substantial performance improvements are realized by ensuring code seldom requires threads in a warp to diverge, analogous to considering cache line sizes in traditional code for peak performance [CUDA_C_Programming_Guide:L6136-L6156].

## Branch Divergence

A warp executes one common instruction at a time, so full efficiency is realized when all 32 threads of a warp agree on their execution path [CUDA_C_Programming_Guide:L6136-L6156]. If threads of a warp diverge via a data-dependent conditional branch, the warp executes each branch path taken, disabling threads that are not on that path [CUDA_C_Programming_Guide:L6136-L6156].

Branch divergence occurs only within a warp; different warps execute independently regardless of whether they are executing common or disjoint code paths [CUDA_C_Programming_Guide:L6136-L6156].

## Evolution: Independent Thread Scheduling

### Pre-Volta Architecture

Prior to NVIDIA Volta, warps used a single program counter shared amongst all 32 threads in the warp, together with an active mask specifying the active threads [CUDA_C_Programming_Guide:L6136-L6156]. This architecture meant that threads from the same warp in divergent regions or different states of execution could not signal each other or exchange data [CUDA_C_Programming_Guide:L6136-L6156]. Algorithms requiring fine-grained sharing of data guarded by locks or mutexes could easily lead to deadlock, depending on which warp the contending threads came from [CUDA_C_Programming_Guide:L6136-L6156].

### Volta Architecture and Beyond

Starting with the NVIDIA Volta architecture, **Independent Thread Scheduling** allows full concurrency between threads, regardless of warp [CUDA_C_Programming_Guide:L6136-L6156]. Key features include:
*   The GPU maintains execution state per thread, including a program counter and call stack [CUDA_C_Programming_Guide:L6136-L6156].
*   Execution can be yielded at a per-thread granularity, either to make better use of execution resources or to allow one thread to wait for data produced by another [CUDA_C_Programming_Guide:L6136-L6156].
*   A schedule optimizer determines how to group active threads from the same warp together into SIMT units, retaining high throughput while allowing divergence and reconvergence at sub-warp granularity [CUDA_C_Programming_Guide:L6136-L6156].

#### Implications for Developers

Independent Thread Scheduling can lead to a different set of threads participating in executed code than intended if the developer made assumptions about warp-synchronicity of previous hardware architectures [CUDA_C_Programming_Guide:L6136-L6156]. In particular, any warp-synchronous code (such as synchronization-free, intra-warp reductions) should be revisited to ensure compatibility with NVIDIA Volta and beyond [CUDA_C_Programming_Guide:L6136-L6156]. See Compute Capability 7.x for further details [CUDA_C_Programming_Guide:L6136-L6156].

## Memory Access Behavior

### Non-Atomic Writes

If a non-atomic instruction executed by a warp writes to the same location in global or shared memory for more than one of the threads of the warp, the number of serialized writes that occur to that location varies depending on the compute capability of the device (see Compute Capability 5.x, Compute Capability 6.x, and Compute Capability 7.x), and which thread performs the final write is undefined [CUDA_C_Programming_Guide:L6136-L6156].

### Atomic Instructions

If an atomic instruction executed by a warp reads, modifies, and writes to the same location in global memory for more than one of the threads of the warp, each read/modify/write to that location occurs and they are all serialized, but the order in which they occur is undefined [CUDA_C_Programming_Guide:L6136-L6156].

## References

*   [CUDA_C_Programming_Guide:L6136-L6156] CUDA C++ Programming Guide: Thread Hierarchy and SIMT Architecture.
