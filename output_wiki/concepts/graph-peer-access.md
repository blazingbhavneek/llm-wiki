# Graph Peer Access

Configuration of graph allocations for multi-GPU peer access and virtual address reuse across GPUs.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L16249-L16252

Citation: [CUDA_C_Programming_Guide:L16249-L16252]

````text
## 16.7. Peer Access

Graph allocations can be configured for access from multiple GPUs, in which case CUDA will map the allocations onto the peer GPUs as required. CUDA allows graph allocations requiring diferent mappings to reuse the same virtual address. When this occurs, the address range is mapped onto all GPUs required by the diferent allocations. This means an allocation may sometimes allow more peer access than was requested during its creation; however, relying on these extra mappings is still an error.
````
