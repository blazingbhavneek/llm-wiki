# CUDA Graph Child Graph Ownership

CUDA 12.9 introduces the ability to move child graph ownership to a parent graph [CUDA_C_Programming_Guide:L16323-L16363]. This feature allows child graphs containing memory allocation and free nodes to be independently constructed prior to their addition into a parent graph [CUDA_C_Programming_Guide:L16323-L16363].

## Restrictions on Moved Child Graphs

Once a child graph's ownership has been moved to a parent graph, the following restrictions apply [CUDA_C_Programming_Guide:L16323-L16363]:

*   The child graph cannot be independently instantiated or destroyed.
*   The child graph cannot be added as a child graph of a separate parent graph.
*   The child graph cannot be used as an argument to `cuGraphExecUpdate`.
*   No additional memory allocation or free nodes can be added to the child graph.

## Example Usage

The following code example demonstrates the creation of a child graph with memory allocation and free nodes, followed by moving its ownership to a parent graph [CUDA_C_Programming_Guide:L16323-L16363]:

```txt
// Create the child graph
cudaGraphCreate(&child, 0);

// parameters for a basic allocation
cudaMemAllocNodeParams params = {};
params.poolProps.allocType = cudaMemAllocationTypePinned;
params.poolProps.location.type = cudaMemLocationTypeDevice;
// specify device 0 as the resident device
params.poolProps.location.id = 0;
params.bytesize = size;

cudaGraphAddMemAllocNode(&allocNode, graph, NULL, 0, &params);
// Additional nodes using the allocation could be added here
cudaGraphAddMemFreeNode(&freeNode, graph, &allocNode, 1, params.dptr);

// Create the parent graph
cudaGraphCreate(&parent, 0);

// Move the child graph to the parent graph
cudaGraphNodeParams childNodeParams = { cudaGraphNodeTypeGraph };
childNodesParams.graph.graph = child;
childNodesParams.graph.ownership = cudaGraphChildGraphOwnershipMove;
cudaGraphAddNode(&parentNode, parent, NULL, NULL, 0, &childNodesParams);
```
