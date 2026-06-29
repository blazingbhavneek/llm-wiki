# memcpy_async

`memcpy_async` is a group-wide collective function that utilizes hardware-accelerated support for nonblocking memory transactions from global to shared memory [CUDA_C_Programming_Guide:L12632-L12677]. It is part of the `cooperative_groups` namespace and requires the inclusion of the `cooperative_groups/memcpy_async.h` header [CUDA_C_Programming_Guide:L12632-L12677].

## Overview

Given a set of threads named in a group, `memcpy_async` moves a specified amount of bytes or elements through a single pipeline stage [CUDA_C_Programming_Guide:L12632-L12677]. While it functions as a general memcpy, it is only asynchronous if the source is global memory and the destination is shared memory, and both can be addressed with 16, 8, or 4 byte alignments [CUDA_C_Programming_Guide:L12632-L12677].

To achieve best performance, an alignment of 16 bytes for both shared memory and global memory is required [CUDA_C_Programming_Guide:L12632-L12677]. Asynchronously copied data should only be read following a call to `wait` or `wait_prior`, which signals that the corresponding stage has completed moving data to shared memory [CUDA_C_Programming_Guide:L12632-L12677].

## Usage and Signatures

There are two primary usage patterns for `memcpy_async`:

### Usage 1: Shape-based Copy

```cpp
template <typename TyGroup, typename TyElem, typename TyShape>
void memcpy_async(
    const TyGroup &group,
    TyElem *__restrict__ _dst,
    const TyElem *__restrict__ _src,
    const TyShape &shape
);
```

This version performs a copy of `shape` bytes [CUDA_C_Programming_Guide:L12632-L12677].

### Usage 2: Layout-based Copy

```cpp
template <typename TyGroup, typename TyElem, typename TyDstLayout, typename
TySrcLayout>
void memcpy_async(
    const TyGroup &group,
    TyElem *__restrict__ dst,
    const TyDstLayout &dstLayout,
    const TyElem *__restrict__ src,
    const TySrcLayout &srcLayout
);
```

This version performs a copy of `min(dstLayout, srcLayout)` elements [CUDA_C_Programming_Guide:L12632-L12677]. If layouts are of type `cuda::aligned_size_t<N>`, both must specify the same alignment [CUDA_C_Programming_Guide:L12632-L12677].

### Layout and Alignment Requirements

If the specified shape or layout of the copy is of type `cuda::aligned_size_t<N>`, alignment will be guaranteed to be at least `min(16, N)` [CUDA_C_Programming_Guide:L12632-L12677]. In this case:
*   Both `dst` and `src` pointers need to be aligned to `N` bytes [CUDA_C_Programming_Guide:L12632-L12677].
*   The number of bytes copied needs to be a multiple of `N` [CUDA_C_Programming_Guide:L12632-L12677].

**Errata Note:** The `memcpy_async` API introduced in CUDA 11.1 with both src and dst input layouts expects the layout to be provided in elements rather than bytes [CUDA_C_Programming_Guide:L12632-L12677]. The element type is inferred from `TyElem` and has the size `sizeof(TyElem)` [CUDA_C_Programming_Guide:L12632-L12677]. If `cuda::aligned_size_t<N>` type is used as the layout, the number of elements specified times `sizeof(TyElem)` must be a multiple of `N` [CUDA_C_Programming_Guide:L12632-L12677]. It is recommended to use `std::byte` or `char` as the element type in such cases [CUDA_C_Programming_Guide:L12632-L12677].

## Synchronization and Performance

Having to wait on all outstanding requests can lose some flexibility (but gain simplicity) [CUDA_C_Programming_Guide:L12632-L12677]. To efficiently overlap data transfer and execution, it is important to be able to kick off an N+1 `memcpy_async` request while waiting on and operating on request N [CUDA_C_Programming_Guide:L12632-L12677]. This is achieved by using `memcpy_async` and waiting on it using the collective stage-based `wait_prior` API [CUDA_C_Programming_Guide:L12632-L12677].

## Codegen Requirements

*   **Compute Capability:** 5.0 minimum [CUDA_C_Programming_Guide:L12632-L12677].
*   **Asynchronicity:** Compute Capability 8.0 is required for asynchronicity [CUDA_C_Programming_Guide:L12632-L12677].
*   **Language:** C++11 [CUDA_C_Programming_Guide:L12632-L12677].

## Example

The following example streams data from global memory into a limited-sized shared memory block to operate on, using `wait` to synchronize between stages [CUDA_C_Programming_Guide:L12678-L12706].

```cpp
/// This example streams elementsPerThreadBlock worth of data from global memory
/// into a limited sized shared memory (elementsInShared) block to operate on.
#include <cooperative_groups.h>
#include <cooperative_groups/memcpy_async.h>

namespace cg = cooperative_groups;

__global__ void kernel(int* global_data) {
    cg::thread_block tb = cg::this_thread_block();
    const size_t elementsPerThreadBlock = 16 * 1024;
    const size_t elementsInShared = 128;
    __shared__ int local_smem[elementsInShared];

    size_t copy_count;
    size_t index = 0;
    while (index < elementsPerThreadBlock) {
        cg::memcpy_async(tb, local_smem, elementsInShared, global_data + index,
        elementsPerThreadBlock - index);
        copy_count = min(elementsInShared, elementsPerThreadBlock - index);
        cg::wait(tb);
        // Work with local_smem
        index += copy_count;
    }
}
```

[CUDA_C_Programming_Guide:L12678-L12706]
