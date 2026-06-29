# Tail Launch

Tail Launch is a specific launch mode for CUDA device graphs that facilitates serial work dependencies on the GPU. Unlike the host environment, where synchronization can be achieved via traditional methods like `cudaDeviceSynchronize()` or `cudaStreamSynchronize()`, these methods are not available for synchronizing device graphs directly from the GPU [CUDA_C_Programming_Guide:L2998-L3045]. Tail launch provides similar functionality by ensuring that a graph executes only when its predecessor's environment is complete [CUDA_C_Programming_Guide:L2998-L3045].

## Execution Semantics

A tail launch executes when a graph’s environment is considered complete, which is defined as the state where the graph and all its children are complete [CUDA_C_Programming_Guide:L2998-L3045]. When a graph completes, the environment of the next graph in the tail launch list replaces the completed environment as a child of the parent environment [CUDA_C_Programming_Guide:L2998-L3045].

Similar to fire-and-forget launches, a graph can have multiple graphs enqueued for tail launch [CUDA_C_Programming_Guide:L2998-L3045]. The execution order is strictly sequential based on the order of enqueueing: the first enqueued graph runs first, followed by the second, and so on [CUDA_C_Programming_Guide:L2998-L3045].

### Nested Tail Launches

Tail launches enqueued by a tail graph will execute before any tail launches enqueued by previous graphs in the tail launch list [CUDA_C_Programming_Guide:L2998-L3045]. These new tail launches execute in the order they are enqueued [CUDA_C_Programming_Guide:L2998-L3045].

## Implementation

Tail launches are initiated using the `cudaGraphLaunch` function with the `cudaStreamGraphTailLaunch` flag [CUDA_C_Programming_Guide:L2998-L3045]. An example implementation involves creating and instantiating device graphs, uploading them to a stream, and then launching a host graph that contains the tail launch kernel [CUDA_C_Programming_Guide:L2998-L3045].

```cpp
__global__ void launchTailGraph(cudaGraphExec_t graph) {
    cudaGraphLaunch(graph, cudaStreamGraphTailLaunch);
}

void graphSetup() {
    cudaGraphExec_t gExec1, gExec2;
    cudaGraph_t g1, g2;

    // Create, instantiate, and upload the device graph.
    create_graph(&g2);
    cudaGraphInstantiate(&gExec2, g2, cudaGraphInstantiateFlagDeviceLaunch);
    cudaGraphUpload(gExec2, stream);

    // Create and instantiate the launching graph.
    cudaStreamBeginCapture(stream, cudaStreamCaptureModeGlobal);
    launchTailGraph<<<1, 1, 0, stream>>>(gExec2);
    cudaStreamEndCapture(stream, &g1);
    cudaGraphInstantiate(&gExec1, g1);

    // Launch the host graph, which will in turn launch the device graph.
    cudaGraphLaunch(gExec1, stream);
}
```

## Constraints

A graph can have up to 255 pending tail launches [CUDA_C_Programming_Guide:L2998-L3045].

## See Also

- [cudaGraphLaunch](concept/cuda-graph-launch)
- [Device Graphs](concept/device-graphs)
