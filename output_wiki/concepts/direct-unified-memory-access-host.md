# Direct Unified Memory Access from Host

Describes cudaDevAttrDirectManagedMemAccessFromHost, which enables hardware-coherent direct reads/stores/atomics from host to GPU-resident memory without page faults. Notes the requirement for cudaMemAdviseSetAccessedBy with cudaMemLocationTypeHost.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21676-L21680

Citation: [CUDA_C_Programming_Guide:L21676-L21680]

````text

Some devices have hardware support for coherent reads, stores and atomic accesses from the host on GPU-resident unified memory. These devices have the attribute cudaDevAttrDirectManaged-MemAccessFromHost set to 1. Note that all hardware coherent systems have this attribute set for NVLink-connected devices. On these systems, the host has direct access to GPU-resident memory without page faults and data migration (see Data Usage Hints for more details on memory usage hints). Note that with CUDA Managed Memory, the cudaMemAdviseSetAccessedBy hint with location type cudaMemLocationTypeHost is necessary to enable this direct access without page faults.

Consider an example code below:
````
