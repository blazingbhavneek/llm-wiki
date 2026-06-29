# CUDA Device Management

Device management within the CUDA device runtime is subject to strict constraints to ensure stability and determinism. The primary rule is that **only the device on which a kernel is running is controllable from that kernel** [CUDA_C_Programming_Guide:L13961-L13964].

## API Limitations

Due to these constraints, several standard host-side device management APIs are either unsupported or behave differently when executed on the device:

*   **`cudaSetDevice()`**: This API is **not supported** by the device runtime. A kernel cannot switch the active device context [CUDA_C_Programming_Guide:L13961-L13964].
*   **`cudaGetDevice()`**: This call returns the active device number as seen from the GPU. This value will be the same as the device number seen from the host system [CUDA_C_Programming_Guide:L13961-L13964].
*   **`cudaDeviceGetAttribute()`**: This API is supported and allows querying attributes of **other devices**. It accepts a device ID as a parameter, enabling inspection of non-active devices [CUDA_C_Programming_Guide:L13961-L13964].
*   **`cudaGetDeviceProperties()`**: The catch-all API for retrieving device properties is **not offered** by the device runtime. Instead, properties must be queried individually using specific attribute queries [CUDA_C_Programming_Guide:L13961-L13964].

## Summary of Device Runtime Constraints

| API | Supported on Device? | Notes |
| :--- | :--- | :--- |
| `cudaSetDevice()` | No | Cannot change active device context. |
| `cudaGetDevice()` | Yes | Returns the current active device ID. |
| `cudaDeviceGetAttribute()` | Yes | Can query attributes for any specified device ID. |
| `cudaGetDeviceProperties()` | No | Properties must be queried individually. |

## References

*   CUDA C Programming Guide, Section 13.3.1.5 Device Management [CUDA_C_Programming_Guide:L13961-L13964].
