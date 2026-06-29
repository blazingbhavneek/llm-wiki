# cudaGraphInstantiateFlagAutoFreeOnLaunch

The `cudaGraphInstantiateFlagAutoFreeOnLaunch` flag modifies the behavior of graph instantiation to allow a graph to be relaunched even if it contains unfreed memory allocations. Under normal circumstances, CUDA prevents a graph from being relaunched if it has unfreed allocations, as multiple allocations at the same address would result in memory leaks [CUDA_C_Programming_Guide:L16132-L16139].

When this flag is used, the launch automatically inserts an asynchronous free of the unfreed allocations [CUDA_C_Programming_Guide:L16132-L16139]. This feature is particularly useful for single-producer multiple-consumer algorithms. In such scenarios, a producer graph creates several allocations, and a varying set of consumers accesses those allocations depending on runtime conditions [CUDA_C_Programming_Guide:L16132-L16139]. Because consumers cannot safely free the allocations (as a subsequent consumer may require access), auto free on launch allows the launch loop to avoid tracking the producer's allocations, isolating that information to the producer's creation and destruction logic [CUDA_C_Programming_Guide:L16132-L16139].

## Caveats

The `cudaGraphInstantiateFlagAutoFreeOnLaunch` flag does not change the behavior of graph destruction [CUDA_C_Programming_Guide:L16132-L16139]. The application must explicitly free the unfreed memory to avoid memory leaks, even for graphs instantiated with this flag [CUDA_C_Programming_Guide:L16132-L16139].

## See Also

* `cudaGraphInstantiate`
