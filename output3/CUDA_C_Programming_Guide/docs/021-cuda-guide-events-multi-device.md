
## 6.2.8.8 Events

The runtime also provides a way to closely monitor the device’s progress, as well as perform accurate timing, by letting the application asynchronously record events at any point in the program, and query when these events are completed. An event has completed when all tasks - or optionally, all commands in a given stream - preceding the event have completed. Events in stream zero are completed after all preceding tasks and commands in all streams are completed.

## 6.2.8.8.1 Creation and Destruction of Events

The following code sample creates two events:

```txt
cudaEvent_t start, stop;
cudaEventCreate(&start);
cudaEventCreate(&stop);
```

They are destroyed this way:

```javascript
cudaEventDestroy(start);
cudaEventDestroy(stop);
```

## 6.2.8.8.2 Elapsed Time

The events created in Creation and Destruction of Events can be used to time the code sample of Creation and Destruction of Streams the following way:

```txt
cudaEventRecord(start, 0);
for (int i = 0; i < 2; ++i) {
    cudaMemcpyAsync(inputDev + i * size, inputHost + i * size,
                    size, cudaMemcpyHostToDevice, stream[i]);
    MyKernel<<<100, 512, 0, stream[i]>>>
        (outputDev + i * size, inputDev + i * size, size);
```

(continues on next page)

```txt
cudaMemcpyAsync(outputHost + i * size, outputDev + i * size,
                    size, cudaMemcpyDeviceToHost, stream[i]);
}
cudaEventRecord(stop, 0);
cudaEventSynchronize(stop);
float elapsedTime;
cudaEventElapsedTime(&elapsedTime, start, stop);
```

## 6.2.8.9 Synchronous Calls

When a synchronous function is called, control is not returned to the host thread before the device has completed the requested task. Whether the host thread will then yield, block, or spin can be specified by calling cudaSetDeviceFlags()with some specific flags (see reference manual for details) before any other CUDA call is performed by the host thread.

## 6.2.9. Multi-Device System

## 6.2.9.1 Device Enumeration

A host system can have multiple devices. The following code sample shows how to enumerate these devices, query their properties, and determine the number of CUDA-enabled devices.

```txt
int deviceCount;
cudaGetDeviceCount(&deviceCount);
int device;
for (device = 0; device < deviceCount; ++device) {
    cudaDeviceProp deviceProp;
    cudaGetDeviceProperties(&deviceProp, device);
    printf("Device %d has compute capability %d.%d.\n",
        device, deviceProp.major, deviceProp.minor);
}
```

## 6.2.9.2 Device Selection

A host thread can set the device it operates on at any time by calling cudaSetDevice(). Device memory allocations and kernel launches are made on the currently set device; streams and events are created in association with the currently set device. If no call to cudaSetDevice() is made, the current device is device 0.

The following code sample illustrates how setting the current device afects memory allocation and kernel execution.

```cpp
size_t size = 1024 * sizeof(float);
cudaSetDevice(0);          // Set device 0 as current
float* p0;
cudaMalloc(&p0, size);      // Allocate memory on device 0
MyKernel<<<1000, 128>>>(p0); // Launch kernel on device 0
cudaSetDevice(1);            // Set device 1 as current
float* p1;
```

(continues on next page)

```cpp
cudaMalloc(&p1, size);      // Allocate memory on device 1
MyKernel<<<1000, 128>>>(p1); // Launch kernel on device 1
```

(continued from previous page)

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

## 6.2.9.4 Peer-to-Peer Memory Access

Depending on the system properties, specifically the PCIe and/or NVLINK topology, devices are able to address each other’s memory (i.e., a kernel executing on one device can dereference a pointer to the memory of the other device). This peer-to-peer memory access feature is supported between two devices if cudaDeviceCanAccessPeer() returns true for these two devices.

Peer-to-peer memory access is only supported in 64-bit applications and must be enabled between two devices by calling cudaDeviceEnablePeerAccess() as illustrated in the following code sample. On non-NVSwitch enabled systems, each device can support a system-wide maximum of eight peer connections.

A unified address space is used for both devices (see Unified Virtual Address Space), so the same pointer can be used to address memory from both devices as shown in the code sample below.

```txt
cudaSetDevice(0);                      // Set device 0 as current
float* p0;
size_t size = 1024 * sizeof(float);
```

(continues on next page)

```txt
cudaMalloc(&p0, size);          // Allocate memory on device 0
MyKernel<<<1000, 128>>>(p0);      // Launch kernel on device 0
cudaSetDevice(1);                    // Set device 1 as current
cudaDeviceEnablePeerAccess(0, 0);    // Enable peer-to-peer access
                                        // with device 0

// Launch kernel on device 1
// This kernel launch can access memory on device 0 at address p0
MyKernel<<<1000, 128>>>(p0);
```

## 6.2.9.4.1 IOMMU on Linux

On Linux only, CUDA and the display driver does not support IOMMU-enabled bare-metal PCIe peer to peer memory copy. However, CUDA and the display driver does support IOMMU via VM pass through. As a consequence, users on Linux, when running on a native bare metal system, should disable the IOMMU. The IOMMU should be enabled and the VFIO driver be used as a PCIe pass through for virtual machines.

On Windows the above limitation does not exist.

See also Allocating DMA Bufers on 64-bit Platforms.

## 6.2.9.5 Peer-to-Peer Memory Copy

Memory copies can be performed between the memories of two diferent devices.

When a unified address space is used for both devices (see Unified Virtual Address Space), this is done using the regular memory copy functions mentioned in Device Memory.

Otherwise, this is done using cudaMemcpyPeer(), cudaMemcpyPeerAsync(), cudaMemcpy3DPeer(), or cudaMemcpy3DPeerAsync() as illustrated in the following code sample.

```cpp
cudaSetDevice(0);                      // Set device 0 as current
float* p0;
size_t size = 1024 * sizeof(float);
cudaMalloc(&p0, size);                 // Allocate memory on device 0
cudaSetDevice(1);                          // Set device 1 as current
float* p1;
cudaMalloc(&p1, size);                 // Allocate memory on device 1
cudaSetDevice(0);                          // Set device 0 as current
MyKernel<<<1000, 128>>>(p0);      // Launch kernel on device 0
cudaSetDevice(1);                          // Set device 1 as current
cudaMemcpyPeer(p1, 1, p0, 0, size); // Copy p0 to p1
MyKernel<<<1000, 128>>>(p1);       // Launch kernel on device 1
```

A copy (in the implicit NULL stream) between the memories of two diferent devices:

does not start until all commands previously issued to either device have completed and

runs to completion before any commands (see Asynchronous Concurrent Execution) issued after the copy to either device can start.

Consistent with the normal behavior of streams, an asynchronous copy between the memories of two devices may overlap with copies or kernels in another stream.

Note that if peer-to-peer access is enabled between two devices via cudaDeviceEnablePeerAccess() as described in Peer-to-Peer Memory Access, peer-to-peer memory copy between these two devices no longer needs to be staged through the host and is therefore faster.
