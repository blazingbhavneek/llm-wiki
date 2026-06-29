# inclusive_scan and exclusive_scan

The `inclusive_scan` and `exclusive_scan` functions perform scan operations on data provided by each thread named in a specified cooperative group. These functions are part of the Cooperative Groups library and require the inclusion of the `cooperative_groups/scan.h` header [CUDA_C_Programming_Guide:L12955-L13031].

## Function Signatures

### Basic Scan

```cpp
template <typename TyGroup, typename TyVal, typename TyFn>
auto inclusive_scan(const TyGroup& group, TyVal&& val, TyFn&& op) -> decltype(op(val, val));

template <typename TyGroup, typename TyVal>
TyVal inclusive_scan(const TyGroup& group, TyVal&& val);

template <typename TyGroup, typename TyVal, typename TyFn>
auto exclusive_scan(const TyGroup& group, TyVal&& val, TyFn&& op) -> decltype(op(val, val));

template <typename TyGroup, typename TyVal>
TyVal exclusive_scan(const TyGroup& group, TyVal&& val);
```

### Scan Update

The `*_scan_update` variants take an additional `atomic` argument, which can be either `cuda::atomic` or `cuda::atomic_ref` from the CUDA C++ Standard Library. These variants are available only on platforms and devices where these types are supported [CUDA_C_Programming_Guide:L12955-L13031].

```cpp
template <typename TyGroup, typename TyAtomic, typename TyVal, typename TyFn>
auto inclusive_scan_update(const TyGroup& group, TyAtomic& atomic, TyVal&& val, TyFn&& op) -> decltype(op(val, val));

template <typename TyGroup, typename TyAtomic, typename TyVal>
TyVal inclusive_scan_update(const TyGroup& group, TyAtomic& atomic, TyVal&& val);

template <typename TyGroup, typename TyAtomic, typename TyVal, typename TyFn>
auto exclusive_scan_update(const TyGroup& group, TyAtomic& atomic, TyVal&& val, TyFn&& op) -> decltype(op(val, val));

template <typename TyGroup, typename TyAtomic, typename TyVal>
TyVal exclusive_scan_update(const TyGroup& group, TyAtomic& atomic, TyVal&& val);
```

## Parameters

- **group**: The cooperative group containing the threads to participate in the scan. Valid group types are `coalesced_group` and `thread_block_tile` [CUDA_C_Programming_Guide:L12955-L13031].
- **val**: A value of any type that satisfies the following requirements:
  - Must be trivially copyable (`is_trivially_copyable<TyArg>::value == true`) [CUDA_C_Programming_Guide:L12955-L13031].
  - `sizeof(T) <= 32` for `coalesced_group` and tiles of size lower or equal to 32; `sizeof(T) <= 8` for larger tiles [CUDA_C_Programming_Guide:L12955-L13031].
  - Must have suitable arithmetic or comparative operators for the given function object [CUDA_C_Programming_Guide:L12955-L13031].
  - Different threads in the group can pass different values for this argument [CUDA_C_Programming_Guide:L12955-L13031].
- **op**: A function object used for the reduction operation. Convenience function objects include `plus()`, `less()`, `greater()`, `bit_and()`, `bit_xor()`, and `bit_or()`. These must be constructed, requiring the `TyVal` template argument (e.g., `plus<int>()`) [CUDA_C_Programming_Guide:L12955-L13031]. The functions also support lambdas and other function objects invocable via `operator()` [CUDA_C_Programming_Guide:L12955-L13031]. Overloads without the `op` argument use `cg::plus<TyVal>()` by default [CUDA_C_Programming_Guide:L12955-L13031].
- **atomic**: For the update variants, this is the atomic variable to be updated. The type held by the atomic must match `TyVal` [CUDA_C_Programming_Guide:L12955-L13031]. The scope of the atomic must include all threads in the group, and if multiple groups use the same atomic concurrently, the scope must include all threads in all groups [CUDA_C_Programming_Guide:L12955-L13031]. The atomic update is performed with relaxed memory ordering [CUDA_C_Programming_Guide:L12955-L13031].

## Behavior

- **exclusive_scan**: The result for each thread is a reduction of data from threads with a lower `thread_rank` than that thread [CUDA_C_Programming_Guide:L12955-L13031].
- **inclusive_scan**: The result includes the calling thread's data in the reduction [CUDA_C_Programming_Guide:L12955-L13031].
- **scan_update**: These variants perform an update to the atomic variable according to `op` with the value of the sum of input values of all threads in the group. The previous value of the atomic is combined with the result of the scan by each thread and returned [CUDA_C_Programming_Guide:L12955-L13031].

## Codegen Requirements

- Minimum Compute Capability: 5.0 [CUDA_C_Programming_Guide:L12955-L13031].
- C++11 support required [CUDA_C_Programming_Guide:L12955-L13031].

## Examples

### Inclusive Scan

The following example demonstrates an inclusive scan where each thread's result is the sum of its own rank and the ranks of all preceding threads in the tile [CUDA_C_Programming_Guide:L13032-L13106].

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

### Stream Compaction with Exclusive Scan

The following example shows how `exclusive_scan` can be used for stream compaction to calculate starting indices in the output array [CUDA_C_Programming_Guide:L13032-L13106].

```cpp
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
    // into a contiguous part of the array and count them.
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
    }
    // return the total number of items in the output
    return g.shfl(my_idx + my_count, g.num_threads() - 1);
}
```

## Scan Update Pseudocode

The `inclusive_scan_update` function behaves similarly to the following block, except both the reduction and inclusive scan are calculated simultaneously [CUDA_C_Programming_Guide:L12955-L13031]:

```cpp
/*
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

## See Also

- `reduce`
- `cooperative_groups` namespace
- `cuda::atomic`
- `cuda::atomic_ref`
