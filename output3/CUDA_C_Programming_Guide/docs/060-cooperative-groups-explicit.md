## 11.4.2. Explicit Groups

## 11.4.2.1 Thread Block Tile

A templated version of a tiled group, where a template parameter is used to specify the size of the tile - with this known at compile time there is the potential for more optimal execution.

```dart
template <unsigned int Size, typename ParentT = void>
class thread_block_tile;
```

Constructed via:

```c
template <unsigned int Size, typename ParentT>
_CG_QUALIFIER thread_block_tile<Size, ParentT> tiled_partition(const ParentT& g)
```

Size must be a power of 2 and less than or equal to 1024. Notes section describes extra steps needed to create tiles of size larger than 32 on hardware with Compute Capability 7.5 or lower.

ParentT is the parent-type from which this group was partitioned. It is automatically inferred, but a value of void will store this information in the group handle rather than in the type.

## Public Member Functions:

void sync() const: Synchronize the threads named in the group

unsigned long long num\_threads() const: Total number of threads in the group

unsigned long long thread\_rank() const: Rank of the calling thread within [0, num\_threads)

unsigned long long meta\_group\_size() const: Returns the number of groups created when the parent group was partitioned.

unsigned long long meta\_group\_rank() const: Linear rank of the group within the set of tiles partitioned from a parent group (bounded by meta\_group\_size)

T shfl(T var, unsigned int src\_rank) const: Refer to Warp Shufle Functions, Note: For sizes larger than 32 all threads in the group have to specify the same src\_rank, otherwise the behavior is undefined.

T shfl\_up(T var, int delta) const: Refer to Warp Shufle Functions, available only for sizes lower or equal to 32.

T shfl\_down(T var, int delta) const: Refer to Warp Shufle Functions, available only for sizes lower or equal to 32

T shfl\_xor(T var, int delta) const: Refer to Warp Shufle Functions, available only for sizes lower or equal to 32.

int any(int predicate) const: Refer to Warp Vote Functions

int all(int predicate) const: Refer to Warp Vote Functions

unsigned int ballot(int predicate) const: Refer to Warp Vote Functions, available only for sizes lower or equal to 32.

unsigned int match\_any(T val) const: Refer to Warp Match Functions, available only for sizes lower or equal to 32.

unsigned int match\_all(T val, int &pred) const: Refer to Warp Match Functions, available only for sizes lower or equal to 32.

Legacy member functions (aliases):

unsigned long long size() const: Total number of threads in the group (alias of num\_threads())

## Notes:

▶ thread\_block\_tile templated data structure is being used here, the size of the group is passed to the tiled\_partition call as a template parameter rather than an argument.

shfl, shfl\_up, shfl\_down, and shfl\_xor functions accept objects of any type when compiled with C++11 or later. This means it’s possible to shufle non-integral types as long as they satisfy the below constraints:

Qualifies as trivially copyable i.e., is\_trivially\_copyable<T>::value == true

▶ sizeof(T) <= 32 for tile sizes lower or equal 32, sizeof(T) <= 8 for larger tiles

On hardware with Compute Capability 7.5 or lower tiles of size larger than 32 need small amount of memory reserved for them. This can be done using cooperative\_groups::block\_tile\_memory struct template that has to reside in either shared or global memory.

```txt
template <unsigned int MaxBlockSize = 1024>
struct block_tile_memory;
```

MaxBlockSize Specifies the maximal number of threads in the current thread block. This parameter can be used to minimize the shared memory usage of block\_tile\_memory in kernels launched only with smaller thread counts.

This block\_tile\_memory needs be then passed into cooperative\_groups::this\_thread\_block, allowing the resulting thread\_block to be partitioned into tiles of sizes larger than 32. Overload of this\_thread\_block accepting block\_tile\_memory argument is a collective operation and has to be called with all threads in the thread\_block.

block\_tile\_memory can be used on hardware with Compute Capability 8.0 or higher in order to be able to write one source targeting multiple diferent Compute Capabilities. It should consume no memory when instantiated in shared memory in cases where its not required.

## Examples:

```rust
/// The following code will create two sets of tiled groups, of size 32 and 4
→respectively:
/// The latter has the provenance encoded in the type, while the first stores it in the
→handle
thread_block block = this_thread_block();
thread_block_tile<32> tile32 = tiled_partition<32>(block);
thread_block_tile<4, thread_block> tile4 = tiled_partition<4>(block);
```

```txt
/// The following code will create tiles of size 128 on all Compute Capabilities.
/// block_tile_memory can be omitted on Compute Capability 8.0 or higher.
__global__ void kernel(...) {
    // reserve shared memory for thread_block_tile usage,
```

(continues on next page)

```dart
//   specify that block size will be at most 256 threads.
__shared__ block_tile_memory<256> shared;
thread_block thb = this_thread_block(shared);

// Create tiles with 128 threads.
auto tile = tiled_partition<128>(thb);

// ...
}
```

(continued from previous page)

## 11.4.2.1.1 Warp-Synchronous Code Pattern

Developers might have had warp-synchronous codes that they previously made implicit assumptions about the warp size and would code around that number. Now this needs to be specified explicitly.

