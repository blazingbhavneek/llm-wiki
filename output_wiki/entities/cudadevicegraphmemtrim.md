# cudaDeviceGraphMemTrim

`cudaDeviceGraphMemTrim` is a CUDA API function designed to explicitly release physical memory reserved by graph memory nodes back to the operating system (OS). It operates within the context of the graph memory pool, which is distinct from the stream-ordered memory allocator.

## Purpose and Behavior

Due to the pool-management behavior of asynchronous allocation, destroying a graph that contains memory nodes does not immediately return physical memory to the OS, even if those allocations are technically free. This retained memory remains reserved by the driver for potential reuse by the current process.

`cudaDeviceGraphMemTrim` addresses this by unmaping and releasing any physical memory reserved by graph memory nodes that is **not actively in use**. The function ensures that:

*   Allocations that have not been freed are considered actively in use and are not impacted.
*   Graphs that are scheduled or currently running are considered actively in use and are not impacted.

## Impact on Applications

Using `cudaDeviceGraphMemTrim` makes the released physical memory available to other allocation APIs, other applications, or other processes. However, this action has performance implications for the CUDA application itself:

*   **Reallocation and Remapping:** When the trimmed graphs are launched next, CUDA must reallocate and remap the memory. This can introduce latency during subsequent graph executions.
*   **Memory Pool Isolation:** The graph memory pool is not exposed to the stream-ordered memory allocator. Therefore, `cudaDeviceGraphMemTrim` operates on a different pool than `cudaMemPoolTrimTo()`.

## Monitoring and Attributes

Applications can query the graph memory footprint using the `cudaDeviceGetGraphMemAttribute` API. Two key attributes are available for tracking memory usage and the effectiveness of memory sharing mechanisms:

*   **`cudaGraphMemAttrReservedMemCurrent`**: Returns the total amount of physical memory reserved by the driver for graph allocations in the current process.
*   **`cudaGraphMemAttrUsedMemCurrent`**: Returns the amount of physical memory currently mapped by at least one graph.

These attributes are useful for examining how much memory is saved by the sharing mechanism and for tracking when new physical memory is acquired by CUDA for allocating graphs.

## References

- [CUDA_C_Programming_Guide:L16243-L16248]
