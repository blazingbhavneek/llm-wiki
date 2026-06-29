# Conditional IF Nodes

Conditional IF nodes are a type of CUDA graph node that allows for dynamic control flow within a graph. The body graph of an IF node is executed once if the condition is non-zero when the node is executed [CUDA_C_Programming_Guide:L3165-L3281].

## Basic IF Node (Non-Zero Condition)

In the basic configuration, an IF node executes its associated body graph if the condition value is non-zero [CUDA_C_Programming_Guide:L3165-L3281]. The condition value is typically set by an upstream kernel using `cudaGraphSetConditional` [CUDA_C_Programming_Guide:L3165-L3281].

### Creation and Population

To create a graph containing an IF conditional node:

1.  Create the graph and a conditional handle [CUDA_C_Programming_Guide:L3165-L3281].
2.  Add an upstream kernel node that sets the conditional handle value [CUDA_C_Programming_Guide:L3165-L3281].
3.  Add the conditional node itself, specifying `cudaGraphCondTypeIf` as the type [CUDA_C_Programming_Guide:L3165-L3281].
4.  Populate the body graph using the API [CUDA_C_Programming_Guide:L3165-L3281].

```cpp
cudaGraph_t graph;
cudaGraphExec_t graphExec;
cudaGraphNode_t node;
void *kernelArgs[1];
int value = 1;

cudaGraphCreate(&graph, 0);

cudaGraphConditionalHandle handle;
cudaGraphConditionalHandleCreate(&handle, graph);

// Use a kernel upstream of the conditional to set the handle value
cudaGraphNodeParams params = { cudaGraphNodeTypeKernel };
params.kernel.func = (void *)setHandle;
params.kernel.gridDim.x = params.kernel.gridDim.y = params.kernel.gridDim.z = 1;
params.kernel.blockDim.x = params.kernel.blockDim.y = params.kernel.blockDim.z = 1;
params.kernel.kernelParams = kernelArgs;
kernelArgs[0] = &handle;
cudaGraphAddNode(&node, graph, NULL, NULL, 0, &params);

cudaGraphNodeParams cParams = { cudaGraphNodeTypeConditional };
cParams.conditional.handle = handle;
cParams.conditional.type   = cudaGraphCondTypeIf;
cParams.conditional.size   = 1;
cudaGraphAddNode(&node, graph, &node, NULL, 1, &cParams);

cudaGraph_t bodyGraph = cParams.conditional.phGraph_out[0];

// Populate the body of the conditional node
...
cudaGraphAddNode(&node, bodyGraph, NULL, NULL, 0, &params);

cudaGraphInstantiate(&graphExec, graph, NULL, NULL, 0);
cudaGraphLaunch(graphExec, 0);
cudaDeviceSynchronize();

cudaGraphExecDestroy(graphExec);
cudaGraphDestroy(graph);
```

## Extended IF Node (Zero Condition Support)

Starting in CUDA 12.8, IF nodes can also have an optional second body graph which is executed once when the node is executed if the condition value is zero [CUDA_C_Programming_Guide:L3165-L3281].

### Implementation Details

To support the optional second body graph:

1.  Set the `size` field of the conditional node parameters to 2 [CUDA_C_Programming_Guide:L3165-L3281].
2.  Access the second body graph via `cParams.conditional.phGraph_out[1]` [CUDA_C_Programming_Guide:L3165-L3281].
3.  Populate both the `ifBodyGraph` and `elseBodyGraph` [CUDA_C_Programming_Guide:L3165-L3281].

```cpp
void graphSetup() {
    cudaGraph_t graph;
    cudaGraphExec_t graphExec;
    cudaGraphNode_t node;
    void *kernelArgs[1];
    int value = 1;

    cudaGraphCreate(&graph, 0);

    cudaGraphConditionalHandle handle;
    cudaGraphConditionalHandleCreate(&handle, graph);

    // Use a kernel upstream of the conditional to set the handle value
    cudaGraphNodeParams params = { cudaGraphNodeTypeKernel };
    params.kernel.func = (void *)setHandle;
    params.kernel.gridDim.x = params.kernel.gridDim.y = params.kernel.gridDim.z = 1;
    params.kernel.blockDim.x = params.kernel.blockDim.y = params.kernel.blockDim.z = 1;
    params.kernel.kernelParams = kernelArgs;
    kernelArgs[0] = &handle;
    cudaGraphAddNode(&node, graph, NULL, NULL, 0, &params);

    cudaGraphNodeParams cParams = { cudaGraphNodeTypeConditional };
    cParams.conditional.handle = handle;
    cParams.conditional.type = cudaGraphCondTypeIf;
    cParams.conditional.size = 2; // Note that size is now set to '2'
    cudaGraphAddNode(&node, graph, &node, NULL, 1, &cParams);

    cudaGraph_t ifBodyGraph = cParams.conditional.phGraph_out[0];
    cudaGraph_t elseBodyGraph = cParams.conditional.phGraph_out[1];

    // Populate the body graphs of the conditional node
    ...
    cudaGraphAddNode(&node, ifBodyGraph, NULL, NULL, 0, &params);
    ...
    cudaGraphAddNode(&node, elseBodyGraph, NULL, NULL, 0, &params);

    cudaGraphInstantiate(&graphExec, graph, NULL, NULL, 0);
    cudaGraphLaunch(graphExec, 0);
    cudaDeviceSynchronize();

    cudaGraphExecDestroy(graphExec);
    cudaGraphDestroy(graph);
}
```

## Related Types

*   `cudaGraphCondTypeIf`: The type identifier for conditional IF nodes [CUDA_C_Programming_Guide:L3165-L3281].
*   `cudaGraphConditionalHandle`: The handle used to link the condition-setting kernel to the conditional node [CUDA_C_Programming_Guide:L3165-L3281].
