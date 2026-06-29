# labeled_partition

`labeled_partition` is a collective operation in the CUDA Cooperative Groups library that partitions a parent group into one-dimensional subgroups. Within these subgroups, threads are coalesced based on a provided label value.

## Function Signature

The function is available in two template forms:

```cpp
template <typename Label>
coalesced_group labeled_partition(const coalesced_group& g, Label label);

template <unsigned int Size, typename Label>
coalesced_group labeled_partition(const thread_block_tile<Size>& g, Label label);
```

## Description

The implementation evaluates the `label` condition and assigns threads that have the same value for `label` into the same subgroup [CUDA_C_Programming_Guide:L12504-L12524]. The `Label` parameter can be any integral type [CUDA_C_Programming_Guide:L12504-L12524].

This is a collective operation, meaning the implementation may cause the calling thread to wait until all members of the parent group have invoked the operation before resuming execution [CUDA_C_Programming_Guide:L12504-L12524].

## Requirements

- **Compute Capability**: 7.0 minimum [CUDA_C_Programming_Guide:L12504-L12524].
- **Language Standard**: C++11 [CUDA_C_Programming_Guide:L12504-L12524].

## Caveats

Note that this functionality is still being evaluated and may slightly change in the future [CUDA_C_Programming_Guide:L12504-L12524].
