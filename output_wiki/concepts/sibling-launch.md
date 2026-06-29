# Sibling Launch

Sibling launch is a variation of fire-and-forget launch in which the graph is launched not as a child of the launching graph’s execution environment, but rather as a child of the launching graph’s parent environment [CUDA_C_Programming_Guide:L3079-L3114]. This mode is equivalent to a fire-and-forget launch from the launching graph’s parent environment [CUDA_C_Programming_Guide:L3079-L3114].

## Key Characteristics

*   **Execution Hierarchy**: The launched graph becomes a sibling to the launching graph within the parent execution environment, rather than a child of the launching graph itself [CUDA_C_Programming_Guide:L3079-L3114].
*   **Tail Launch Behavior**: Because sibling launches are not launched into the launching graph’s execution environment, they will not gate tail launches enqueued by the launching graph [CUDA_C_Programming_Guide:L3079-L3114].

## Implementation

Sibling launches are performed using the `cudaStreamGraphFireAndForgetAsSibling` flag within a `cudaGraphLaunch` call inside a kernel. The following example demonstrates creating a device graph, instantiating it, and then launching it from a host graph using the sibling launch mode [CUDA_C_Programming_Guide:L3079-L3114].

```cpp
__global__ void launchSiblingGraph(cudaGraphExec_t graph) {
    cudaGraphLaunch(graph, cudaStreamGraphFireAndForgetAsSibling);
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
    launchSiblingGraph<<<1, 1, 0, stream>>>(gExec2);
    cudaStreamEndCapture(stream, &g1);
    cudaGraphInstantiate(&gExec1, g1);

    // Launch the host graph, which will in turn launch the device graph.
    cudaGraphLaunch(gExec1, stream);
}
```

## See Also

*   Fire-and-forget launch
*   CUDA Graphs

## References

*   CUDA C++ Programming Guide, Section 6.2.8.7.7.11 Sibling Launch [CUDA_C_Programming_Guide:L3079-L3114]
