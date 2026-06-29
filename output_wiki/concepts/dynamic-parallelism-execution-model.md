# Dynamic Parallelism Execution Model

The CUDA execution model is fundamentally based on primitives of threads, thread blocks, and grids, with kernel functions defining the program executed by individual threads within a thread block and grid [CUDA_C_Programming_Guide:L13681-L13684]. When a kernel function is invoked, the grid’s properties are described by an execution configuration, which utilizes special syntax in CUDA [CUDA_C_Programming_Guide:L13681-L13684].

Support for dynamic parallelism in CUDA extends the ability to configure, launch, and implicitly synchronize upon new grids to threads that are running on the device [CUDA_C_Programming_Guide:L13681-L13684]. This capability introduces a hierarchical structure to kernel execution.

## Parent and Child Grids

A device thread that configures and launches a new grid belongs to the parent grid, and the grid created by the invocation is referred to as a child grid [CUDA_C_Programming_Guide:L13685-L13691].

The invocation and completion of child grids is properly nested [CUDA_C_Programming_Guide:L13685-L13691]. This means that the parent grid is not considered complete until all child grids created by its threads have completed [CUDA_C_Programming_Guide:L13685-L13691]. The runtime guarantees an implicit synchronization between the parent and child grids [CUDA_C_Programming_Guide:L13685-L13691].

## Scope of CUDA Primitives

On both host and device, the CUDA runtime offers an API for launching kernels and for tracking dependencies between launches via streams and events [CUDA_C_Programming_Guide:L13694-L13700].

On the host system, the state of launches and the CUDA primitives referencing streams and events are shared by all threads within a process; however, processes execute independently and may not share CUDA objects [CUDA_C_Programming_Guide:L13694-L13700].

On the device, launched kernels and CUDA objects are visible to all threads in a grid [CUDA_C_Programming_Guide:L13694-L13700]. This means, for example, that a stream may be created by one thread and used by any other thread in the grid [CUDA_C_Programming_Guide:L13694-L13700].

## Device Management

There is no multi-GPU support from the device runtime; the device runtime is only capable of operating on the device upon which it is currently executing [CUDA_C_Programming_Guide:L13726-L13729]. It is permitted, however, to query properties for any CUDA capable device in the system [CUDA_C_Programming_Guide:L13726-L13729].
