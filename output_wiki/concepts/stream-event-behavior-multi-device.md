# Stream and Event Behavior in Multi-Device Systems

In multi-device CUDA applications, streams and events are bound to specific devices. This binding dictates the success or failure of various CUDA runtime operations when interacting with streams or events from a device context that differs from their association.

## Stream Behavior

### Kernel Launches
A kernel launch will fail if it is issued to a stream that is not associated with the current device. For example, if a stream is created on device 0, attempting to launch a kernel into that stream while device 1 is the current device will result in a failure [CUDA_C_Programming_Guide:L3494-L3528].

### Memory Copies
In contrast to kernel launches, a memory copy operation will succeed even if it is issued to a stream that is not associated with the current device [CUDA_C_Programming_Guide:L3494-L3528].

### Default Streams
Each device maintains its own default stream. Commands issued to the default stream of one device may execute out of order or concurrently with respect to commands issued to the default stream of any other device [CUDA_C_Programming_Guide:L3494-L3528].

## Event Behavior

### Recording Events
The `cudaEventRecord()` function will fail if the input event and the input stream are associated with different devices [CUDA_C_Programming_Guide:L3494-L3528].

### Elapsed Time Calculation
The `cudaEventElapsedTime()` function will fail if the two input events are associated with different devices [CUDA_C_Programming_Guide:L3494-L3528].

### Synchronization and Querying
The `cudaEventSynchronize()` and `cudaEventQuery()` functions will succeed even if the input event is associated with a device that is different from the current device [CUDA_C_Programming_Guide:L3494-L3528].

### Stream-Event Synchronization
The `cudaStreamWaitEvent()` function will succeed even if the input stream and input event are associated with different devices. This capability allows `cudaStreamWaitEvent()` to be used to synchronize multiple devices with each other [CUDA_C_Programming_Guide:L3494-L3528].

## Example: Stream Association Failure

The following code illustrates a kernel launch failure due to stream-device mismatch:

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

In this example, `s0` is associated with device 0. When device 1 is set as the current device, launching a kernel into `s0` fails because `s0` is not associated with the current device (device 1) [CUDA_C_Programming_Guide:L3494-L3528].
