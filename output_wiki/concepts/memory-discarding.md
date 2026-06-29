# Memory Discarding in Unified Memory

Memory discarding is a feature in CUDA Unified Memory that allows applications to explicitly inform the runtime that the contents of specified memory ranges are no longer useful. This mechanism helps optimize performance by preventing the Unified Memory driver from performing redundant automatic memory transfers, which can occur due to fault-based migration or memory evictions required for device memory oversubscription [CUDA_C_Programming_Guide:L21259-L21305].

## APIs

### cudaMemDiscardBatchAsync

The `cudaMemDiscardBatchAsync` API allows applications to mark address ranges as discarded. This informs the Unified Memory driver that the application has consumed the contents in the range and there is no need to migrate this data on prefetches or page evictions to make room for other allocations [CUDA_C_Programming_Guide:L21259-L21305].

**Function Signature:**

```c
cudaError_t cudaMemDiscardBatchAsync(void **dptrs,
                               size_t *sizes,
                               size_t count,
                               unsigned long long flags,
                               cudaStream_t stream);
```

**Parameters:**
- `dptrs`: An array of pointers to the start of each memory range.
- `sizes`: An array of sizes for each memory range. This array must be of the same length as `dptrs` as specified by `count`.
- `count`: The number of memory ranges to discard.
- `flags`: Reserved for future use (typically 0).
- `stream`: The CUDA stream on which the operation is executed.

**Constraints:**
- Both `dptrs` and `sizes` arrays must be of the same length as specified by `count`.
- Each memory range must refer to managed memory allocated via `cudaMallocManaged` or declared via `__managed__` variables [CUDA_C_Programming_Guide:L21259-L21305].

### cudaMemDiscardAndPrefetchBatchAsync

The `cudaMemDiscardAndPrefetchBatchAsync` API combines both discard and prefetch operations into a single call. This is semantically equivalent to calling `cudaMemDiscardBatchAsync` followed by `cudaMemPrefetchBatchAsync`, but is more optimal. It is useful when the application needs the memory to be on a target location but does not need the contents of the memory [CUDA_C_Programming_Guide:L21259-L21305].

**Function Signature:**

```c
cudaError_t cudaMemDiscardAndPrefetchBatchAsync(void **dptrs,
                                                size_t *sizes,
                                                size_t count,
                                                struct cudaMemLocation *prefetchLocs,
                                                size_t *prefetchLocIdxs,
                                                size_t numPrefetchLocs,
                                                unsigned long long flags,
                                                cudaStream_t stream);
```

**Parameters:**
- `prefetchLocs`: An array specifying the destinations for prefetching.
- `prefetchLocIdxs`: An array indicating which operations each prefetch location applies to. For example, if a batch has 10 operations and the first 6 should be prefetched to one location while the remaining 4 to another, then `numPrefetchLocs` would be 2, `prefetchLocIdxs` would be `{0, 6}`, and `prefetchLocs` would contain the two destination locations.
- `numPrefetchLocs`: The number of unique prefetch locations specified in `prefetchLocs`.

## Important Considerations

- **Indeterminate Values:** Reading from a discarded range without a subsequent write or prefetch will return an indeterminate value [CUDA_C_Programming_Guide:L21259-L21305].
- **Undoing Discard:** The discard operation can be undone by writing to the range or prefetching it via `cudaMemPrefetchAsync` [CUDA_C_Programming_Guide:L21259-L21305].
- **Undefined Behavior:** Any reads, writes, or prefetches that occur simultaneously with the discard operation result in undefined behavior [CUDA_C_Programming_Guide:L21259-L21305].
- **Hardware Requirements:** All devices involved must have a non-zero value for `cudaDevAttrConcurrentManagedAccess` [CUDA_C_Programming_Guide:L21259-L21305].
