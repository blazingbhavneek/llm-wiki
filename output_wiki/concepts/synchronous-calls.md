# Synchronous Calls

Synchronous functions block the host thread until the device completes the requested task. Host thread behavior (yield, block, or spin) can be configured using cudaSetDeviceFlags() before any CUDA calls.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3449-L3453

Citation: [CUDA_C_Programming_Guide:L3449-L3453]

````text
## 6.2.8.9 Synchronous Calls

When a synchronous function is called, control is not returned to the host thread before the device has completed the requested task. Whether the host thread will then yield, block, or spin can be specified by calling cudaSetDeviceFlags()with some specific flags (see reference manual for details) before any other CUDA call is performed by the host thread.

## 6.2.9. Multi-Device System
````
