# CUDA Graph Memory Reuse

CUDA provides optimized memory reuse mechanisms to reduce memory footprint and mapping overhead. These mechanisms operate at two levels: virtual address assignment within a single graph and physical memory sharing across multiple graphs.

## Virtual and Physical Memory Reuse

CUDA reuses memory in two distinct ways [CUDA_C_Programming_Guide:L16191-L16223]:

1.  **Within a Graph**: Virtual and physical memory reuse is based on virtual address assignment, similar to the stream ordered allocator. This allows the same virtual address ranges to be assigned to different allocations if their lifetimes do not overlap [CUDA_C_Programming_Guide:L16191-L16223].
2.  **Between Graphs**: Physical memory reuse is achieved through virtual aliasing. Different graphs can map the same physical memory to their unique virtual addresses, provided they do not run concurrently [CUDA_C_Programming_Guide:L16191-L16223].

## Address Reuse within a Graph

CUDA may reuse memory within a graph by assigning the same virtual address ranges to different allocations whose lifetimes do not overlap [CUDA_C_Programming_Guide:L16191-L16223]. Because virtual addresses may be reused, pointers to different allocations with disjoint lifetimes are not guaranteed to be unique [CUDA_C_Programming_Guide:L16191-L16223].

The reuse logic depends on dependencies between allocation and free nodes:

*   **Dependent Reuse**: A new allocation node can reuse the address freed by a dependent free node. For example, if a free node (1) frees an address, a subsequent allocation node (2) that depends on that free can reuse the same virtual address range [CUDA_C_Programming_Guide:L16191-L16223].
*   **Non-Dependent Reuse**: If a new allocation node is not dependent on the free node associated with a previous allocation, it cannot reuse the address from that previous allocation. For instance, if allocation node (2) used the address freed by free node (1), a new allocation node (4) that is not dependent on free node (2) would require a new address [CUDA_C_Programming_Guide:L16191-L16223].

## Physical Memory Management and Sharing

CUDA is responsible for mapping physical memory to the virtual address before the allocating node is reached in GPU order [CUDA_C_Programming_Guide:L16191-L16223].

### Non-Concurrent Graphs

As an optimization for memory footprint and mapping overhead, multiple graphs may use the same physical memory for distinct allocations if they will not run simultaneously [CUDA_C_Programming_Guide:L16191-L16223]. For example, graphs launched sequentially in the same stream never run concurrently; therefore, CUDA can and should use the same physical memory to satisfy all allocations across these graphs [CUDA_C_Programming_Guide:L16191-L16223].

### Constraints and Risks

Physical pages cannot be reused if they are bound to more than one executing graph at the same time, or to a graph allocation which remains unfreed [CUDA_C_Programming_Guide:L16191-L16223].

CUDA may update physical memory mappings at any time during graph instantiation, launch, or execution [CUDA_C_Programming_Guide:L16191-L16223]. To prevent live graph allocations from referring to the same physical memory, CUDA may introduce synchronization between future graph launches [CUDA_C_Programming_Guide:L16191-L16223].

### Safety Warning

As with any allocate-free-allocate pattern, if a program accesses a pointer outside of an allocation’s lifetime, the erroneous access may silently read or write live data owned by another allocation, even if the virtual address of the allocation is unique [CUDA_C_Programming_Guide:L16191-L16223]. Developers should use compute sanitizer tools to catch this type of error [CUDA_C_Programming_Guide:L16191-L16223].

## See Also

*   [Performance Considerations](concept/cuda-graph-performance)
