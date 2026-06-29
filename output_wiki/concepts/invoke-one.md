# invoke_one

`invoke_one` and `invoke_one_broadcast` are collective functions provided by the `cooperative_groups` namespace that allow a group of threads to designate a single thread to execute a specific function. This pattern is useful for reducing redundant computation or coordinating access to shared resources where only one thread needs to perform the operation, while others may need the result.

## Function Signatures

The signatures for both functions are defined as follows [CUDA_C_Programming_Guide:L13154-L13161]:

```cpp
template<typename Group, typename Fn, typename... Args>
void invoke_one(const Group& group, Fn&& fn, Args&&... args);

template<typename Group, typename Fn, typename... Args>
auto invoke_one_broadcast(const Group& group, Fn&& fn, Args&&... args) ->
    decltype(fn(args...));
```

## Behavior

### `invoke_one`
`invoke_one` selects a single arbitrary thread from the calling group and uses that thread to call the supplied invocable `fn` with the supplied arguments `args` [CUDA_C_Programming_Guide:L13166-L13185]. The function does not return a value to the other threads.

### `invoke_one_broadcast`
`invoke_one_broadcast` operates similarly to `invoke_one` but additionally distributes the result of the call to all threads in the group and returns that value from the collective call [CUDA_C_Programming_Guide:L13166-L13185].

## Constraints and Requirements

### Thread Selection
The thread selection mechanism is not guaranteed to be deterministic [CUDA_C_Programming_Guide:L13166-L13185]. On devices with Compute Capability 9.0 or higher, hardware acceleration might be used to select the thread when called with explicit group types [CUDA_C_Programming_Guide:L13166-L13185].

### Synchronization and Communication
The calling group can be synchronized with the selected thread before and/or after it calls the supplied invocable [CUDA_C_Programming_Guide:L13166-L13185]. This implies that communication within the calling group is not allowed inside the supplied invocable body; doing so would mean forward progress is not guaranteed [CUDA_C_Programming_Guide:L13166-L13185]. However, communication with threads outside of the calling group is allowed in the body of the supplied invocable [CUDA_C_Programming_Guide:L13166-L13185].

### Valid Group Types
- `invoke_one`: All group types are valid [CUDA_C_Programming_Guide:L13166-L13185].
- `invoke_one_broadcast`: Only `coalesced_group` and `thread_block_tile` are valid [CUDA_C_Programming_Guide:L13166-L13185].

### Return Type Requirements (for `invoke_one_broadcast`)
For `invoke_one_broadcast`, the return type of the supplied invocable `fn` must satisfy specific requirements [CUDA_C_Programming_Guide:L13166-L13185]:
1. It must qualify as trivially copyable (`std::is_trivially_copyable<T>::value == true`).
2. Size constraints depend on the group size:
   - `sizeof(T) <= 32` for `coalesced_group` and tiles of size lower or equal to 32.
   - `sizeof(T) <= 8` for larger tiles.

### Codegen Requirements
- Minimum Compute Capability: 5.0 [CUDA_C_Programming_Guide:L13166-L13185].
- Hardware acceleration requires Compute Capability 9.0 [CUDA_C_Programming_Guide:L13166-L13185].
- Requires C++11 [CUDA_C_Programming_Guide:L13166-L13185].

## Example Usage

The following example demonstrates using `invoke_one_broadcast` to implement an aggregated atomic add operation. One thread performs the atomic fetch-add, and the result is broadcast to all threads, which then compute their individual contributions [CUDA_C_Programming_Guide:L13186-L13203]:

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

In this example, `invoke_one_broadcast` ensures that all threads in the `coalesced_group` `g` receive the base value `prev` from the atomic operation, allowing each thread to add its own `thread_rank` to the result [CUDA_C_Programming_Guide:L13186-L13203].
