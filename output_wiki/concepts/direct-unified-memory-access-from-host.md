# Direct Unified Memory Access from Host

Direct Unified Memory Access from Host refers to the capability of certain devices to support coherent reads, stores, and atomic accesses from the host processor directly on GPU-resident unified memory [CUDA_C_Programming_Guide:L21676-L21680].

## Hardware Support and Attributes

Devices that support this feature have the device attribute `cudaDevAttrDirectManagedMemAccessFromHost` set to 1 [CUDA_C_Programming_Guide:L21676-L21680]. This attribute is notably set for all NVLink-connected devices on hardware coherent systems [CUDA_C_Programming_Guide:L21676-L21680].

## Operational Behavior

On systems where this attribute is enabled, the host has direct access to GPU-resident memory without triggering page faults or requiring data migration [CUDA_C_Programming_Guide:L21676-L21680]. This behavior is contingent upon the use of CUDA Managed Memory and the application of specific memory usage hints [CUDA_C_Programming_Guide:L21676-L21680].

## Configuration Requirements

To enable direct access without page faults, the `cudaMemAdviseSetAccessedBy` hint must be used with the location type `cudaMemLocationTypeHost` [CUDA_C_Programming_Guide:L21676-L21680]. This configuration ensures that the host is recognized as an accessor of the managed memory, allowing for coherent access patterns [CUDA_C_Programming_Guide:L21676-L21680].

## See Also

- Data Usage Hints
- CUDA Managed Memory
- `cudaMemAdviseSetAccessedBy`
- `cudaMemLocationTypeHost`