```lisp
__global__ void cooperative_kernel(...) {
    // obtain default "current thread block" group
    thread_block my_block = this_thread_block();

    // subdivide into 32-thread, tiled subgroups
    // Tiled subgroups evenly partition a parent group into
    // adjacent sets of threads - in this case each one warp in size
    auto my_tile = tiled_partition<32>(my_block);

    // This operation will be performed by only the
    // first 32-thread tile of each block
    if (my_tile.meta_group_rank() == 0) {
        // ...
        my_tile.sync();
    }
}
```

## 11.4.2.1.2 Single Thread Group

Group representing the current thread can be obtained from this\_thread function:

```txt
thread_block_tile<1> this_thread();
```

The following memcpy\_async API uses a thread\_group, to copy an int element from source to destination:

```c
#include <cooperative_groups.h>
#include <cooperative_groups/memcpy_async.h>

cooperative_groups::memcpy_async(cooperative_groups::this_thread(), dest, src,
sizeof(int));
```

More detailed examples of using this\_thread to perform asynchronous copies can be found in the Single-Stage Asynchronous Data Copies using cuda::pipeline and Multi-Stage Asynchronous Data Copies using cuda::pipeline sections.

## 11.4.2.2 Coalesced Groups

In CUDA’s SIMT architecture, at the hardware level the multiprocessor executes threads in groups of 32 called warps. If there exists a data-dependent conditional branch in the application code such that threads within a warp diverge, then the warp serially executes each branch disabling threads not on that path. The threads that remain active on the path are referred to as coalesced. Cooperative Groups has functionality to discover, and create, a group containing all coalesced threads.

Constructing the group handle via coalesced\_threads() is opportunistic. It returns the set of active threads at that point in time, and makes no guarantee about which threads are returned (as long as they are active) or that they will stay coalesced throughout execution (they will be brought back together for the execution of a collective but can diverge again afterwards).

class coalesced\_group;

Constructed via:

coalesced\_group active = coalesced\_threads();

## Public Member Functions:

void sync() const: Synchronize the threads named in the group

unsigned long long num\_threads() const: Total number of threads in the group

unsigned long long thread\_rank() const: Rank of the calling thread within [0, num\_threads)

unsigned long long meta\_group\_size() const: Returns the number of groups created when the parent group was partitioned. If this group was created by querying the set of active threads, for example coalesced\_threads() the value of meta\_group\_size() will be 1.

unsigned long long meta\_group\_rank() const: Linear rank of the group within the set of tiles partitioned from a parent group (bounded by meta\_group\_size). If this group was created by querying the set of active threads, e.g. coalesced\_threads() the value of meta\_group\_rank() will always be 0.

T shfl(T var, unsigned int src\_rank) const: Refer to Warp Shufle Functions

T shfl\_up(T var, int delta) const: Refer to Warp Shufle Functions

T shfl\_down(T var, int delta) const: Refer to Warp Shufle Functions

int any(int predicate) const: Refer to Warp Vote Functions

int all(int predicate) const: Refer to Warp Vote Functions

unsigned int ballot(int predicate) const: Refer to Warp Vote Functions

unsigned int match\_any(T val) const: Refer to Warp Match Functions

unsigned int match\_all(T val, int &pred) const: Refer to Warp Match Functions

Legacy member functions (aliases):

unsigned long long size() const: Total number of threads in the group (alias of num\_threads())

## Notes:

shfl, shfl\_up, and shfl\_down functions accept objects of any type when compiled with C++11 or later. This means it’s possible to shufle non-integral types as long as they satisfy the below constraints:

▶ Qualifies as trivially copyable i.e. is\_trivially\_copyable<T>::value == true

```txt
▶ sizeof(T) <= 32
```

```rust
/// Consider a situation whereby there is a branch in the
/// code in which only the 2nd, 4th and 8th threads in each warp are
/// active. The coalesced_threads() call, placed in that branch, will create (for each
/// warp) a group, active, that has three threads (with
/// ranks 0-2 inclusive).
__global__ void kernel(int *globalInput) {
    // Lets say globalInput says that threads 2, 4, 8 should handle the data
    if (threadIdx.x == *globalInput) {
        coalesced_group active = coalesced_threads();
        // active contains 0-2 inclusive
        active.sync();
    }
}
```

## 11.4.2.2.1 Discovery Pattern

Commonly developers need to work with the current active set of threads. No assumption is made about the threads that are present, and instead developers work with the threads that happen to be there. This is seen in the following “aggregating atomic increment across threads in a warp” example (written using the correct CUDA 9.0 set of intrinsics):

```c
{
    unsigned int writemask = __activemask();
    unsigned int total = __popc(writemask);
    unsigned int prefix = __popc(writemask & __lanemask_lt());
    // Find the lowest-numbered active lane
    int elected_lane = __ffs(writemask) - 1;
    int base_offset = 0;
    if (prefix == 0) {
        base_offset = atomicAdd(p, total);
    }
    base_offset = __shfl_sync(writemask, base_offset, elected_lane);
    int thread_offset = prefix + base_offset;
    return thread_offset;
}
```

This can be re-written with Cooperative Groups as follows:

```cpp
{
    cg::coalesced_group g = cg::coalesced_threads();
    int prev;
    if (g.thread_rank() == 0) {
        prev = atomicAdd(p, g.num_threads());
    }
    prev = g.thread_rank() + g.shfl(prev, 0);
    return prev;
}
```
