# Peer-to-Peer Memory Access

Peer-to-Peer (P2P) memory access is a feature that allows a kernel executing on one device to dereference a pointer to the memory of another device. This capability depends on the system properties, specifically the PCIe and/or NVLink topology [CUDA_C_Programming_Guide:L3529-L3534].

## Prerequisites and Configuration

For P2P memory access to function between two devices, the following conditions must be met:

1. **Topology Support**: The devices must be connected in a topology that supports P2P access [CUDA_C_Programming_Guide:L3529-L3534].
2. **API Verification**: The function `cudaDeviceCanAccessPeer()` must return `true` for the two devices in question [CUDA_C_Programming_Guide:L3529-L3534].
3. **Explicit Enablement**: P2P access must be explicitly enabled between the devices by calling `cudaDeviceEnablePeerAccess()` [CUDA_C_Programming_Guide:L3529-L3534].
4. **Architecture**: P2P memory access is only supported in 64-bit applications [CUDA_C_Programming_Guide:L3529-L3534].

## Connection Limits

On systems that do not use NVSwitch technology, each device supports a system-wide maximum of eight peer connections [CUDA_C_Programming_Guide:L3529-L3534].

## Unified Virtual Address Space (UVA)

When using P2P memory access, a Unified Virtual Address Space (UVA) is utilized for both devices. This allows the same pointer to address memory from both devices, simplifying the code structure [CUDA_C_Programming_Guide:L3535-L3556].

### Example Usage

The following code sample illustrates how to allocate memory on one device and access it from a kernel running on another device:

```cpp
cudaSetDevice(0);                      // Set device 0 as current
float* p0;
size_t size = 1024 * sizeof(float);

cudaMalloc(&p0, size);          // Allocate memory on device 0
MyKernel<<<1000, 128>>>(p0);      // Launch kernel on device 0

cudaSetDevice(1);                    // Set device 1 as current
cudaDeviceEnablePeerAccess(0, 0);    // Enable peer-to-peer access
                                     // with device 0

// Launch kernel on device 1
// This kernel launch can access memory on device 0 at address p0
MyKernel<<<1000, 128>>>(p0);
```

In this example, `MyKernel` launched on device 1 successfully dereferences `p0`, which points to memory allocated on device 0 [CUDA_C_Programming_Guide:L3535-L3556].
