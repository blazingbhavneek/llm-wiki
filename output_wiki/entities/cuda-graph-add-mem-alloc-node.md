# cudaGraphAddMemAllocNode / cudaGraphAddMemFreeNode

Graph memory nodes may be explicitly created with the memory node creation APIs, `cudaGraphAddMemAllocNode` and `cudaGraphAddMemFreeNode` [CUDA_C_Programming_Guide:L15943-L15986]. These nodes enable the management of memory lifetime within the context of a CUDA graph execution [CUDA_C_Programming_Guide:L15943-L15986].

## API Overview

### cudaGraphAddMemAllocNode
This function creates an allocation node within a graph [CUDA_C_Programming_Guide:L15943-L15986]. The address of the allocated memory is returned to the user in the `dptr` field of the passed `CUDA_MEM_ALLOC_NODE_PARAMS` structure [CUDA_C_Programming_Guide:L15943-L15986].

### cudaGraphAddMemFreeNode
This function creates a free node within a graph [CUDA_C_Programming_Guide:L15943-L15986]. It is used to deallocate memory previously allocated by an allocation node [CUDA_C_Programming_Guide:L15943-L15986].

## Dependency and Ordering Rules

Proper ordering of graph nodes is critical for memory safety when using graph memory nodes [CUDA_C_Programming_Guide:L15943-L15986].

1.  **Allocation Order**: All operations using graph allocations inside the allocating graph must be ordered after the allocating node [CUDA_C_Programming_Guide:L15943-L15986]. For example, if a kernel node depends on the allocation node, it can safely access the memory [CUDA_C_Programming_Guide:L15943-L15986]. If a kernel node does not depend on the allocation node, it cannot safely access the memory, even if a free node depends on it [CUDA_C_Programming_Guide:L15943-L15986].
2.  **Freeing Order**: Any free nodes must be ordered after all uses of the allocation within the graph [CUDA_C_Programming_Guide:L15943-L15986]. A free node must depend on all kernel nodes that use the allocation [CUDA_C_Programming_Guide:L15943-L15986]. If a kernel node does not depend on the free node, it must not access the freed graph allocation [CUDA_C_Programming_Guide:L15943-L15986].

## Example Implementation

The following code snippet demonstrates the creation of a graph with an allocation node, kernel nodes that use the allocation, and a free node [CUDA_C_Programming_Guide:L15943-L15986].

```txt
// Create the graph - it starts out empty
cudaGraphCreate(&graph, 0);

// parameters for a basic allocation
cudaMemAllocNodeParams params = {};
params.poolProps.allocType = cudaMemAllocationTypePinned;
params.poolProps.location.type = cudaMemLocationTypeDevice;
// specify device 0 as the resident device
params.poolProps.location.id = 0;
params.bytesize = size;

cudaGraphAddMemAllocNode(&allocNode, graph, NULL, 0, &params);
nodeParams->kernelParams[0] = params.dptr;
cudaGraphAddKernelNode(&a, graph, &allocNode, 1, &nodeParams);
cudaGraphAddKernelNode(&b, graph, &a, 1, &nodeParams);
cudaGraphAddKernelNode(&c, graph, &a, 1, &nodeParams);
cudaGraphNode_t dependencies[2];
// kernel nodes b and c are using the graph allocation, so the freeing node must
→ depend on them.  Since the dependency of node b on node a establishes an indirect
→ dependency, the free node does not need to explicitly depend on node a.
dependencies[0] = b;
dependencies[1] = c;
cudaGraphAddMemFreeNode(&freeNode, graph, dependencies, 2, params.dptr);
// free node does not depend on kernel node d, so it must not access the freed graph
→ allocation.
cudaGraphAddKernelNode(&d, graph, &c, 1, &nodeParams);

// node e does not depend on the allocation node, so it must not access the
→ allocation.  This would be true even if the freeNode depended on kernel node e.
cudaGraphAddKernelNode(&e, graph, NULL, 0, &nodeParams);
```

In this example:
- Kernel nodes `a`, `b`, and `c` are ordered after the allocation node and before the free node, allowing them to access the allocation [CUDA_C_Programming_Guide:L15943-L15986].
- Kernel node `e` is not ordered after the alloc node and therefore cannot safely access the memory [CUDA_C_Programming_Guide:L15943-L15986].
- Kernel node `d` is not ordered before the free node, therefore it cannot safely access the memory [CUDA_C_Programming_Guide:L15943-L15986].

## See Also

- CUDA Graph Node APIs
- CUDA Memory Allocation
