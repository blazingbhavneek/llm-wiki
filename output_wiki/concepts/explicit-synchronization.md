# Explicit Synchronization

Methods to explicitly synchronize streams include cudaDeviceSynchronize(), cudaStreamSynchronize(), cudaStreamWaitEvent(), and cudaStreamQuery().

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2231-L2242

Citation: [CUDA_C_Programming_Guide:L2231-L2242]

````text
## 6.2.8.5.3 Explicit Synchronization

There are various ways to explicitly synchronize streams with each other.

cudaDeviceSynchronize() waits until all preceding commands in all streams of all host threads have completed.

cudaStreamSynchronize()takes a stream as a parameter and waits until all preceding commands in the given stream have completed. It can be used to synchronize the host with a specific stream, allowing other streams to continue executing on the device.

cudaStreamWaitEvent()takes a stream and an event as parameters (see Events for a description of events)and makes all the commands added to the given stream after the call to cudaStreamWait-Event()delay their execution until the given event has completed.

cudaStreamQuery()provides applications with a way to know if all preceding commands in a stream have completed.
````
