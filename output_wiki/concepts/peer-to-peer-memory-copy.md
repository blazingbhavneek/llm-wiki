# Peer-to-Peer Memory Copy

Memory can be copied directly between devices using cudaMemcpyPeer() or similar functions. Copies in the implicit NULL stream synchronize with all previous commands. Asynchronous copies can overlap with other operations. P2P access via cudaDeviceEnablePeerAccess() avoids staging through host memory, improving performance.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3565-L3597

Citation: [CUDA_C_Programming_Guide:L3565-L3597]

````text
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
````
