# CUDA SLI Interoperability

In a system with multiple GPUs, all CUDA-enabled GPUs are accessible via the CUDA driver and runtime as separate devices. However, special considerations apply when the system is configured in SLI mode for interoperability with Direct3D or OpenGL [CUDA_C_Programming_Guide:L4507-L4518].

## Memory Allocation

An allocation performed on one CUDA device within an SLI configuration consumes memory on all other GPUs that are part of the SLI configuration of the Direct3D or OpenGL device [CUDA_C_Programming_Guide:L4507-L4518]. Consequently, memory allocations may fail earlier than they would in a non-SLI configuration due to this distributed memory consumption [CUDA_C_Programming_Guide:L4507-L4518].

## Context and Device Management

Applications should create multiple CUDA contexts, one for each GPU in the SLI configuration [CUDA_C_Programming_Guide:L4507-L4518]. While not strictly required, this approach avoids unnecessary data transfers between devices [CUDA_C_Programming_Guide:L4507-L4518].

To identify the CUDA device handles for the GPUs performing rendering in the current and next frames, applications should use:
*   `cudaD3D[9|10|11]GetDevices()` for Direct3D [CUDA_C_Programming_Guide:L4507-L4518].
*   `cudaGLGetDevices()` for OpenGL [CUDA_C_Programming_Guide:L4507-L4518].

Based on this information, the application typically selects the appropriate device and maps Direct3D or OpenGL resources to the CUDA device returned by these functions, specifically when the `deviceList` parameter is set to `cudaD3D[9|10|11]DeviceListCurrentFrame` or `cudaGLDeviceListCurrentFrame` [CUDA_C_Programming_Guide:L4507-L4518].

## Resource Registration Constraints

Resources returned from `cudaGraphicsD3D[9|10|11]RegisterResource` and `cudaGraphicsGLRegister[Buffer|Image]` must only be used on the device where the registration occurred [CUDA_C_Programming_Guide:L4507-L4518]. Therefore, in SLI configurations where data for different frames is computed on different CUDA devices, it is necessary to register the resources separately for each device [CUDA_C_Programming_Guide:L4507-L4518].

For further details on the specific interoperability mechanisms, see Direct3D Interoperability and OpenGL Interoperability [CUDA_C_Programming_Guide:L4507-L4518].
