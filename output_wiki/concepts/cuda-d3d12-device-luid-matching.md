# Direct3D 12 Device LUID Matching

When performing Direct3D 12 interoperability, memory and synchronization objects exported by Direct3D 12 must be imported and mapped on the same device on which they were created [CUDA_C_Programming_Guide:L4971-L4998]. To achieve this, the CUDA device that corresponds to the specific Direct3D 12 device must be identified by comparing the Local Unique Identifier (LUID) of the CUDA device with that of the Direct3D 12 device [CUDA_C_Programming_Guide:L4971-L4998].

## Prerequisites and Constraints

The Direct3D 12 device used for interoperability must not be created on a linked node adapter. Specifically, the node count returned by `ID3D12Device::GetNodeCount` must be 1 [CUDA_C_Programming_Guide:L4971-L4998].

## Implementation

The following code sample demonstrates how to determine the corresponding CUDA device ID by iterating through available CUDA devices and comparing their LUIDs with the LUID of the Direct3D 12 device [CUDA_C_Programming_Guide:L4971-L4998].

```cpp
int getCudaDeviceForD3D12Device(ID3D12Device *d3d12Device) {
    LUID d3d12Luid = d3d12Device->GetAdapterLuid();

    int cudaDeviceCount;
    cudaGetDeviceCount(&cudaDeviceCount);

    for (int cudaDevice = 0; cudaDevice < cudaDeviceCount; cudaDevice++) {
        cudaDeviceProp deviceProp;
        cudaGetDeviceProperties(&deviceProp, cudaDevice);
        char *cudaLuid = deviceProp.luid;

        if (!memcmp(&d3d12Luid.LowPart, cudaLuid, sizeof(d3d12Luid.LowPart)) &&
            !memcmp(&d3d12Luid.HighPart, cudaLuid + sizeof(d3d12Luid.LowPart),
            sizeof(d3d12Luid.HighPart))) {
            return cudaDevice;
        }
    }
    return cudaInvalidDeviceId;
}
```

The function returns the CUDA device ID if a match is found, or `cudaInvalidDeviceId` if no corresponding CUDA device is found [CUDA_C_Programming_Guide:L4971-L4998].
