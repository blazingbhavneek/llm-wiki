# Device Enumeration

Host systems can contain multiple devices. This section demonstrates how to enumerate CUDA-enabled devices, query their properties, and determine the total device count using cudaGetDeviceCount() and cudaGetDeviceProperties().

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3455-L3470

Citation: [CUDA_C_Programming_Guide:L3455-L3470]

````text
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
````
