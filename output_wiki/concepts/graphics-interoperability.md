# Graphics Interoperability

Graphics interoperability enables the mapping of resources from OpenGL and Direct3D into the address space of CUDA. This capability facilitates data exchange, allowing CUDA to read data written by OpenGL or Direct3D, or to write data for consumption by those graphics APIs [CUDA_C_Programming_Guide:L3991-L3994].

## Registration

Before a resource can be mapped, it must be registered with CUDA. This process is potentially high-overhead and is typically performed only once per resource [CUDA_C_Programming_Guide:L3995-L3998].

*   **Resource Type**: Registration functions return a pointer to a CUDA graphics resource of type `struct cudaGraphicsResource` [CUDA_C_Programming_Guide:L3998-L3999].
*   **Context Requirement**: Each CUDA context that intends to use the resource must register it separately [CUDA_C_Programming_Guide:L3999-L4000].
*   **Unregistration**: A registered resource is unregistered using `cudaGraphicsUnregisterResource()` [CUDA_C_Programming_Guide:L3998-L3999].

## Mapping and Unmapping

Once registered, a resource can be mapped and unmapped multiple times as needed using `cudaGraphicsMapResources()` and `cudaGraphicsUnmapResources()` [CUDA_C_Programming_Guide:L4000-L4001].

### Usage Hints

The function `cudaGraphicsResourceSetMapFlags()` can be called to specify usage hints, such as write-only or read-only access. These hints allow the CUDA driver to optimize resource management [CUDA_C_Programming_Guide:L4001-L4002].

## Accessing Mapped Resources

Mapped resources are accessed by kernels using the device memory address or array returned by specific query functions:

*   **Buffers**: Use `cudaGraphicsResourceGetMappedPointer()` to obtain the device pointer [CUDA_C_Programming_Guide:L4002-L4003].
*   **CUDA Arrays**: Use `cudaGraphicsSubResourceGetMappedArray()` to obtain the mapped array [CUDA_C_Programming_Guide:L4003-L4004].

## Constraints and Warnings

Accessing a resource through OpenGL, Direct3D, or another CUDA context while it is mapped produces undefined results [CUDA_C_Programming_Guide:L4004-L4005]. Specific details and code samples for each graphics API are provided in the OpenGL Interoperability and Direct3D Interoperability sections, with additional specifics for SLI mode available in the SLI Interoperability section [CUDA_C_Programming_Guide:L4005-L4007].
