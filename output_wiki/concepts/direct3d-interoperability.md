# Direct3D Interoperability

Direct3D interoperability is supported for Direct3D 9Ex, Direct3D 10, and Direct3D 11 [CUDA_C_Programming_Guide:L4117-L4128].

## Device Criteria

A CUDA context may interoperate only with Direct3D devices that fulfill specific creation criteria [CUDA_C_Programming_Guide:L4117-L4128]:

*   **Direct3D 9Ex**: Devices must be created with `DeviceType` set to `D3DDEVTYPE_HAL` and `BehaviorFlags` with the `D3DCREATE_HARDWARE_VERTEXPROCESSING` flag [CUDA_C_Programming_Guide:L4117-L4128].
*   **Direct3D 10 and 11**: Devices must be created with `DriverType` set to `D3D_DRIVER_TYPE_HARDWARE` [CUDA_C_Programming_Guide:L4117-L4128].

## Resource Registration

The Direct3D resources that may be mapped into the address space of CUDA are Direct3D buffers, textures, and surfaces [CUDA_C_Programming_Guide:L4117-L4128]. These resources are registered using the following functions:

*   `cudaGraphicsD3D9RegisterResource()`
*   `cudaGraphicsD3D10RegisterResource()`
*   `cudaGraphicsD3D11RegisterResource()` [CUDA_C_Programming_Guide:L4117-L4128]

## Version-Specific Details

Further details for specific Direct3D versions are covered in the following sections:

*   [Direct3D 9 Version](concept/direct3d-interoperability-d3d9)

## Example Usage

The following code sample uses a kernel to dynamically modify a 2D width x height grid of vertices stored in a vertex buffer object [CUDA_C_Programming_Guide:L4117-L4128].
