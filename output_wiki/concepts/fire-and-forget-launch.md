# Fire and Forget Launch

A fire-and-forget launch is a mechanism in CUDA where a graph is submitted to the GPU immediately and runs independently of the launching graph [CUDA_C_Programming_Guide:L2941-L2976]. In this scenario, the graph that initiates the launch is considered the parent, and the graph being launched is the child [CUDA_C_Programming_Guide:L2941-L2976].

## Execution Model

The fire-and-forget launch enables a parent graph to trigger the execution of a child graph without waiting for its completion or maintaining a strict synchronization dependency in the same way as standard graph launches [CUDA_C_Programming_Guide:L2941-L2976]. The launched graph operates independently once submitted [CUDA_C_Programming_Guide:L2941-L2976].

## Implementation

To perform a fire-and-forget launch, the `cudaGraphLaunch` function is called with the `cudaStreamGraphFireAndForget` flag [CUDA_C_Programming_Guide:L2941-L2976]. This is typically done within a kernel that is part of the launching (parent) graph [CUDA_C_Programming_Guide:L2941-L2976].

Example kernel code:
```cpp
__global__ void launchFireAndForgetGraph(cudaGraphExec_t graph) {
    cudaGraphLaunch(graph, cudaStreamGraphFireAndForget);
}
```

A typical setup involves:
1. Creating and instantiating the device graph to be launched (the child graph) [CUDA_C_Programming_Guide:L2941-L2976].
2. Creating and instantiating the launching graph (the parent graph) which contains the kernel calling `cudaGraphLaunch` [CUDA_C_Programming_Guide:L2941-L2976].
3. Launching the parent graph [CUDA_C_Programming_Guide:L2941-L2976].

## Constraints

A single graph execution can contain up to 120 total fire-and-forget graphs [CUDA_C_Programming_Guide:L2941-L2976]. This counter resets between separate launches of the same parent graph [CUDA_C_Programming_Guide:L2941-L2976].

## References

- CUDA C++ Programming Guide, Section 6.2.8.7.7.7 Fire and Forget Launch [CUDA_C_Programming_Guide:L2941-L2976]
