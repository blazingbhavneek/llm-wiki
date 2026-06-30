# Direct3D 11 Device LUID Matching

Matches CUDA devices to Direct3D 11 devices by comparing their Local Unique Identifiers (LUIDs).

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L5337-L5379

Citation: [CUDA_C_Programming_Guide:L5337-L5379]

````text
## 6.2.16.4 Direct3D 11 Interoperability

## 6.2.16.4.1 Matching Device LUIDs

When importing memory and synchronization objects exported by Direct3D 11, they must be imported and mapped on the same device as they were created on. The CUDA device that corresponds to the Direct3D 11 device on which the objects were created can be determined by comparing the LUID of a CUDA device with that of the Direct3D 11 device, as shown in the following code sample.

```c
int getCudaDeviceForD3D11Device(ID3D11Device *d3d11Device) {
    IDXGIDevice *dxgiDevice;
    d3d11Device->QueryInterface(__uuidof(IDXGIDevice), (void **)&dxgiDevice);

    IDXGIAdapter *dxgiAdapter;
```

(continues on next page)

(continued from previous page)

```cpp
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
````
