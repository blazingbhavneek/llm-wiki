## 11.5. Group Partitioning

## 11.5.1. tiled\_partition

```c
template <unsigned int Size, typename ParentT>
thread_block_tile<Size, ParentT> tiled_partition(const ParentT& g);
```

thread\_group tiled\_partition(const thread\_group& parent, unsigned int tilesz);

The tiled\_partition method is a collective operation that partitions the parent group into a onedimensional, row-major, tiling of subgroups. A total of ((size(parent)/tilesz) subgroups will be created, therefore the parent group size must be evenly divisible by the Size. The allowed parent groups are thread\_block or thread\_block\_tile.

The implementation may cause the calling thread to wait until all the members of the parent group have invoked the operation before resuming execution. Functionality is limited to native hardware sizes, 1/2/4/8/16/32 and the cg::size(parent) must be greater than the Size parameter. The templated version of tiled\_partition supports 64/128/256/512 sizes as well, but some additional steps are required on Compute Capability 7.5 or lower, refer to Thread Block Tile for details.

Codegen Requirements: Compute Capability 5.0 minimum, C++11 for sizes larger than 32

## Example:

```c
/// The following code will create a 32-thread tile
thread_block block = this_thread_block();
thread_block_tile<32> tile32 = tiled_partition<32>(block);
```

We can partition each of these groups into even smaller groups, each of size 4 threads:

```txt
auto tile4 = tiled_partition<4>(tile32);
// or using a general group
// thread_group tile4 = tiled_partition(tile32, 4);
```

If, for instance, if we were to then include the following line of code:

```javascript
if (tile4.thread_rank()==0) printf("Hello from tile4 rank 0\n");
```

then the statement would be printed by every fourth thread in the block: the threads of rank 0 in each tile4 group, which correspond to those threads with ranks 0,4,8,12,etc. in the block group.

## 11.5.2. labeled\_partition

```txt
template <typename Label>
coalesced_group labeled_partition(const coalesced_group& g, Label label);
```

```txt
template <unsigned int Size, typename Label>
coalesced_group labeled_partition(const thread_block_tile<Size>& g, Label label);
```

The labeled\_partition method is a collective operation that partitions the parent group into onedimensional subgroups within which the threads are coalesced. The implementation will evaluate a condition label and assign threads that have the same value for label into the same group.

Label can be any integral type.

The implementation may cause the calling thread to wait until all the members of the parent group have invoked the operation before resuming execution.

Note: This functionality is still being evaluated and may slightly change in the future.

Codegen Requirements: Compute Capability 7.0 minimum, C++11

## 11.5.3. binary\_partition

```txt
coalesced_group binary_partition(const coalesced_group& g, bool pred);
```

```txt
template <unsigned int Size>
coalesced_group binary_partition(const thread_block_tile<Size>& g, bool pred);
```

The binary\_partition() method is a collective operation that partitions the parent group into onedimensional subgroups within which the threads are coalesced. The implementation will evaluate a predicate and assign threads that have the same value into the same group. This is a specialized form of labeled\_partition(), where the label can only be 0 or 1.

The implementation may cause the calling thread to wait until all the members of the parent group have invoked the operation before resuming execution.

Note: This functionality is still being evaluated and may slightly change in the future.

Codegen Requirements: Compute Capability 7.0 minimum, C++11

## Example:

```cpp
/// This example divides a 32-sized tile into a group with odd
/// numbers and a group with even numbers
_global__ void oddEven(int *inputArr) {
    auto block = cg::this_thread_block();
    auto tile32 = cg::tiled_partition<32>(block);

    // inputArr contains random integers
    int elem = inputArr[block.thread_rank()];
    // after this, tile32 is split into 2 groups,
    // a subtile where elem&1 is true and one where its false
    auto subtile = cg::binary_partition(tile32, (elem & 1));
}
```

## 11.6. Group Collectives

Cooperative Groups library provides a set of collective operations that can be performed by a group of threads. These operations require participation of all threads in the specified group in order to complete the operation. All threads in the group need to pass the same values for corresponding arguments to each collective call, unless diferent values are explicitly allowed in the argument description. Otherwise the behavior of the call is undefined.

## 11.6.1. Synchronization

11.6.1.1 barrier\_arrive and barrier\_wait

```c
T::arrival_token T::barrier_arrive();
void T::barrier_wait(T::arrival_token&&);
```

barrier\_arrive and barrier\_wait member functions provide a synchronization API similar to cuda::barrier (read more). Cooperative Groups automatically initializes the group barrier, but arrive and wait operations have an additional restriction resulting from collective nature of those operations: All threads in the group must arrive and wait at the barrier once per phase. When barrier\_arrive is called with a group, result of calling any collective operation or another barrier arrival with that group is undefined until completion of the barrier phase is observed with barrier\_wait call. Threads blocked on barrier\_wait might be released from the synchronization before other threads call barrier\_wait, but only after all threads in the group called barrier\_arrive. Group type T can be any of the implicit groups.This allows threads to do independent work after they arrive and before they wait for the synchronization to resolve, allowing to hide some of the synchronization latency. barrier\_arrive returns an arrival\_token object that must be passed into the corresponding barrier\_wait. Token is consumed this way and can not be used for another barrier\_wait call.

Example of barrier\_arrive and barrier\_wait used to synchronize initalization of shared memory across the cluster:

```cpp
#include <cooperative_groups.h>

using namespace cooperative_groups;

void __device__ init_shared_data(const thread_block& block, int *data);
void __device__ local_processing(const thread_block& block);
void __device__ process_shared_data(const thread_block& block, int *data);

__global__ void cluster_kernel() {
    extern __shared__ int array[];
    auto cluster = this_cluster();
    auto block = this_thread_block();

    // Use this thread block to initialize some shared state
    init_shared_data(block, &array[0]);

    auto token = cluster.barrier_arrive(); // Let other blocks know this block is running and data was initialized

    // Do some local processing to hide the synchronization latency
    local_processing(block);

    // Map data in shared memory from the next block in the cluster
    int *dsmem = cluster.map_shared_rank(&array[0], (cluster.block_rank() + 1) % cluster.num_blocks());

    // Make sure all other blocks in the cluster are running and initialized shared data before accessing dsmem
    cluster.barrier_wait(std::move(token));

    // Consume data in distributed shared memory
    process_shared_data(block, dsmem);
```

(continues on next page)

```txt
cluster.sync();
}
```

(continued from previous page)

## 11.6.1.2 sync

```cpp
static void T::sync();
```

```txt
template <typename T>
void sync(T& group);
```

sync synchronizes the threads named in the group. Group type T can be any of the existing group types, as all of them support synchronization. Its available as a member function in every group type or as a free function taking a group as parameter. If the group is a grid\_group the kernel must have been launched using the appropriate cooperative launch APIs. Equivalent to T.barrier\_wait(T. barrier\_arrive()).

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

## 11.6.2.2 wait and wait\_prior

```c
template <typename TyGroup>
void wait(TyGroup & group);

template <unsigned int NumStages, typename TyGroup>
void wait_prior(TyGroup & group);
```

wait and wait\_prior collectives allow to wait for memcpy\_async copies to complete. wait blocks calling threads until all previous copies are done. wait\_prior allows that the latest NumStages are still not done and waits for all the previous requests. So with N total copies requested, it waits until the first N-NumStages are done and the last NumStages might still be in progress. Both wait and wait\_prior will synchronize the named group.

Codegen Requirements: Compute Capability 5.0 minimum, Compute Capability 8.0 for asynchronicity, C++11

cooperative\_groups∕memcpy\_async.h header needs to be included.

## Example:

```cpp
/// This example streams elementsPerThreadBlock worth of data from global memory
/// into a limited sized shared memory (elementsInShared) block to operate on in
/// multiple (two) stages. As stage N is kicked off, we can wait on and operate on
stage N-1.
#include <cooperative_groups.h>
#include <cooperative_groups/memcpy_async.h>

namespace cg = cooperative_groups;

__global__ void kernel(int* global_data) {
    cg::thread_block tb = cg::this_thread_block();
    const size_t elementsPerThreadBlock = 16 * 1024 + 64;
    const size_t elementsInShared = 128;
    __align__(16) __shared__ int local_smem[2][elementsInShared];
    int stage = 0;
    // First kick off an extra request
    size_t copy_count = elementsInShared;
    size_t index = copy_count;
    cg::memcpy_async(tb, local_smem[stage], elementsInShared, global_data,
elementsPerThreadBlock - index);
    while (index < elementsPerThreadBlock) {
        // Now we kick off the next request...
        cg::memcpy_async(tb, local_smem[stage ^ 1], elementsInShared, global_data +
index, elementsPerThreadBlock - index);
        // ... but we wait on the one before it
        cg::wait_prior<1>(tb);

        // Its now available and we can work with local_smem[stage] here
        // (...)
        //

        // Calculate the amount fo data that was actually copied, for the next
iteration.
        copy_count = min(elementsInShared, elementsPerThreadBlock - index);
        index += copy_count;

        // A cg::sync(tb) might be needed here depending on whether
```

```rust
// the work done with local_smem[stage] can release threads to race ahead or not
        // Wrap to the next stage
        stage ^= 1;
    }
    cg::wait(tb);
    // The last local_smem[stage] can be handled here
}
```

## 11.6.3. Data Manipulation

## 11.6.3.1 reduce

```cpp
template <typename TyGroup, typename TyArg, typename TyOp>
auto reduce(const TyGroup& group, TyArg&& val, TyOp&& op) -> decltype(op(val, val));
```

reduce performs a reduction operation on the data provided by each thread named in the group passed in. This takes advantage of hardware acceleration (on compute 80 and higher devices) for the arithmetic add, min, or max operations and the logical AND, OR, or XOR, as well as providing a software fallback on older generation hardware. Only 4B types are accelerated by hardware.

group: Valid group types are coalesced\_group and thread\_block\_tile.

val: Any type that satisfies the below requirements:

▶ Qualifies as trivially copyable i.e. is\_trivially\_copyable<TyArg>::value == true

sizeof(T) <= 32 for coalesced\_group and tiles of size lower or equal 32, sizeof(T) <= 8 for larger tiles

▶ Has suitable arithmetic or comparative operators for the given function object.

Note: Diferent threads in the group can pass diferent values for this argument.

op: Valid function objects that will provide hardware acceleration with integral types are plus(), less(), greater(), bit\_and(), bit\_xor(), bit\_or(). These must be constructed, hence the TyVal template argument is required, i.e. plus<int>(). Reduce also supports lambdas and other function objects that can be invoked using operator()

Asynchronous reduce

template <typename TyGroup, typename TyArg, typename TyAtomic, typename TyOp> void reduce\_update\_async(const TyGroup& group, TyAtomic& atomic, TyArg&& val, TyOp&& ,<sub>→</sub>op);

template <typename TyGroup, typename TyArg, typename TyAtomic, typename TyOp> void reduce\_store\_async(const TyGroup& group, TyAtomic& atomic, TyArg&& val, TyOp&& ,<sub>→</sub>op);

```txt
template <typename TyGroup, typename TyArg, typename TyOp>
void reduce_store_async(const TyGroup& group, TyArg* ptr, TyArg&& val, TyOp&& op);
```

\*\_async variants of the API are asynchronously calculating the result to either store to or update a specified destination by one of the participating threads, instead of returning it by each thread. To observe the efect of these asynchronous calls, calling group of threads or a larger group containing them need to be synchronized.

In case of the atomic store or update variant, atomic argument can be either of cuda::atomic or cuda::atomic\_ref available in CUDA C++ Standard Library. This variant of the API is available only on platforms and devices, where these types are supported by the CUDA C++ Standard Library. Result of the reduction is used to atomically update the atomic according to the specified op, eg. the result is atomically added to the atomic in case of cg::plus(). Type held by the atomic must match the type of TyArg. Scope of the atomic must include all the threads in the group and if multiple groups are using the same atomic concurrently, scope must include all threads in all groups using it. Atomic update is performed with relaxed memory ordering.

In case of the pointer store variant, result of the reduction will be weakly stored into the dst pointer.

Codegen Requirements: Compute Capability 5.0 minimum, Compute Capability 8.0 for HW acceleration, C++11.

cooperative\_groups∕reduce.h header needs to be included.

Example of approximate standard deviation for integer vector:

```cpp
#include <cooperative_groups.h>
#include <cooperative_groups/reduce.h>
namespace cg = cooperative_groups;

/// Calculate approximate standard deviation of integers in vec
__device__ int std_dev(const cg::thread_block_tile<32>& tile, int *vec, int length) {
    int thread_sum = 0;

    // calculate average first
    for (int i = tile.thread_rank(); i < length; i += tile.num_threads()) {
        thread_sum += vec[i];
    }
    // cg::plus<int> allows cg::reduce() to know it can use hardware acceleration for
addition
    int avg = cg::reduce(tile, thread_sum, cg::plus<int>() ) / length;

    int thread_diffs_sum = 0;
    for (int i = tile.thread_rank(); i < length; i += tile.num_threads()) {
        int diff = vec[i] - avg;
        thread_diffs_sum += diff * diff;
    }

    // temporarily use floats to calculate the square root
    float diff_sum = static_cast<float>(cg::reduce(tile, thread_diffs_sum, cg::plus
<int>() )) / length;

    return static_cast<int>(sqrtf(diff_sum));
}
```

Example of block wide reduction:

```cpp
#include <cooperative_groups.h>
#include <cooperative_groups/reduce.h>
namespace cg=cooperative_groups;

/// The following example accepts input in *A and outputs a result into *sum
/// It spreads the data equally within the block
__device__ void block_reduce(const int* A, int count, cuda::atomic<int, cuda::thread_
->scope_block>& total_sum) {
    auto block = cg::this_thread_block();
(continues on next page)
```

(continues on next page)

```cpp
auto tile = cg::tiled_partition<32>(block);
int thread_sum = 0;

// Stride loop over all values, each thread accumulates its part of the array.
for (int i = block.thread_rank(); i < count; i += block.size()) {
    thread_sum += A[i];
}

// reduce thread sums across the tile, add the result to the atomic
// cg::plus<int> allows cg::reduce() to know it can use hardware acceleration for
addition
cg::reduce_update_async(tile, total_sum, thread_sum, cg::plus<int>());
// synchronize the block, to ensure all async reductions are ready
block.sync();
}
```

## 11.6.3.2 Reduce Operators

Below are the prototypes of function objects for some of the basic operations that can be done with reduce

```cpp
namespace cooperative_groups {
  template <typename Ty>
  struct cg::plus;

  template <typename Ty>
  struct cg::less;

  template <typename Ty>
  struct cg::greater;

  template <typename Ty>
  struct cg::bit_and;

  template <typename Ty>
  struct cg::bit_xor;

  template <typename Ty>
  struct cg::bit_or;
}
```

Reduce is limited to the information available to the implementation at compile time. Thus in order to make use of intrinsics introduced in CC 8.0, the cg:: namespace exposes several functional objects that mirror the hardware. These objects appear similar to those presented in the C++ STL, with the exception of less∕greater. The reason for any diference from the STL is that these function objects are designed to actually mirror the operation of the hardware intrinsics.

## Functional description:

▶ cg::plus: Accepts two values and returns the sum of both using operator+.

▶ cg::less: Accepts two values and returns the lesser using operator<. This difers in that the lower value is returned rather than a Boolean.

▶ cg::greater: Accepts two values and returns the greater using operator<. This difers in that the greater value is returned rather than a Boolean.

▶ cg::bit\_and: Accepts two values and returns the result of operator&.

▶ cg::bit\_xor: Accepts two values and returns the result of operator^.

▶ cg::bit\_or: Accepts two values and returns the result of operator|.

## Example:

```cpp
{
    // cg::plus<int> is specialized within cg::reduce and calls __reduce_add_sync(...)
    on CC 8.0+
    cg::reduce(tile, (int)val, cg::plus<int>());
    // cg::plus<float> fails to match with an accelerator and instead performs a
    standard shuffle based reduction
    cg::reduce(tile, (float)val, cg::plus<float>());
    // While individual components of a vector are supported, reduce will not use
    hardware intrinsics for the following
    // It will also be necessary to define a corresponding operator for vector and any
    custom types that may be used
    int4 vec = {...};
    cg::reduce(tile, vec, cg::plus<int4inine)

    // Finally lambdas and other function objects cannot be inspected for dispatch
    // and will instead perform shuffle based reductions using the provided function
    object.
    cg::reduce(tile, (int)val, [](int 1, int r) -> int {return 1 + r;});
}
```

## 11.6.3.3 inclusive\_scan and exclusive\_scan

```c
template <typename TyGroup, typename TyVal, typename TyFn>
auto inclusive_scan(const TyGroup& group, TyVal&& val, TyFn&& op) -> decltype(op(val,
    val));

template <typename TyGroup, typename TyVal>
TyVal inclusive_scan(const TyGroup& group, TyVal&& val);

template <typename TyGroup, typename TyVal, typename TyFn>
auto exclusive_scan(const TyGroup& group, TyVal&& val, TyFn&& op) -> decltype(op(val,
    val));

template <typename TyGroup, typename TyVal>
TyVal exclusive_scan(const TyGroup& group, TyVal&& val);
```

inclusive\_scan and exclusive\_scan performs a scan operation on the data provided by each thread named in the group passed in. Result for each thread is a reduction of data from threads with lower thread\_rank than that thread in case of exclusive\_scan. inclusive\_scan result also includes the calling thread data in the reduction.

group: Valid group types are coalesced\_group and thread\_block\_tile.

val: Any type that satisfies the below requirements:

```txt
Qualifies as trivially copyable i.e. is_trivially_copyable<TyArg>::value == true
```

▶ sizeof(T) <= 32 for coalesced\_group and tiles of size lower or equal 32, sizeof(T) <= 8 for larger tiles

▶ Has suitable arithmetic or comparative operators for the given function object.

Note: Diferent threads in the group can pass diferent values for this argument.

op: Function objects defined for convenience are plus(), less(), greater(), bit\_and(), bit\_xor(), bit\_or() described in Reduce Operators. These must be constructed, hence the TyVal template argument is required, i.e. plus<int>(). inclusive\_scan and exclusive\_scan also supports lambdas and other function objects that can be invoked using operator(). Overloads without this argument use cg::plus<TyVal>().

## Scan update

template <typename TyGroup, typename TyAtomic, typename TyVal, typename TyFn> auto inclusive\_scan\_update(const TyGroup& group, TyAtomic& atomic, TyVal&& val, TyFn&& , op) -> decltype(op(val, val));

```txt
template <typename TyGroup, typename TyAtomic, typename TyVal>
TyVal inclusive_scan_update(const TyGroup& group, TyAtomic& atomic, TyVal&& val);
```

template <typename TyGroup, typename TyAtomic, typename TyVal, typename TyFn> auto exclusive\_scan\_update(const TyGroup& group, TyAtomic& atomic, TyVal&& val, TyFn&& ,<sub>→</sub> op) -> decltype(op(val, val));

```txt
template <typename TyGroup, typename TyAtomic, typename TyVal>
TyVal exclusive_scan_update(const TyGroup& group, TyAtomic& atomic, TyVal&& val);
```

\*\_scan\_update collectives take an additional argument atomic that can be either of cuda::atomic or cuda::atomic\_ref available in CUDA C++ Standard Library. These variants of the API are available only on platforms and devices, where these types are supported by the CUDA C++ Standard Library. These variants will perform an update to the atomic according to op with value of the sum of input values of all threads in the group. Previous value of the atomic will be combined with the result of scan by each thread and returned. Type held by the atomic must match the type of TyVal. Scope of the atomic must include all the threads in the group and if multiple groups are using the same atomic concurrently, scope must include all threads in all groups using it. Atomic update is performed with relaxed memory ordering.

Following pseudocode illustrates how the update variant of scan works:

```txt
/*
  inclusive_scan_update behaves as the following block,
  except both reduce and inclusive_scan is calculated simultaneously.
auto total = reduce(group, val, op);
TyVal old;
if (group.thread_rank() == selected_thread) {
    atomically {
      old = atomic.load();
      atomic.store(op(old, total));
    }
}
old = group.shfl(old, selected_thread);
return op(inclusive_scan(group, val, op), old);
*/
```

Codegen Requirements: Compute Capability 5.0 minimum, C++11.

cooperative\_groups∕scan.h header needs to be included.

## Example:

```cpp
#include <stdio.h>
#include <cooperative_groups.h>
#include <cooperative_groups/scan.h>
namespace cg = cooperative_groups;

__global__ void kernel() {
    auto thread_block = cg::this_thread_block();
    auto tile = cg::tiled_partition<8>(thread_block);
    unsigned int val = cg::inclusive_scan(tile, tile.thread_rank());
    printf("%u: %u\n", tile.thread_rank(), val);
}

/* prints for each group:
    0: 0
    1: 1
    2: 3
    3: 6
    4: 10
    5: 15
    6: 21
    7: 28
*/
```

Example of stream compaction using exclusive\_scan:

```txt
#include <cooperative_groups.h>
#include <cooperative_groups/scan.h>
namespace cg = cooperative_groups;

// put data from input into output only if it passes test_fn predicate
template<typename Group, typename Data, typename TyFn>
__device__ int stream_compaction(Group &g, Data *input, int count, TyFn&& test_fn,
Data *output) {
    int per_thread = count / g.num_threads();
    int thread_start = min(g.thread_rank() * per_thread, count);
    int my_count = min(per_thread, count - thread_start);

    // get all passing items from my part of the input
    //  into a contagious part of the array and count them.
    int i = thread_start;
    while (i < my_count + thread_start) {
        if (test_fn(input[i])) {
            i++;
        }
        else {
            my_count--;
            input[i] = input[my_count + thread_start];
        }
    }

    // scan over counts from each thread to calculate my starting
    // index in the output
    int my_idx = cg::exclusive_scan(g, my_count);

    for (i = 0; i < my_count; ++i) {
        output[my_idx + i] = input[thread_start + i];
```

(continues on next page)

```txt
}
// return the total number of items in the output
return g.shfl(my_idx + my_count, g.num_threads() - 1);
}
```

(continued from previous page)

Example of dynamic bufer space allocation using exclusive\_scan\_update:

```cpp
#include <cooperative_groups.h>
#include <cooperative_groups/scan.h>
namespace cg = cooperative_groups;

// Buffer partitioning is static to make the example easier to follow,
// but any arbitrary dynamic allocation scheme can be implemented by replacing this
function.
__device__ int calculate_buffer_space_needed(cg::thread_block_tile<32>& tile) {
    return tile.thread_rank() % 2 + 1;
}

__device__ int my_thread_data(int i) {
    return i;
}

__global__ void kernel() {
    __shared__ extern int buffer[];
    __shared__ cuda::atomic<int, cuda::thread_scope_block> buffer_used;

    auto block = cg::this_thread_block();
    auto tile = cg::tiled_partition<32>(block);
    buffer_used = 0;
    block.sync();

    // each thread calculates buffer size it needs
    int buf_needed = calculate_buffer_space_needed(tile);

    // scan over the needs of each thread, result for each thread is an offset
    // of that thread's part of the buffer. buffer_used is atomically updated with
    // the sum of all thread's inputs, to correctly offset other tile's allocations
    int buf_offset =
        cg::exclusive_scan_update(tile, buffer_used, buf_needed);

    // each thread fills its own part of the buffer with thread specific data
    for (int i = 0 ; i < buf_needed ; ++i) {
        buffer[buf_offset + i] = my_thread_data(i);
    }

    block.sync();
    // buffer_used now holds total amount of memory allocated
    // buffer is {0, 0, 1, 0, 0, 1 ...};
}
```

```txt
template<typename Group, typename Fn, typename... Args>
void invoke_one(const Group& group, Fn&& fn, Args&&... args);

template<typename Group, typename Fn, typename... Args>
auto invoke_one_broadcast(const Group& group, Fn&& fn, Args&&... args) ->
    decltype(fn(args...));
```

## 11.6.4. Execution control

## 11.6.4.1 invoke\_one and invoke\_one\_broadcast

invoke\_one selects a single arbitrary thread from the calling group and uses that thread to call the supplied invocable fn with the supplied arguments args. In case of invoke\_one\_broadcast the result of the call is also distributed to all threads in the group and returned from this collective.

Calling group can be synchronized with the selected thread before and/or after it calls the supplied invocable. It means that communication within the calling group is not allowed inside the supplied invocable body, otherwise forward progress is not guaranteed. Communication with threads outside of the calling group is allowed in the body of the supplied invocable. Thread selection mechanism is not guaranteed to be deterministic.

On devices with Compute Capability 9.0 or higher hardware acceleration might be used to select the thread when called with explicit group types.

group: All group types are valid for invoke\_one, coalesced\_group and thread\_block\_tile are valid for invoke\_one\_broadcast.

fn: Function or object that can be invoked using operator().

args: Parameter pack of types matching types of parameters of the supplied invocable fn.

In case of invoke\_one\_broadcast the return type of the supplied invocable fn must satisfy the below requirements:

Qualifies as trivially copyable i.e. is\_trivially\_copyable<T>::value == true

sizeof(T) <= 32 for coalesced\_group and tiles of size lower or equal 32, sizeof(T) <= 8 for larger tiles

Codegen Requirements: Compute Capability 5.0 minimum, Compute Capability 9.0 for hardware acceleration, C++11.

Aggregated atomic example from Discovery pattern section re-written to use invoke\_one\_broadcast:

```cpp
#include <cooperative_groups.h>
#include <cuda/atomic>
namespace cg = cooperative_groups;

template<cuda::thread_scope Scope>
__device__ unsigned int atomicAddOneRelaxed(cuda::atomic<unsigned int, Scope>&
    atomic) {
    auto g = cg::coalesced_threads();
    auto prev = cg::invoke_one_broadcast(g, [&] () {
        return atomic.fetch_add(g.num_threads(), cuda::memory_order_relaxed);
    });
    return prev + g.thread_rank();
}
```
