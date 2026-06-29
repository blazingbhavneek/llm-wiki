# coalesced_group

The `coalesced_group` is a cooperative group type that represents the set of active threads within a warp at a specific point in time. In CUDA's Single Instruction, Multiple Threads (SIMT) architecture, multiprocessors execute threads in groups of 32 called warps. When data-dependent conditional branches cause divergence, the warp serially executes each branch path, disabling threads not on that path. The threads that remain active on a specific path are referred to as coalesced [CUDA_C_Programming_Guide:L12358-L12427].

## Construction and Discovery Pattern

A `coalesced_group` is constructed using the `coalesced_threads()` function. This construction is opportunistic: it returns the set of active threads at the moment of the call and makes no guarantee about which specific threads are returned (provided they are active) or that they will remain coalesced throughout execution. Threads may diverge again after a collective operation completes [CUDA_C_Programming_Guide:L12358-L12427].

```cpp
cg::coalesced_group active = coalesced_threads();
```

This pattern is commonly used when developers need to work with the current active set of threads without making assumptions about their presence. For example, in an "aggregating atomic increment across threads in a warp" scenario, the group allows replacing low-level intrinsics with higher-level cooperative primitives [CUDA_C_Programming_Guide:L12428-L12463].

### Example Usage

Consider a kernel where only specific threads (e.g., threads 2, 4, and 8) are active due to a branch. The `coalesced_threads()` call creates a group containing only these active threads, re-indexing them to ranks 0 through 2 [CUDA_C_Programming_Guide:L12358-L12427].

```cpp
__global__ void kernel(int *globalInput) {
    if (threadIdx.x == *globalInput) {
        cg::coalesced_group active = coalesced_threads();
        // active contains threads with ranks 0-2 inclusive
        active.sync();
    }
}
```

This can be compared to legacy intrinsics-based implementations. The following code demonstrates aggregating an atomic increment using `__activemask()` and `__shfl_sync()` [CUDA_C_Programming_Guide:L12428-L12463]:

```c
{
    unsigned int writemask = __activemask();
    unsigned int total = __popc(writemask);
    unsigned int prefix = __popc(writemask & __lanemask_lt());
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

Using Cooperative Groups, the same logic is expressed more clearly [CUDA_C_Programming_Guide:L12428-L12463]:

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

## Member Functions

The `coalesced_group` class provides synchronization, querying, and communication functions. Since this group is created by querying active threads, it is considered a single meta-group.

### Synchronization

- `void sync() const`: Synchronizes all threads named in the group [CUDA_C_Programming_Guide:L12358-L12427].

### Querying

- `unsigned long long num_threads() const`: Returns the total number of active threads in the group [CUDA_C_Programming_Guide:L12358-L12427].
- `unsigned long long thread_rank() const`: Returns the rank of the calling thread within the range `[0, num_threads)` [CUDA_C_Programming_Guide:L12358-L12427].
- `unsigned long long meta_group_size() const`: Returns the number of groups created when the parent group was partitioned. For groups created via `coalesced_threads()`, this value is always 1 [CUDA_C_Programming_Guide:L12358-L12427].
- `unsigned long long meta_group_rank() const`: Returns the linear rank of the group within the set of tiles partitioned from a parent group. For groups created via `coalesced_threads()`, this value is always 0 [CUDA_C_Programming_Guide:L12358-L12427].

### Communication and Voting

The group provides wrappers for warp shuffle, vote, and match functions [CUDA_C_Programming_Guide:L12358-L12427]:

- `T shfl(T var, unsigned int src_rank) const`: Shuffles data from a source rank [CUDA_C_Programming_Guide:L12358-L12427].
- `T shfl_up(T var, int delta) const`: Shuffles data from a lower rank [CUDA_C_Programming_Guide:L12358-L12427].
- `T shfl_down(T var, int delta) const`: Shuffles data from a higher rank [CUDA_C_Programming_Guide:L12358-L12427].
- `int any(int predicate) const`: Returns true if any thread in the group satisfies the predicate [CUDA_C_Programming_Guide:L12358-L12427].
- `int all(int predicate) const`: Returns true if all threads in the group satisfy the predicate [CUDA_C_Programming_Guide:L12358-L12427].
- `unsigned int ballot(int predicate) const`: Returns a bitmask of threads satisfying the predicate [CUDA_C_Programming_Guide:L12358-L12427].
- `unsigned int match_any(T val) const`: Returns a bitmask of threads whose value matches `val` [CUDA_C_Programming_Guide:L12358-L12427].
- `unsigned int match_all(T val, int &pred) const`: Returns a bitmask of threads whose value matches `val` and sets `pred` to true if all match [CUDA_C_Programming_Guide:L12358-L12427].

### Legacy Aliases

- `unsigned long long size() const`: An alias for `num_threads()` [CUDA_C_Programming_Guide:L12358-L12427].

## Type Constraints for Shuffle

The `shfl`, `shfl_up`, and `shfl_down` functions accept objects of any type when compiled with C++11 or later. Non-integral types are supported provided they satisfy the following constraints [CUDA_C_Programming_Guide:L12358-L12427]:

1. The type must be trivially copyable (`std::is_trivially_copyable<T>::value == true`).
2. The size of the type must be less than or equal to 32 bytes (`sizeof(T) <= 32`).

## Notes

- The `coalesced_group` is always a single meta-group (`meta_group_size() == 1` and `meta_group_rank() == 0`) because it is not derived from a partitioned parent group but rather from a dynamic query of active threads [CUDA_C_Programming_Guide:L12358-L12427].
- While the group guarantees that threads are brought together for the execution of a collective operation, they may diverge again immediately after [CUDA_C_Programming_Guide:L12358-L12427].
