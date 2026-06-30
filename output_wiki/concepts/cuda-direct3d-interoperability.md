# Direct3D Interoperability

Covers Direct3D 9Ex, 10, and 11 interoperability. Specifies device creation requirements (HAL, hardware vertex processing, D3D_DRIVER_TYPE_HARDWARE). Lists registered resources (buffers, textures, surfaces) and registration functions (cudaGraphicsD3D9/10/11RegisterResource).

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L4117-L4127

Citation: [CUDA_C_Programming_Guide:L4117-L4127]

````text

## 6.2.15.2 Direct3D Interoperability

Direct3D interoperability is supported for Direct3D 9Ex, Direct3D 10, and Direct3D 11.

A CUDA context may interoperate only with Direct3D devices that fulfill the following criteria: Direct3D 9Ex devices must be created with DeviceType set to D3DDEVTYPE\_HAL and BehaviorFlags with the D3DCREATE\_HARDWARE\_VERTEXPROCESSING flag; Direct3D 10 and Direct3D 11 devices must be created with DriverType set to D3D\_DRIVER\_TYPE\_HARDWARE.

The Direct3D resources that may be mapped into the address space of CUDA are Direct3D bufers, textures, and surfaces. These resources are registered using cudaGraphicsD3D9RegisterResource(), cudaGraphicsD3D10RegisterResource(), and cudaGraphicsD3D11RegisterResource().

The following code sample uses a kernel to dynamically modify a 2D width x height grid of vertices stored in a vertex bufer object.
````
