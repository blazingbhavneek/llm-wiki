# binary_partition

`binary_partition` is a collective operation within the CUDA Cooperative Groups (CG) library that partitions a parent group into one-dimensional subgroups. It is a specialized form of `labeled_partition` where the label is restricted to boolean values (0 or 1).

## Syntax

The function provides two overloads:

```cpp
coesced_group binary_partition(const coalesced_group& g, bool pred);

template <unsigned int Size>
coalesced_group binary_partition(const thread_block_tile<Size>& g, bool pred);
```

## Behavior

The implementation evaluates a predicate for each thread in the parent group. Threads that evaluate to the same boolean value are assigned to the same subgroup. Within these subgroups, threads remain coalesced.

As a collective operation, the implementation may cause the calling thread to wait until all members of the parent group have invoked the operation before resuming execution.

## Requirements

- **Compute Capability**: 7.0 minimum
- **Language Standard**: C++11

## Example

The following example demonstrates dividing a 32-sized tile into two groups: one containing threads with odd numbers and one containing threads with even numbers.

```cpp
/// This example divides a 32-sized tile into a group with odd
/// numbers and a group with even numbers
__global__ void oddEven(int *inputArr) {
    auto block = cg::this_thread_block();
    auto tile32 = cg::tiled_partition<32>(block);

    // inputArr contains random integers
    int elem = inputArr[block.thread_rank()];
    // after this, tile32 is split into 2 groups,
    // a subtile where elem&1 is true and one where its false
    auto subtile = cg::binary_partition(tile32, (elem & 1));
}
```

## Caveats

This functionality is still being evaluated and may slightly change in the future.

## References

- [CUDA_C_Programming_Guide:L12525-L12543]
- [CUDA_C_Programming_Guide:L12544-L12560]
