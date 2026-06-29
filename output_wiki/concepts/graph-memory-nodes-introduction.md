# Graph Memory Nodes Introduction

> **Warning**: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA. [CUDA_C_Programming_Guide:L15886-L15896]

Graph memory nodes allow graphs to create and own memory allocations. These nodes operate with GPU ordered lifetime semantics, which dictate when memory is allowed to be accessed on the device [CUDA_C_Programming_Guide:L15886-L15896].

## Key Characteristics

### GPU Ordered Lifetime Semantics
The GPU ordered lifetime semantics enable driver-managed memory reuse and match those of the stream ordered allocation APIs `cudaMallocAsync` and `cudaFreeAsync`, which may be captured when creating a graph [CUDA_C_Programming_Guide:L15886-L15896].

### Fixed Virtual Addresses
Graph allocations have fixed addresses over the life of a graph, including repeated instantiations and launches [CUDA_C_Programming_Guide:L15886-L15896]. This stability allows the memory to be directly referenced by other operations within the graph without the need of a graph update, even when CUDA changes the backing physical memory [CUDA_C_Programming_Guide:L15886-L15896].

### Memory Reuse and Aliasing
Within a single graph, allocations whose graph ordered lifetimes do not overlap may use the same underlying physical memory [CUDA_C_Programming_Guide:L15886-L15896].

CUDA may reuse the same physical memory for allocations across multiple graphs, aliasing virtual address mappings according to the GPU ordered lifetime semantics [CUDA_C_Programming_Guide:L15886-L15896]. For example, when different graphs are launched into the same stream, CUDA may virtually alias the same physical memory to satisfy the needs of allocations which have single-graph lifetimes [CUDA_C_Programming_Guide:L15886-L15896].
