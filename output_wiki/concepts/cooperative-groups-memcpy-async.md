# memcpy_async

A group-wide collective memcpy that utilizes hardware acceleration for nonblocking memory transactions from global to shared memory. Requires 16-byte alignment and should be paired with wait/wait_prior for completion.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L12632-L12706

Citation: [CUDA_C_Programming_Guide:L12632-L12706]

````text

## 11.6.2. Data Transfer

## 11.6.2.1 memcpy\_async

memcpy\_async is a group-wide collective memcpy that utilizes hardware accelerated support for nonblocking memory transactions from global to shared memory. Given a set of threads named in the group, memcpy\_async will move specified amount of bytes or elements of the input type through a single pipeline stage. Additionally for achieving best performance when using the memcpy\_async API, an alignment of 16 bytes for both shared memory and global memory is required. It is important to note that while this is a memcpy in the general case, it is only asynchronous if the source is global memory and the destination is shared memory and both can be addressed with 16, 8, or 4 byte alignments. Asynchronously copied data should only be read following a call to wait or wait\_prior which signals that the corresponding stage has completed moving data to shared memory.

Having to wait on all outstanding requests can lose some flexibility (but gain simplicity). In order to efficiently overlap data transfer and execution, its important to be able to kick of an N+1memcpy\_async request while waiting on and operating on request N. To do so, use memcpy\_async and wait on it using the collective stage-based wait\_prior API. See wait and wait\_prior for more details.

Usage 1

```txt
template <typename TyGroup, typename TyElem, typename TyShape>
void memcpy_async(
    const TyGroup &group,
    TyElem *__restrict__ _dst,
    const TyElem *__restrict__ _src,
    const TyShape &shape
);
```

Performs a copy of \`\`shape\`\` bytes.

Usage 2

```c
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

Performs a copy of \`\`min(dstLayout, srcLayout)\`\` elements. If layouts are of type cuda::aligned\_size\_t<N>, both must specify the same alignment.

Errata The memcpy\_async API introduced in CUDA 11.1 with both src and dst input layouts, expects the layout to be provided in elements rather than bytes. The element type is inferred from TyElem and has the size sizeof(TyElem). If cuda::aligned\_size\_t<N> type is used as the layout, the number of elements specified times sizeof(TyElem) must be a multiple of N and it is recommended to use std::byte or char as the element type.

If specified shape or layout of the copy is of type cuda::aligned\_size\_t<N>, alignment will be guaranteed to be at least min(16, N). In that case both dst and src pointers need to be aligned to N bytes and the number of bytes copied needs to be a multiple of N.

Codegen Requirements: Compute Capability 5.0 minimum, Compute Capability 8.0 for asynchronicity, C++11

cooperative\_groups∕memcpy\_async.h header needs to be included.

## Example:

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
````
