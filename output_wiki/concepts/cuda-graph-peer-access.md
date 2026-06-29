# CUDA Graph Peer Access

## Overview

In the context of CUDA Graphs, memory allocations can be configured to allow access from multiple GPUs. When a graph allocation is created with peer access requirements, the CUDA runtime automatically maps these allocations onto the necessary peer GPUs to satisfy the graph's execution dependencies [CUDA_C_Programming_Guide:L16249-L16253].

## Virtual Address Reuse and Mapping

CUDA allows graph allocations that require different peer mappings to reuse the same virtual address. When this reuse occurs, the address range is mapped onto all GPUs that are required by the various allocations sharing that virtual address [CUDA_C_Programming_Guide:L16249-L16253].

## Implicit Peer Access

Because of the virtual address reuse and automatic mapping mechanism, a memory allocation may sometimes allow more peer access than was explicitly requested during its creation. This happens when the runtime maps the allocation to additional GPUs to satisfy the needs of different graph allocations sharing the same address space [CUDA_C_Programming_Guide:L16249-L16253].

### Important Constraint

While the runtime may grant extra peer access implicitly, relying on these extra mappings is an error. Applications must explicitly configure the required peer access for graph allocations and cannot depend on the runtime's implicit mapping behavior to provide access to GPUs that were not explicitly granted peer access [CUDA_C_Programming_Guide:L16249-L16253].

## Related Concepts

- **Peer Access with Graph Node APIs**: Specific APIs exist to manage peer access within the context of graph nodes [CUDA_C_Programming_Guide:L16249-L16253].
