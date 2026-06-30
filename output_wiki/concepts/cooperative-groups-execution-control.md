# Cooperative Groups Execution Control (invoke_one / invoke_one_broadcast)

Covers the cooperative groups execution control functions invoke_one and invoke_one_broadcast, including function signatures, parameter requirements, codegen constraints, and usage examples for dynamic buffer allocation and aggregated atomics.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L13107-L13203

Citation: [CUDA_C_Programming_Guide:L13107-L13203]

````text
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
````
