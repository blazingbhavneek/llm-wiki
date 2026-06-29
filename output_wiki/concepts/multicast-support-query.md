# Multicast Support Query

Before attempting to use Multicast Objects, applications must ensure that the devices they want to use support them. This is achieved by querying the device attributes.

The following code sample demonstrates how to query for Multicast support using the `cuDeviceGetAttribute` function with the `CU_DEVICE_ATTRIBUTE_MULTICAST_SUPPORTED` attribute:

```javascript
int deviceSupportsMultiCast;
CUresult result = cuDeviceGetAttribute(&deviceSupportsMultiCast, CU_DEVICE_ATTRIBUTE_MULTICAST_SUPPORTED, device);
if (deviceSupportsMultiCast != 0) {
    // `device` supports Multicast Objects
}
```

[CUDA_C_Programming_Guide:L15278-L15289]
