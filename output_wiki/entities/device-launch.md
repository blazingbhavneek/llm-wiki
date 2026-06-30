# Device Launch Execution

Covers launching device graphs from host or device using `cudaGraphLaunch()`. Notes that device-side launch is per-thread, requiring users to select a single thread for a given graph to avoid conflicts.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2927-L2932

Citation: [CUDA_C_Programming_Guide:L2927-L2932]

````text
## 6.2.8.7.7.5 Device Launch

Device graphs can be launched from both the host and the device via cudaGraphLaunch(), which has the same signature on the device as on the host. Device graphs are launched via the same handle on the host and the device. Device graphs must be launched from another graph when launched from the device.

Device-side graph launch is per-thread and multiple launches may occur from diferent threads at the same time, so the user will need to select a single thread from which to launch a given graph.
````
