# Cooperative Groups

Cooperative Groups is an extension to the CUDA programming model, introduced in CUDA 9, for organizing groups of communicating threads [CUDA_C_Programming_Guide:L11929-L11934]. It allows developers to express the granularity at which threads are communicating, helping them to express richer, more efficient parallel decompositions [CUDA_C_Programming_Guide:L11929-L11934].

## Motivation

Historically, the CUDA programming model provided a single, simple construct for synchronizing cooperating threads: a barrier across all threads of a thread block, implemented with the `__syncthreads()` intrinsic function [CUDA_C_Programming_Guide:L11929-L11934]. However, programmers often require the ability to define and synchronize groups of threads at other granularities to enable greater performance, design flexibility, and software reuse in the form of "collective" group-wide function interfaces [CUDA_C_Programming_Guide:L11929-L11934].

To express broader patterns of parallel interaction, many performance-oriented programmers resorted to writing their own ad hoc and unsafe primitives for synchronizing threads within a single warp, or across sets of thread blocks running on a single GPU [CUDA_C_Programming_Guide:L11929-L11934]. While these custom solutions often provided valuable performance improvements, they resulted in brittle code that is expensive to write, tune, and maintain over time and across GPU generations [CUDA_C_Programming_Guide:L11929-L11934]. Cooperative Groups addresses this by providing a safe and future-proof mechanism to enable performant code [CUDA_C_Programming_Guide:L11929-L11934].

## Programming Model Concept

The Cooperative Groups programming model describes synchronization patterns both within and across CUDA thread blocks [CUDA_C_Programming_Guide:L11959-L12007]. It provides the means for applications to define their own groups of threads, along with the interfaces to synchronize them [CUDA_C_Programming_Guide:L11959-L12007]. The model also provides new launch APIs that enforce certain restrictions, thereby guaranteeing that synchronization will work [CUDA_C_Programming_Guide:L11959-L12007]. These primitives enable new patterns of cooperative parallelism within CUDA, including producer-consumer parallelism, opportunistic parallelism, and global synchronization across the entire Grid [CUDA_C_Programming_Guide:L11959-L12007].

### Core Elements

The Cooperative Groups programming model consists of the following elements [CUDA_C_Programming_Guide:L11959-L12007]:

*   Data types for representing groups of cooperating threads;
*   Operations to obtain implicit groups defined by the CUDA launch API (e.g., thread blocks);
*   Collectives for partitioning existing groups into new groups;
*   Collective Algorithms for data movement and manipulation (e.g., `memcpy_async`, `reduce`, `scan`);
*   An operation to synchronize all threads within the group;
*   Operations to inspect the group properties;
*   Collectives that expose low-level, group-specific and often HW accelerated, operations.

### Group Objects

The main concept in Cooperative Groups is that of objects naming the set of threads that are part of a group [CUDA_C_Programming_Guide:L11959-L12007]. This expression of groups as first-class program objects improves software composition, since collective functions can receive an explicit object representing the group of participating threads [CUDA_C_Programming_Guide:L11959-L12007]. This object also makes programmer intent explicit, which eliminates unsound architectural assumptions that result in brittle code, undesirable restrictions upon compiler optimizations, and better compatibility with new GPU generations [CUDA_C_Programming_Guide:L11959-L12007].

To write efficient code, it is best to use specialized groups (as going generic loses a lot of compile time optimizations) and pass these group objects by reference to functions that intend to use these threads in some cooperative fashion [CUDA_C_Programming_Guide:L11959-L12007].

## Usage and Implementation

Cooperative Groups requires CUDA 9.0 or later [CUDA_C_Programming_Guide:L11959-L12007]. To use Cooperative Groups, include the header file `cooperative_groups.h` and use the `cooperative_groups` namespace [CUDA_C_Programming_Guide:L11959-L12007].

```c
// Primary header is compatible with pre-C++11, collective algorithm headers require
// C++11
#include <cooperative_groups.h>
// Optionally include for memcpy_async() collective
#include <cooperative_groups/memcpy_async.h>
// Optionally include for reduce() collective
#include <cooperative_groups/reduce.h>
// Optionally include for inclusive_scan() and exclusive_scan() collectives
#include <cooperative_groups/scan.h>
```

```cpp
using namespace cooperative_groups;
// Alternatively use an alias to avoid polluting the namespace with collective
// algorithms
namespace cg = cooperative_groups;
```

The code can be compiled in a normal way using `nvcc`. However, if you wish to use `memcpy_async`, `reduce`, or `scan` functionality and your host compiler's default dialect is not C++11 or higher, you must add `--std=c++11` to the command line [CUDA_C_Programming_Guide:L11959-L12007].

## Composition Example

To illustrate the concept of groups, consider a block-wide sum reduction. Previously, there were hidden constraints on the implementation when writing code using `__syncthreads()` [CUDA_C_Programming_Guide:L12008-L12049].

```lisp
__device__ int sum(int *x, int n) {
    // ...
    __syncthreads();
    return total;
}

__global__ void parallel_kernel(float *x) {
    // ...
    // Entire thread block must call sum
    sum(x, n);
}
```

In this example, all threads in the thread block must arrive at the `__syncthreads()` barrier, but this constraint is hidden from the developer who might want to use `sum(...)` [CUDA_C_Programming_Guide:L12008-L12049]. With Cooperative Groups, a better way of writing this would be to pass the group object explicitly [CUDA_C_Programming_Guide:L12008-L12049]:

```lisp
__device__ int sum(const thread_block& g, int *x, int n) {
    // ...
    g.sync();
    return total;
}

__global__ void parallel_kernel(...) {
    // ...
    // Entire thread block must call sum
    thread_block tb = this_thread_block();
    sum(tb, x, n);
    // ...
}
```

This approach makes the synchronization requirement explicit through the group object `tb` [CUDA_C_Programming_Guide:L12008-L12049].
