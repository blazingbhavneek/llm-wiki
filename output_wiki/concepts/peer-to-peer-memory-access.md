# Peer-to-Peer Memory Access

Devices can directly address each other's memory based on PCIe/NVLINK topology. Enabled via cudaDeviceEnablePeerAccess() and verified with cudaDeviceCanAccessPeer(). Requires 64-bit applications and unified address space. Linux bare-metal systems require IOMMU to be disabled for PCIe P2P, while VM pass-through with VFIO is supported.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3529-L3564

Citation: [CUDA_C_Programming_Guide:L3529-L3564]

````text
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
````
