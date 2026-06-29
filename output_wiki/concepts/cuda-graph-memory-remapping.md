# CUDA Graph Memory Remapping

CUDA Graph memory remapping is a mechanism triggered when the execution context of a graph changes in a way that requires distinct physical memory allocations. While CUDA attempts to optimize performance by retaining physical memory mappings between launches, certain operations force a remap to ensure data integrity and avoid corruption.

## Mechanism and Optimization

When multiple graphs are launched into the same stream, CUDA attempts to allocate the same physical memory to them. This is possible because the execution of graphs within the same stream cannot overlap. To avoid the computational cost of remapping, CUDA retains the physical mappings for a graph between launches [CUDA_C_Programming_Guide:L16224-L16236].

## Causes of Remapping

Remapping is necessary when concurrent execution is introduced or when memory pools are modified. The primary causes include:

*   **Stream Changes**: If a graph is launched into a different stream than before, its execution may overlap with other graphs. Since concurrent graphs require distinct memory to avoid data corruption, CUDA must perform remapping [CUDA_C_Programming_Guide:L16224-L16236].
*   **Trim Operations**: A trim operation on the graph memory pool explicitly frees unused memory, which can trigger remapping of subsequent allocations [CUDA_C_Programming_Guide:L16224-L16236].
*   **Conflicting Allocations**: Relaunching a graph while an unfreed allocation from another graph is mapped to the same memory will cause a remap of memory before the relaunch [CUDA_C_Programming_Guide:L16224-L16236].

## Performance Implications

Remapping operations are relatively expensive. This cost arises from two main factors:

1.  **Execution Order Dependency**: Remapping must happen in execution order and only after any previous execution of that graph is complete. This ensures that memory currently in use is not unmapped prematurely [CUDA_C_Programming_Guide:L16224-L16236].
2.  **OS Calls**: The mapping operations involve calls to the operating system, which adds overhead [CUDA_C_Programming_Guide:L16224-L16236].

## Best Practices

To avoid the performance penalty associated with memory remapping, applications should launch graphs containing allocation memory nodes consistently into the same stream. This consistency allows CUDA to retain physical mappings and reuse existing memory allocations [CUDA_C_Programming_Guide:L16224-L16236].
