# Multi-Device Systems

A host system can have multiple devices [CUDA_C_Programming_Guide:L3456-L3469]. Developers can enumerate these devices, query their properties, and determine the total number of CUDA-enabled devices available on the system [CUDA_C_Programming_Guide:L3456-L3469].

## Device Enumeration

To enumerate devices, the application queries the device count and then iterates through each device index to retrieve its properties [CUDA_C_Programming_Guide:L3456-L3469]. The following code sample demonstrates this process:

```c
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

This approach allows the host application to identify specific devices by their compute capability and other properties [CUDA_C_Programming_Guide:L3456-L3469].
