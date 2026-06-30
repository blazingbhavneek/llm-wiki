# CUDA Dynamic Parallelism Synchronization

Inter-thread and inter-grid synchronization mechanisms and limitations in the device runtime.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L13954-L13960

Citation: [CUDA_C_Programming_Guide:L13954-L13960]

````text

## 13.3.1.4 Synchronization

It is up to the program to perform suficient inter-thread synchronization, for example via a CUDA Event, if the calling thread is intended to synchronize with child grids invoked from other threads.

As it is not possible to explicitly synchronize child work from a parent thread, there is no way to guarantee that changes occurring in child grids are visible to threads within the parent grid.
````
