# CDP1 Texture Memory

In the context of CUDA Dynamic Parallelism version 1 (CDP1), texture memory coherence between parent and child grids follows specific synchronization rules. Unlike global memory, writes to the global memory region over which a texture is mapped are inherently incoherent with respect to texture accesses [CUDA_C_Programming_Guide:L14472-L14480].

## Coherence Rules

Coherence for texture memory is enforced at two specific points:
1. At the invocation of a child grid.
2. When a child grid completes [CUDA_C_Programming_Guide:L14472-L14480].

This enforcement implies the following behaviors:
*   **Parent to Child:** Writes to memory made by the parent prior to launching a child kernel are reflected in the texture memory accesses of the child [CUDA_C_Programming_Guide:L14472-L14480].
*   **Child to Parent:** Writes to memory by a child kernel are reflected in the texture memory accesses by the parent, but only after the parent synchronizes on the child’s completion [CUDA_C_Programming_Guide:L14472-L14480].

## Warnings and Deprecation

Concurrent accesses by parent and child kernels to the same memory regions may result in inconsistent data [CUDA_C_Programming_Guide:L14472-L14480].

Furthermore, explicit synchronization with child kernels from a parent block (e.g., using `cudaDeviceSynchronize()` in device code) is deprecated in CUDA 11.6, removed for compute capability 9.0+ compilation, and is slated for full removal in a future CUDA release [CUDA_C_Programming_Guide:L14472-L14480].

## See Also

For the CDP2 version of these rules, refer to the Texture Memory section in the CDP2 documentation [CUDA_C_Programming_Guide:L14472-L14480].
