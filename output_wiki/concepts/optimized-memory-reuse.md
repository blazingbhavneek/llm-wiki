# Optimized Memory Reuse

CUDA reuses memory via virtual address assignment within graphs and physical memory aliasing between graphs.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L16191-L16222

Citation: [CUDA_C_Programming_Guide:L16191-L16222]

````text
## 16.4. Optimized Memory Reuse

## CUDA reuses memory in two ways:

▶ Virtual and physical memory reuse within a graph is based on virtual address assignment, like in the stream ordered allocator.

▶ Physical memory reuse between graphs is done with virtual aliasing: diferent graphs can map the same physical memory to their unique virtual addresses.

## 16.4.1. Address Reuse within a Graph

CUDA may reuse memory within a graph by assigning the same virtual address ranges to diferent allocations whose lifetimes do not overlap. Since virtual addresses may be reused, pointers to diferent allocations with disjoint lifetimes are not guaranteed to be unique.

The following figure shows adding a new allocation node (2) that can reuse the address freed by a dependent node (1).

![](images/f378e6daa910633134c3a3577d442b2904f6569eefeefb7e80de4dade9eafc07.jpg)  
Figure 33: Adding New Alloc Node 2  
The following figure shows adding a new alloc node (4). The new alloc node is not dependent on the free node (2) so cannot reuse the address from the associated alloc node (2). If the alloc node (2) used the address freed by free node (1), the new alloc node 3 would need a new address.

## 16.4.2. Physical Memory Management and Sharing

CUDA is responsible for mapping physical memory to the virtual address before the allocating node is reached in GPU order. As an optimization for memory footprint and mapping overhead, multiple graphs may use the same physical memory for distinct allocations if they will not run simultaneously; however, physical pages cannot be reused if they are bound to more than one executing graph at the same time, or to a graph allocation which remains unfreed.

CUDA may update physical memory mappings at any time during graph instantiation, launch, or execution. CUDA may also introduce synchronization between future graph launches in order to prevent live graph allocations from referring to the same physical memory. As for any allocate-free-allocate pattern, if a program accesses a pointer outside of an allocation’s lifetime, the erroneous access may silently read or write live data owned by another allocation (even if the virtual address of the allocation is unique). Use of compute sanitizer tools can catch this error.

![](images/b18e924b24285918eded0ea9b9496ba7d0dc0c12395c106c66985d6fcfae9dbf.jpg)  
Figure 34: Adding New Alloc Node 3

The following figure shows graphs sequentially launched in the same stream. In this example, each graph frees all the memory it allocates. Since the graphs in the same stream never run concurrently, CUDA can and should use the same physical memory to satisfy all the allocations.

![](images/52d38ef0e51ba0735c45557628f151494cae08978869c164417c7e98f6f0df28.jpg)  
Figure 35: Sequentially Launched Graphs
````
