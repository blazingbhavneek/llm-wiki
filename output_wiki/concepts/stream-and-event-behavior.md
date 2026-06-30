# Stream and Event Behavior

Details the behavior of streams and events across different devices. Kernel launches fail if issued to a stream not associated with the current device, while memory copies may succeed. Events and streams on different devices have specific synchronization and error-checking rules. Default streams on different devices may execute concurrently.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3496-L3528

Citation: [CUDA_C_Programming_Guide:L3496-L3528]

````text
## 6.2.9.3 Stream and Event Behavior

A kernel launch will fail if it is issued to a stream that is not associated to the current device as illustrated in the following code sample.

```cpp
cudaSetDevice(0);                      // Set device 0 as current
cudaStream_t s0;
cudaStreamCreate(&s0);            // Create stream s0 on device 0
MyKernel<<<100, 64, 0, s0>>>();
// Launch kernel on device 0 in s0
cudaSetDevice(1);                    // Set device 1 as current
cudaStream_t s1;
cudaStreamCreate(&s1);           // Create stream s1 on device 1
MyKernel<<<100, 64, 0, s1>>>();
// Launch kernel on device 1 in s1

// This kernel launch will fail:
MyKernel<<<100, 64, 0, s0>>>();
// Launch kernel on device 1 in s0
```

A memory copy will succeed even if it is issued to a stream that is not associated to the current device.

cudaEventRecord() will fail if the input event and input stream are associated to diferent devices.

cudaEventElapsedTime() will fail if the two input events are associated to diferent devices.

cudaEventSynchronize() and cudaEventQuery() will succeed even if the input event is associated to a device that is diferent from the current device.

cudaStreamWaitEvent() will succeed even if the input stream and input event are associated to diferent devices. cudaStreamWaitEvent() can therefore be used to synchronize multiple devices with each other.

Each device has its own default stream (see Default Stream), so commands issued to the default stream of a device may execute out of order or concurrently with respect to commands issued to the default stream of any other device.
````
