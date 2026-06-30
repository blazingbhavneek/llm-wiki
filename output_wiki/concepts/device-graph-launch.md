# Device Graph Launch Overview

Covers the concept of device graphs, which allow dynamic control flow and decision-making directly on the GPU without host round-trips. Requires unified addressing. Distinguishes between device graphs (launchable from host/device) and host graphs (host-only). Notes concurrency restrictions: device graphs cannot be launched twice from the device simultaneously, and simultaneous host/device launches cause undefined behavior.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2854-L2863

Citation: [CUDA_C_Programming_Guide:L2854-L2863]

````text
## 6.2.8.7.7 Device Graph Launch

There are many workflows which need to make data-dependent decisions during runtime and execute diferent operations depending on those decisions. Rather than ofloading this decision-making process to the host, which may require a round-trip from the device, users may prefer to perform it on the device. To that end, CUDA provides a mechanism to launch graphs from the device.

Device graph launch provides a convenient way to perform dynamic control flow from the device, be it something as simple as a loop or as complex as a device-side work scheduler. This functionality is only available on systems which support unified addressing.

Graphs which can be launched from the device will henceforth be referred to as device graphs, and graphs which cannot be launched from the device will be referred to as host graphs.

Device graphs can be launched from both the host and device, whereas host graphs can only be launched from the host. Unlike host launches, launching a device graph from the device while a previous launch of the graph is running will result in an error, returning cudaErrorInvalidValue; therefore, a device graph cannot be launched twice from the device at the same time. Launching a device graph from the host and device simultaneously will result in undefined behavior.
````
