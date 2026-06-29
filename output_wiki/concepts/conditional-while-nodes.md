# Conditional WHILE Nodes

A **Conditional WHILE Node** is a specific type of conditional node in CUDA graphs where the body graph is executed as long as the condition is non-zero [CUDA_C_Programming_Guide:L3282-L3337]. The condition is evaluated when the node is executed and again after the completion of the body graph [CUDA_C_Programming_Guide:L3282-L3337].

## Behavior

The execution flow of a WHILE node involves:
1. Evaluation of the condition upon node execution [CUDA_C_Programming_Guide:L3282-L3337].
2. Execution of the body graph [CUDA_C_Programming_Guide:L3282-L3337].
3. Re-evaluation of the condition after the body graph completes [CUDA_C_Programming_Guide:L3282-L3337].
4. Repetition of steps 2 and 3 if the condition remains non-zero [CUDA_C_Programming_Guide:L3282-L3337].

## Implementation

Creating a graph containing a WHILE conditional node involves several steps, including the creation of a conditional handle and the population of the body graph using the graph API [CUDA_C_Programming_Guide:L3282-L3337].

### Handle Creation

The conditional handle is typically created using `cudaGraphConditionalHandleCreate` [CUDA_C_Programming_Guide:L3282-L3337]. To avoid the need for an upstream kernel to provide the initial condition, `cudaGraphCondAssignDefault` can be used as the initial value [CUDA_C_Programming_Guide:L3282-L3337].

```c
cudaGraphConditionalHandle handle;
cudaGraphConditionalHandleCreate(&handle, graph, 1, cudaGraphCondAssignDefault);
```

### Node Configuration

The conditional node is added to the graph with specific parameters defining its type as `cudaGraphCondTypeWhile` [CUDA_C_Programming_Guide:L3282-L3337].

```c
cudaGraphNodeParams cParams = { cudaGraphNodeTypeConditional };
cParams.conditional.handle = handle;
cParams.conditional.type = cudaGraphCondTypeWhile;
cParams.conditional.size = 1;
cudaGraphAddNode(&node, graph, NULL, NULL, 0, &cParams);
```

### Body Graph Population

The body of the conditional is populated by adding nodes to the `phGraph_out` associated with the conditional handle [CUDA_C_Programming_Guide:L3282-L3337].

```c
cudaGraph_t bodyGraph = cParams.conditional.phGraph_out[0];

cudaGraphNodeParams params = { cudaGraphNodeTypeKernel };
params.kernel.func = (void *)loopKernel;
params.kernel.gridDim.x = params.kernel.gridDim.y = params.kernel.gridDim.z = 1;
params.kernel.blockDim.x = params.kernel.blockDim.y = params.kernel.blockDim.z = 1;
params.kernel.kernelParams = kernelArgs;
kernelArgs[0] = &handle;

cudaGraphAddNode(&node, bodyGraph, NULL, NULL, 0, &params);
```

### Example Kernel

The kernel executed within the WHILE body typically receives the conditional handle and updates the condition. For example, a loop kernel might decrement a counter and return 1 if the counter is non-zero, or 0 otherwise [CUDA_C_Programming_Guide:L3282-L3337].

```c
__global__ void loopKernel(cudaGraphConditionalHandle handle)
{
    static int count = 10;
    cudaGraphSetConditional(handle, --count ? 1 : 0);
}
```

### Execution

After setting up the graph and body, the graph is instantiated and launched [CUDA_C_Programming_Guide:L3282-L3337].

```c
cudaGraphInstantiate(&graphExec, graph, NULL, NULL, 0);
cudaGraphLaunch(graphExec, 0);
cudaDeviceSynchronize();
```

## References

- [CUDA_C_Programming_Guide:L3282-L3337]
