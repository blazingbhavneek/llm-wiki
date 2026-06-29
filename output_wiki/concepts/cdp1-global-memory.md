# CDP1 Global Memory

In the Contextual Data Parallelism 1 (CDP1) model, parent and child grids share the same global and constant memory storage, while maintaining distinct local and shared memory spaces [CUDA_C_Programming_Guide:L14388-L14404].

## Coherence and Consistency

Parent and child grids have coherent access to global memory, with weak consistency guarantees between the child and parent [CUDA_C_Programming_Guide:L14388-L14404]. The child grid's view of memory is fully consistent with the parent thread at two specific points in execution:

1. When the child grid is invoked by the parent.
2. When the child grid completes, as signaled by a synchronization API invocation in the parent thread [CUDA_C_Programming_Guide:L14388-L14404].

## Memory Visibility

The visibility of memory operations follows strict ordering rules:

* **Parent to Child:** All global memory operations in the parent thread prior to the child grid’s invocation are visible to the child grid [CUDA_C_Programming_Guide:L14388-L14404].
* **Child to Parent:** All memory operations of the child grid are visible to the parent after the parent has synchronized on the child grid’s completion [CUDA_C_Programming_Guide:L14388-L14404].

### Example Scenario

Consider a parent thread launching a child grid (`child_launch`). The child grid is only guaranteed to see modifications to data made before the child grid was launched. Since thread 0 of the parent performs the launch, the child will be consistent with the memory seen by thread 0 of the parent [CUDA_C_Programming_Guide:L14388-L14404].

* **Before Launch:** Due to a preceding `__syncthreads()` call, the child will see consistent data (e.g., `data[0]=0, data[1]=1, …, data[255]=255`). Without this synchronization, only `data[0]` would be guaranteed to be seen by the child [CUDA_C_Programming_Guide:L14388-L14404].
* **After Return:** When the child grid returns, thread 0 is guaranteed to see modifications made by the threads in its child grid. These modifications become available to the other threads of the parent grid only after a second `__syncthreads()` call [CUDA_C_Programming_Guide:L14388-L14404].

## Deprecation Warning

Explicit synchronization with child kernels from a parent block (i.e., using `cudaDeviceSynchronize()` in device code) is deprecated in CUDA 11.6, removed for compute_90+ compilation, and is slated for full removal in a future CUDA release [CUDA_C_Programming_Guide:L14388-L14404].

## See Also

* Coherence and Consistency (CDP2 version)
* Global Memory (CDP2 version)

[Source: CUDA_C_Programming_Guide:L14388-L14404]
