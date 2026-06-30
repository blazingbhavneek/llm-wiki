# Minimize Memory Thrashing

Provides recommendations for managing device memory allocation to avoid performance degradation, including sizing allocations, batching cudaMalloc/cudaFree calls, and using cudaMallocManaged for oversubscription.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L6519-L6531

Citation: [CUDA_C_Programming_Guide:L6519-L6531]

````text

## 8.5. Minimize Memory Thrashing

Applications that constantly allocate and free memory too often may find that the allocation calls tend to get slower over time up to a limit. This is typically expected due to the nature of releasing memory back to the operating system for its own use. For best performance in this regard, we recommend the following:

▶ Try to size your allocation to the problem at hand. Don’t try to allocate all available memory with cudaMalloc / cudaMallocHost / cuMemCreate, as this forces memory to be resident immediately and prevents other applications from being able to use that memory. This can put more pressure on operating system schedulers, or just prevent other applications using the same GPU from running entirely.

Try to allocate memory in appropriately sized allocations early in the application and allocations only when the application does not have any use for it. Reduce the number of cudaMalloc+cudaFree calls in the application, especially in performance-critical regions.

▶ If an application cannot allocate enough device memory, consider falling back on other memory types such as cudaMallocHost or cudaMallocManaged, which may not be as performant, but will enable the application to make progress.

For platforms that support the feature, cudaMallocManaged allows for oversubscription, and with the correct cudaMemAdvise policies enabled, will allow the application to retain most if not all the performance of cudaMalloc. cudaMallocManaged also won’t force an allocation to be resident until it is needed or prefetched, reducing the overall pressure on the operating system schedulers and better enabling multi-tenet use cases.
````
