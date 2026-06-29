# Device Graph Launch Overview

Device graph launch provides a mechanism to perform dynamic control flow directly from the device, avoiding the latency of offloading decision-making to the host. This capability allows for workflows that require data-dependent decisions at runtime, such as simple loops or complex device-side work schedulers, to be executed without round-trips between the device and host.

## Terminology

CUDA distinguishes between two types of graphs based on their launch capabilities:

*   **Device graphs**: Graphs that can be launched from both the host and the device.
*   **Host graphs**: Graphs that can only be launched from the host.

## Prerequisites

Device graph launch functionality is only available on systems that support **unified addressing** [CUDA_C_Programming_Guide:L2854-L2863].

## Launch Constraints

When launching device graphs, specific constraints apply to ensure deterministic behavior:

1.  **Concurrent Device Launches**: Launching a device graph from the device while a previous launch of that same graph is still running will result in an error, returning `cudaErrorInvalidValue`. Therefore, a device graph cannot be launched twice from the device simultaneously [CUDA_C_Programming_Guide:L2854-L2863].
2.  **Mixed Host/Device Launches**: Launching a device graph from both the host and the device at the same time results in **undefined behavior** [CUDA_C_Programming_Guide:L2854-L2863].

## Use Cases

Device graph launch is designed for scenarios where:

*   Data-dependent decisions must be made during runtime.
*   Different operations need to be executed based on those decisions.
*   Users prefer to perform control flow logic on the device rather than offloading it to the host [CUDA_C_Programming_Guide:L2854-L2863].
