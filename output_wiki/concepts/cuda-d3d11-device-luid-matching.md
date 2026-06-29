# CUDA Direct3D 11 Device LUID Matching

When importing memory and synchronization objects exported by Direct3D 11, they must be imported and mapped on the same device as they were created on. The CUDA device that corresponds to the Direct3D 11 device on which the objects were created can be determined by comparing the LUID of a CUDA device with that of the Direct3D 11 device [CUDA_C_Programming_Guide:L5341-L5341].

## Implementation

The following C++ function demonstrates how to identify the corresponding CUDA device for a given Direct3D 11 device by querying the DXGI adapter and comparing Local Unique Identifiers (LUIDs) [CUDA_C_Programming_Guide:L5343-L5379].

```cpp
int getCudaDeviceForD3D11Device(ID3D11Device *d3d11Device) {
    IDXGIDevice *dxgiDevice;
    d3d11Device->QueryInterface(__uuidof(IDXGIDevice), (void **)&dxgiDevice);

    IDXGIAdapter *dxgiAdapter;
    dxgiDevice->GetAdapter(&dxgiAdapter);

    DXGI_ADAPTER_DESC dxgiAdapterDesc;
    dxgiAdapter->GetDesc(&dxgiAdapterDesc);

    LUID d3d11Luid = dxgiAdapterDesc.AdapterLuid;

    int cudaDeviceCount;
    cudaGetDeviceCount(&cudaDeviceCount);

    for (int cudaDevice = 0; cudaDevice < cudaDeviceCount; cudaDevice++) {
        cudaDeviceProp deviceProp;
        cudaGetDeviceProperties(&deviceProp, cudaDevice);
        char *cudaLuid = deviceProp.luid;

        if (!memcmp(&d3d11Luid.LowPart, cudaLuid, sizeof(d3d11Luid.LowPart)) &&
            !memcmp(&d3d11Luid.HighPart, cudaLuid + sizeof(d3d11Luid.LowPart),
sizeof(d3d11Luid.HighPart))) {
            return cudaDevice;
        }
    }
    return cudaInvalidDeviceId;
}
```

### Steps

1. **Query DXGI Device**: Obtain the `IDXGIDevice` interface from the `ID3D11Device` using `QueryInterface` [CUDA_C_Programming_Guide:L5343-L5345].
2. **Get Adapter**: Retrieve the `IDXGIAdapter` associated with the DXGI device [CUDA_C_Programming_Guide:L5347-L5348].
3. **Get Adapter Description**: Fetch the `DXGI_ADAPTER_DESC` to access the `AdapterLuid` [CUDA_C_Programming_Guide:L5350-L5352].
4. **Iterate CUDA Devices**: Loop through all available CUDA devices using `cudaGetDeviceCount` and `cudaGetDeviceProperties` [CUDA_C_Programming_Guide:L5354-L5357].
5. **Compare LUIDs**: Compare the `LowPart` and `HighPart` of the Direct3D 11 LUID with the CUDA device's LUID (`deviceProp.luid`) using `memcmp` [CUDA_C_Programming_Guide:L5359-L5363].
6. **Return Match**: Return the CUDA device index if a match is found, otherwise return `cudaInvalidDeviceId` [CUDA_C_Programming_Guide:L5365-L5367].
