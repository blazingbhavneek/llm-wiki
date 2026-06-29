# reduce

The `reduce` function performs a reduction operation on data provided by each thread named in a specified cooperative group. It supports hardware acceleration for common arithmetic and logical operations on devices with Compute Capability 8.0 or higher, while providing a software fallback for older hardware.

## Header

The `cooperative_groups/reduce.h` header must be included to use these functions.

## Synchronous Reduce

### Signature

```cpp
template <typename TyGroup, typename TyArg, typename TyOp>
auto reduce(const TyGroup& group, TyArg&& val, TyOp&& op) -> decltype(op(val, val));
```

### Parameters

*   **group**: A valid group type, specifically `coalesced_group` or `thread_block_tile` [CUDA_C_Programming_Guide:L12775-L12818].
*   **val**: A value satisfying the following requirements:
    *   Must be trivially copyable (`std::is_trivially_copyable<TyArg>::value == true`) [CUDA_C_Programming_Guide:L12775-L12818].
    *   Size constraints: `sizeof(T) <= 32` for `coalesced_group` and tiles of size 32 or less; `sizeof(T) <= 8` for larger tiles [CUDA_C_Programming_Guide:L12775-L12818].
    *   Must have suitable arithmetic or comparative operators for the given function object [CUDA_C_Programming_Guide:L12775-L12818].
    *   Different threads in the group can pass different values for this argument [CUDA_C_Programming_Guide:L12775-L12818].
*   **op**: A valid function object. Hardware acceleration is available for integral types using `plus()`, `less()`, `greater()`, `bit_and()`, `bit_xor()`, and `bit_or()` [CUDA_C_Programming_Guide:L12775-L12818]. These must be constructed (e.g., `plus<int>()`) [CUDA_C_Programming_Guide:L12775-L12818]. Lambdas and other function objects invocable via `operator()` are also supported [CUDA_C_Programming_Guide:L12775-L12818].

### Hardware Acceleration

Hardware acceleration is available on Compute Capability 8.0 and higher devices for the following operations:
*   Arithmetic: `add`, `min`, `max` [CUDA_C_Programming_Guide:L12775-L12818].
*   Logical: `and`, `or`, `xor` [CUDA_C_Programming_Guide:L12775-L12818].

Only 4-byte (4B) types are accelerated by hardware [CUDA_C_Programming_Guide:L12775-L12818].

### Codegen Requirements

*   Minimum Compute Capability: 5.0 [CUDA_C_Programming_Guide:L12775-L12818].
*   Compute Capability 8.0 required for hardware acceleration [CUDA_C_Programming_Guide:L12775-L12818].
*   C++11 [CUDA_C_Programming_Guide:L12775-L12818].

## Asynchronous Reduce

Asynchronous variants calculate the result to store to or update a specified destination by one of the participating threads, rather than returning it to each thread. To observe the effect of these calls, the group of threads or a larger group containing them must be synchronized [CUDA_C_Programming_Guide:L12775-L12818].

### Variants

1.  **Atomic Update**: `reduce_update_async`
    ```cpp
    template <typename TyGroup, typename TyArg, typename TyAtomic, typename TyOp>
    void reduce_update_async(const TyGroup& group, TyAtomic& atomic, TyArg&& val, TyOp&& op);
    ```
    The result of the reduction is used to atomically update the `atomic` argument according to the specified operator (e.g., the result is atomically added to the atomic in the case of `cg::plus()`) [CUDA_C_Programming_Guide:L12775-L12818].

2.  **Atomic Store**: `reduce_store_async` (Atomic)
    ```cpp
    template <typename TyGroup, typename TyArg, typename TyAtomic, typename TyOp>
    void reduce_store_async(const TyGroup& group, TyAtomic& atomic, TyArg&& val, TyOp&& op);
    ```

3.  **Pointer Store**: `reduce_store_async` (Pointer)
    ```cpp
    template <typename TyGroup, typename TyArg, typename TyOp>
    void reduce_store_async(const TyGroup& group, TyArg* ptr, TyArg&& val, TyOp&& op);
    ```
    The result of the reduction will be weakly stored into the destination pointer [CUDA_C_Programming_Guide:L12775-L12818].

### Atomic Requirements

For the atomic store or update variants, the `atomic` argument can be either `cuda::atomic` or `cuda::atomic_ref` available in the CUDA C++ Standard Library [CUDA_C_Programming_Guide:L12775-L12818]. This variant is available only on platforms and devices where these types are supported [CUDA_C_Programming_Guide:L12775-L12818].

*   The type held by the atomic must match the type of `TyArg` [CUDA_C_Programming_Guide:L12775-L12818].
*   The scope of the atomic must include all threads in the group [CUDA_C_Programming_Guide:L12775-L12818].
*   If multiple groups are using the same atomic concurrently, the scope must include all threads in all groups using it [CUDA_C_Programming_Guide:L12775-L12818].
*   Atomic update is performed with relaxed memory ordering [CUDA_C_Programming_Guide:L12775-L12818].

## Examples

### Approximate Standard Deviation

The following example calculates the approximate standard deviation of an integer vector using `cg::reduce` with `cg::plus<int>` to enable hardware acceleration for addition [CUDA_C_Programming_Guide:L12819-L12853].

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
    // addition
    int avg = cg::reduce(tile, thread_sum, cg::plus<int>() ) / length;

    int thread_diffs_sum = 0;
    for (int i = tile.thread_rank(); i < length; i += tile.num_threads()) {
        int diff = vec[i] - avg;
        thread_diffs_sum += diff * diff;
    }

    // temporarily use floats to calculate the square root
    float diff_sum = static_cast<float>(cg::reduce(tile, thread_diffs_sum, cg::plus<int>() )) / length;

    return static_cast<int>(sqrtf(diff_sum));
}
```

### Block Wide Reduction with Async Update

The following example accepts input in `*A` and outputs a result into `*sum` by spreading the data equally within the block and using `reduce_update_async` [CUDA_C_Programming_Guide:L12854-L12888].

```cpp
#include <cooperative_groups.h>
#include <cooperative_groups/reduce.h>
namespace cg=cooperative_groups;

/// The following example accepts input in *A and outputs a result into *sum
/// It spreads the data equally within the block
__device__ void block_reduce(const int* A, int count, cuda::atomic<int, cuda::thread_->scope_block>& total_sum) {
    auto block = cg::this_thread_block();
    auto tile = cg::tiled_partition<32>(block);
    int thread_sum = 0;

    // Stride loop over all values, each thread accumulates its part of the array.
    for (int i = block.thread_rank(); i < count; i += block.size()) {
        thread_sum += A[i];
    }

    // reduce thread sums across the tile, add the result to the atomic
    // cg::plus<int> allows cg::reduce() to know it can use hardware acceleration for
    // addition
    cg::reduce_update_async(tile, total_sum, thread_sum, cg::plus<int>());
    // synchronize the block, to ensure all async reductions are ready
    block.sync();
}
```
