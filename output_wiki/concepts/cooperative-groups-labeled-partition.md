# labeled_partition

A collective operation that partitions the parent group into one-dimensional subgroups based on a label value. Threads with the same label value are assigned to the same subgroup.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L12504-L12525

Citation: [CUDA_C_Programming_Guide:L12504-L12525]

````text
## 11.5.2. labeled\_partition

```txt
template <typename Label>
coalesced_group labeled_partition(const coalesced_group& g, Label label);
```

```txt
template <unsigned int Size, typename Label>
coalesced_group labeled_partition(const thread_block_tile<Size>& g, Label label);
```

The labeled\_partition method is a collective operation that partitions the parent group into onedimensional subgroups within which the threads are coalesced. The implementation will evaluate a condition label and assign threads that have the same value for label into the same group.

Label can be any integral type.

The implementation may cause the calling thread to wait until all the members of the parent group have invoked the operation before resuming execution.

Note: This functionality is still being evaluated and may slightly change in the future.

Codegen Requirements: Compute Capability 7.0 minimum, C++11
````
