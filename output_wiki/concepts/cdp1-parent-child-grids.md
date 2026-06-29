# CDP1 Parent and Child Grids

In the Context of Dynamic Parallelism version 1 (CDP1), CUDA defines a hierarchical relationship between grids launched from within device code.

## Parent and Child Grids

A device thread that configures and launches a new grid belongs to the **parent grid**, and the grid created by the invocation is a **child grid** [CUDA_C_Programming_Guide:L14304-L14312].

## Proper Nesting Guarantees

The invocation and completion of child grids is **properly nested**. This means that the parent grid is not considered complete until all child grids created by its threads have completed [CUDA_C_Programming_Guide:L14304-L14312].

The CUDA runtime guarantees an **implicit synchronization** between the parent and child grids. This synchronization occurs even if the invoking threads do not explicitly synchronize on the child grids launched [CUDA_C_Programming_Guide:L14304-L14312].

## Note on CDP2

For the CDP2 version of this feature, see the documentation on Parent and Child Grids in the CDP2 section of the CUDA C Programming Guide [CUDA_C_Programming_Guide:L14304-L14312].
