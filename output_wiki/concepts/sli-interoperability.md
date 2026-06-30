# SLI Interoperability

Explains special considerations for CUDA interoperability in SLI configurations, including memory allocation impacts across GPUs, the recommendation to create one CUDA context per GPU, and using cudaD3D[9|10|11]GetDevices() or cudaGLGetDevices() to map resources to the correct device per frame.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L4507-L4518

Citation: [CUDA_C_Programming_Guide:L4507-L4518]

````text

## 6.2.15.3 SLI Interoperability

In a system with multiple GPUs, all CUDA-enabled GPUs are accessible via the CUDA driver and runtime as separate devices. There are however special considerations as described below when the system is in SLI mode.

First, an allocation in one CUDA device on one GPU will consume memory on other GPUs that are part of the SLI configuration of the Direct3D or OpenGL device. Because of this, allocations may fail earlier than otherwise expected.

Second, applications should create multiple CUDA contexts, one for each GPU in the SLI configuration. While this is not a strict requirement, it avoids unnecessary data transfers between devices. The application can use the cudaD3D[9|10|11]GetDevices() for Direct3D and cudaGLGetDevices() for OpenGL set of calls to identify the CUDA device handle(s) for the device(s) that are performing the rendering in the current and next frame. Given this information the application will typically choose the appropriate device and map Direct3D or OpenGL resources to the CUDA device returned by cudaD3D[9|10|11]GetDevices() or cudaGLGetDevices() when the deviceList parameter is set to cudaD3D[9|10|11]DeviceListCurrentFrame or cudaGLDeviceListCurrentFrame.

Please note that resource returned from cudaGraphicsD9D[9|10|11]RegisterResource and cudaGraphicsGLRegister[Buffer|Image] must be only used on device the registration happened. Therefore on SLI configurations when data for diferent frames is computed on diferent CUDA devices it is necessary to register the resources for each separately.

See Direct3D Interoperability and OpenGL Interoperability for details on how the CUDA runtime interoperate with Direct3D and OpenGL, respectively.
````
