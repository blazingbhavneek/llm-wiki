# inclusive_scan and exclusive_scan

Collective operations that perform prefix sum (scan) on data provided by each thread. inclusive_scan includes the calling thread's value, while exclusive_scan does not. Supports atomic update variants.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L12956-L13104

Citation: [CUDA_C_Programming_Guide:L12956-L13104]

````text
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
````
