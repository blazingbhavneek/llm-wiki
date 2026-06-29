# Stream Ordered Memory Allocator Query

To determine if a device supports the stream ordered memory allocator, applications must query specific device attributes using `cudaDeviceGetAttribute()`.

## Querying Allocator Support

Support for the stream ordered memory allocator is indicated by the `cudaDevAttrMemoryPoolsSupported` device attribute. If this attribute returns a non-zero value, the device supports the allocator [CUDA_C_Programming_Guide:L15399-L15428].

## Querying IPC Support

Starting with CUDA 11.3, support for Inter-Process Communication (IPC) with memory pools can be queried using the `cudaDevAttrMemoryPoolSupportedHandleTypes` device attribute [CUDA_C_Programming_Guide:L15399-L15428]. This attribute returns a bitmask of supported handle types, such as `cudaMemHandleTypePosixFileDescriptor` [CUDA_C_Programming_Guide:L15399-L15428].

## Driver Version Checks

It is critical to check the driver version before querying these attributes to avoid errors on older drivers that do not recognize the attribute enums [CUDA_C_Programming_Guide:L15399-L15428].

- **cudaDevAttrMemoryPoolsSupported**: Available from driver version 11.2 (11020) onwards [CUDA_C_Programming_Guide:L15399-L15428].
- **cudaDevAttrMemoryPoolSupportedHandleTypes**: Available from driver version 11.3 (11030) onwards [CUDA_C_Programming_Guide:L15399-L15428].

If an attribute is queried on a driver version that does not support it, the call will return `cudaErrorInvalidValue` [CUDA_C_Programming_Guide:L15399-L15428]. To avoid this error, applications should verify the driver version using `cudaDriverGetVersion()` before calling `cudaDeviceGetAttribute()` [CUDA_C_Programming_Guide:L15399-L15428]. Alternatively, `cudaGetLastError()` can be used to clear the error if the query is performed without a version check [CUDA_C_Programming_Guide:L15399-L15428].

### Example Implementation

The following code snippet demonstrates the correct procedure for querying support:

```txt
int driverVersion = 0;
int deviceSupportsMemoryPools = 0;
int poolSupportedHandleTypes = 0;

// Get driver version
cudaDriverGetVersion(&driverVersion);

// Check for Stream Ordered Memory Allocator support (CUDA 11.2+)
if (driverVersion >= 11020) {
    cudaDeviceGetAttribute(&deviceSupportsMemoryPools,
                             cudaDevAttrMemoryPoolsSupported, device);
}

if (deviceSupportsMemoryPools != 0) {
    // `device` supports the Stream Ordered Memory Allocator
}

// Check for IPC support (CUDA 11.3+)
if (driverVersion >= 11030) {
    cudaDeviceGetAttribute(&poolSupportedHandleTypes,
                             cudaDevAttrMemoryPoolSupportedHandleTypes, device);
}

if (poolSupportedHandleTypes & cudaMemHandleTypePosixFileDescriptor) {
    // Pools on the specified device can be created with posix file descriptor-based IPC
}
```

[CUDA_C_Programming_Guide:L15399-L15428]
