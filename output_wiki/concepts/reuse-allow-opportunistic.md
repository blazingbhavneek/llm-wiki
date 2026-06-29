# cudaMemPoolReuseAllowOpportunistic

The `cudaMemPoolReuseAllowOpportunistic` policy controls whether the CUDA memory allocator is permitted to reuse previously freed allocations based on the progress of the stream associated with the free operation, even in the absence of explicit event dependencies.

## Behavior

When this policy is enabled, the allocator examines freed allocations to determine if the "free's stream order semantic" has been met. This condition is satisfied when the stream has passed the point of execution indicated by the `cudaFreeAsync` call [CUDA_C_Programming_Guide:L15631-L15647]. If this condition is met, the allocator may fulfill a new allocation request from the same memory pool using the previously freed memory, regardless of whether the new request is on a different stream [CUDA_C_Programming_Guide:L15631-L15647].

### Example Scenario

Consider the following sequence:
1. Memory is allocated asynchronously on `originalStream`.
2. A kernel is launched on `originalStream` using that memory.
3. The memory is freed asynchronously on `originalStream` using `cudaFreeAsync`.
4. The kernel finishes running, and the stream progresses past the free point.
5. A new allocation is requested on `otherStream`.

If `cudaMemPoolReuseAllowOpportunistic` is enabled, the new allocation on `otherStream` can be fulfilled by reusing the memory freed on `originalStream`, based on the observed progress of `originalStream` [CUDA_C_Programming_Guide:L15631-L15647].

## Disabling the Policy

Disabling `cudaMemPoolReuseAllowOpportunistic` prevents this opportunistic reuse based on stream order semantics. However, it does not prevent all forms of reuse. The allocator will still reuse memory that has been made available through CPU synchronization with a stream (e.g., via `cudaStreamSynchronize`) [CUDA_C_Programming_Guide:L15631-L15647].

Furthermore, disabling this policy does not affect the application of `cudaMemPoolReuseFollowEventDependencies`. That policy remains active and continues to govern reuse based on explicit event dependencies [CUDA_C_Programming_Guide:L15631-L15647].

## See Also

- `cudaMemPoolReuseFollowEventDependencies`
- `cudaMallocAsync`
- `cudaFreeAsync`
