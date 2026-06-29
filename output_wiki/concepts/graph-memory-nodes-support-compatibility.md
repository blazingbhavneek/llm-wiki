# Graph Memory Nodes Support and Compatibility

Graph memory nodes require an 11.4 capable CUDA driver and support for the stream ordered allocator on the GPU [CUDA_C_Programming_Guide:L15897-L15920]. Graph memory nodes are only supported on driver versions 11.4 and newer [CUDA_C_Programming_Guide:L15897-L15920].

## Checking for Support

The following snippet shows how to check for support on a given device by checking the driver version and the `cudaDevAttrMemoryPoolsSupported` attribute [CUDA_C_Programming_Guide:L15897-L15920].

```c
int driverVersion = 0;
int deviceSupportsMemoryPools = 0;
int deviceSupportsMemoryNodes = 0;
cudaDriverGetVersion(&driverVersion);
if (driverVersion >= 11020) { // avoid invalid value error in cudaDeviceGetAttribute
    cudaDeviceGetAttribute(&deviceSupportsMemoryPools,
    cudaDevAttrMemoryPoolsSupported, device);
}
deviceSupportsMemoryNodes = (driverVersion >= 11040) && (deviceSupportsMemoryPools != 0);
```

### Implementation Notes

*   **Driver Version Check:** The attribute query is performed inside a driver version check (`driverVersion >= 11020`) to avoid an invalid value return code on 11.0 and 11.1 drivers [CUDA_C_Programming_Guide:L15897-L15920].
*   **Compute Sanitizer:** Be aware that the compute sanitizer emits warnings when it detects CUDA returning error codes; performing a version check before reading the attribute avoids this [CUDA_C_Programming_Guide:L15897-L15920].
*   **Support Condition:** A device supports graph memory nodes if the driver version is 11.4 or higher (`driverVersion >= 11040`) AND the device supports memory pools (`deviceSupportsMemoryPools != 0`) [CUDA_C_Programming_Guide:L15897-L15920].
