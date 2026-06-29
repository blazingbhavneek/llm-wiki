# wait and wait_prior

The `wait` and `wait_prior` collectives allow threads to wait for `memcpy_async` copies to complete. Both functions synchronize the named group.

## Function Signatures

```cpp
template <typename TyGroup>
void wait(TyGroup & group);

template <unsigned int NumStages, typename TyGroup>
void wait_prior(TyGroup & group);
```

## Behavior

*   **`wait`**: Blocks calling threads until all previous copies are done [CUDA_C_Programming_Guide:L12707-L12722].
*   **`wait_prior`**: Allows the latest `NumStages` to still be in progress while waiting for all previous requests. For example, with N total copies requested, it waits until the first N-NumStages are done, while the last NumStages might still be in progress [CUDA_C_Programming_Guide:L12707-L12722].

## Requirements

*   **Compute Capability**: 5.0 minimum, 8.0 for asynchronicity [CUDA_C_Programming_Guide:L12707-L12722].
*   **Header**: `cooperative_groups/memcpy_async.h` must be included [CUDA_C_Programming_Guide:L12707-L12722].
*   **Language**: C++11 [CUDA_C_Programming_Guide:L12707-L12722].

## Example

The following example streams data from global memory into a limited-sized shared memory block to operate on in multiple stages. As stage N is kicked off, the kernel waits on and operates on stage N-1 using `wait_prior`.

```cpp
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
        // Kick off the next request...
        cg::memcpy_async(tb, local_smem[stage ^ 1], elementsInShared, global_data +
                         index, elementsPerThreadBlock - index);
        
        // ... but we wait on the one before it
        cg::wait_prior<1>(tb);

        // It's now available and we can work with local_smem[stage] here
        // (...)

        // Calculate the amount of data that was actually copied, for the next iteration.
        copy_count = min(elementsInShared, elementsPerThreadBlock - index);
        index += copy_count;

        // A cg::sync(tb) might be needed here depending on whether
        // the work done with local_smem[stage] can release threads to race ahead or not
        
        // Wrap to the next stage
        stage ^= 1;
    }
    
    cg::wait(tb);
    // The last local_smem[stage] can be handled here
}
```

[CUDA_C_Programming_Guide:L12723-L12774]
