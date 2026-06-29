# Device Graph Creation

In order for a graph to be launched from the device, it must be instantiated explicitly for device launch. This is achieved by passing the `cudaGraphInstantiateFlagDeviceLaunch` flag to the `cudaGraphInstantiate()` call [CUDA_C_Programming_Guide:L2864-L2867].

As is the case for host graphs, device graph structure is fixed at time of instantiation and cannot be updated without re-instantiation, and instantiation can only be performed on the host [CUDA_C_Programming_Guide:L2864-L2867].

In order for a graph to be able to be instantiated for device launch, it must adhere to various requirements [CUDA_C_Programming_Guide:L2864-L2867].
