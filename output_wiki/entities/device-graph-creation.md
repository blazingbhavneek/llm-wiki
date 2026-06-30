# Device Graph Creation

Covers the explicit instantiation requirement for device graphs using the `cudaGraphInstantiateFlagDeviceLaunch` flag. Structure is fixed at instantiation, and instantiation must occur on the host.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2864-L2867

Citation: [CUDA_C_Programming_Guide:L2864-L2867]

````text
## 6.2.8.7.7.1 Device Graph Creation

In order for a graph to be launched from the device, it must be instantiated explicitly for device launch. This is achieved by passing the cudaGraphInstantiateFlagDeviceLaunch flag to the cudaGraphInstantiate() call. As is the case for host graphs, device graph structure is fixed at time of instantiation and cannot be updated without re-instantiation, and instantiation can only be performed on the host. In order for a graph to be able to be instantiated for device launch, it must adhere to various requirements.
````
