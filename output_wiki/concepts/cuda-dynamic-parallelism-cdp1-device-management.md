# CUDA Dynamic Parallelism (CDP1) Device Management

In CUDA Dynamic Parallelism version 1 (CDP1), device management capabilities are restricted to ensure stability and determinism within the device runtime environment. The primary constraint is that only the device on which a kernel is currently running can be controlled from within that kernel [CUDA_C_Programming_Guide:L14578-L14583].

## Supported APIs

### Device Identification

*   **`cudaGetDevice()`**: This function is supported. It returns the device number of the active device as seen from the GPU, which is identical to the device number seen from the host system [CUDA_C_Programming_Guide:L14578-L14583].
*   **`cudaDeviceGetAttribute()`**: This function is supported and allows querying attributes. Notably, it accepts a device ID as a parameter, enabling the retrieval of information about devices other than the one currently executing the kernel [CUDA_C_Programming_Guide:L14578-L14583].

## Unsupported APIs

### Device Selection

*   **`cudaSetDevice()`**: This function is **not supported** by the device runtime. Because only the device on which the kernel is running is controllable, switching the active device from within a kernel is prohibited [CUDA_C_Programming_Guide:L14578-L14583].

### Device Properties

*   **`cudaGetDeviceProperties()`**: This catch-all API is **not offered** by the device runtime in CDP1 [CUDA_C_Programming_Guide:L14578-L14583]. To obtain device properties, they must be queried individually using specific attribute or property functions [CUDA_C_Programming_Guide:L14578-L14583].

## Note on CDP2

For the CDP2 version of device management, refer to the general Device Management section of the documentation [CUDA_C_Programming_Guide:L14578-L14583].
