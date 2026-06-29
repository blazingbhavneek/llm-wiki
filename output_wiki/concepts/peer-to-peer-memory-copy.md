# Peer-to-Peer Memory Copy

Peer-to-Peer (P2P) memory copy enables memory transfers directly between the memories of two different devices, bypassing the need to stage data through the host CPU memory when peer access is enabled.

## Implementation Methods

The method used for P2P copying depends on whether a Unified Virtual Address Space (UVA) is configured:

*   **Unified Virtual Address Space (UVA):** If a unified address space is used for both devices, standard memory copy functions (such as `cudaMemcpy`) can be used to copy between devices [CUDA_C_Programming_Guide:L3565-L3597].
*   **Non-UVA Environments:** If UVA is not used, specific P2P functions must be employed:
    *   `cudaMemcpyPeer()`
    *   `cudaMemcpyPeerAsync()`
    *   `cudaMemcpy3DPeer()`
    *   `cudaMemcpy3DPeerAsync()` [CUDA_C_Programming_Guide:L3565-L3597]

## Synchronization Guarantees

P2P copies have strict synchronization behaviors, particularly when using the implicit NULL stream:

*   **Blocking Previous Commands:** A copy between memories of two different devices does not start until all commands previously issued to either device have completed [CUDA_C_Programming_Guide:L3565-L3597].
*   **Blocking Subsequent Commands:** The copy runs to completion before any commands issued after the copy to either device can start [CUDA_C_Programming_Guide:L3565-L3597].

For asynchronous copies (using `*Async` functions or non-NULL streams), the copy may overlap with other copies or kernels in different streams, consistent with normal stream behavior [CUDA_C_Programming_Guide:L3565-L3597].

## Performance Optimization

To achieve faster P2P memory copies, peer-to-peer access must be explicitly enabled between the two devices using `cudaDeviceEnablePeerAccess()` [CUDA_C_Programming_Guide:L3565-L3597].

*   **Without Peer Access:** Copies may need to be staged through the host memory, which incurs additional latency and bandwidth overhead [CUDA_C_Programming_Guide:L3565-L3597].
*   **With Peer Access:** The copy occurs directly between device memories, eliminating the staging step and improving performance [CUDA_C_Programming_Guide:L3565-L3597].

## Example Usage

The following code snippet illustrates a P2P copy using `cudaMemcpyPeer` between two devices:

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

In this example, `cudaMemcpyPeer` copies `size` bytes from device 0 (`p0`) to device 1 (`p1`) [CUDA_C_Programming_Guide:L3565-L3597].
