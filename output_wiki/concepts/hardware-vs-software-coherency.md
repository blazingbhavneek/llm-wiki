# Hardware vs. Software Coherency in Unified Memory

In the context of unified memory architectures, systems are categorized based on how CPU and GPU page tables are managed and how memory coherency is enforced. These distinctions significantly impact performance, particularly regarding TLB efficiency and contention during concurrent access.

## Definitions

*   **Hardware Coherent Systems**: Systems that provide a logically combined page table for both CPUs and GPUs. An example of such a system is the NVIDIA Grace Hopper [CUDA_C_Programming_Guide:L21654-L21656].
*   **Software Coherent Systems**: Systems where CPUs and GPUs maintain separate, distinct logical page tables [CUDA_C_Programming_Guide:L21656-L21657].

## Hardware Coherent Systems

In hardware coherent systems, the GPU accesses System-Allocated Memory by utilizing the page table entries created by the CPU [CUDA_C_Programming_Guide:L21657-L21661]. This unified view is critical for performance because it avoids the overhead associated with separate translation mechanisms.

### Page Size and TLB Efficiency

A key concern in hardware coherent systems is the page size used for System-Allocated Memory. If the page table entries use default CPU page sizes (such as 4KiB or 64KiB), accessing large virtual memory areas can result in significant Translation Lookaside Buffer (TLB) misses, leading to substantial slowdowns [CUDA_C_Programming_Guide:L21661-L21664]. To mitigate this, it is recommended to configure the system to use huge pages, ensuring that System-Allocated Memory utilizes sufficiently large page sizes [CUDA_C_Programming_Guide:L21664-L21666].

## Software Coherent Systems

In software coherent systems, where CPUs and GPUs have their own logical page tables, coherency is typically enforced through page faults. When a processor attempts to access a memory address mapped into the physical memory of a different processor, a page fault is triggered [CUDA_C_Programming_Guide:L21667-L21670].

### Page Fault Mechanism

A page fault in this context involves three main steps to guarantee coherency:

1.  **Invalidation**: The system must ensure that the currently owning processor (where the physical page resides) can no longer access the page. This is achieved by deleting the page table entry or updating it [CUDA_C_Programming_Guide:L21670-L21672].
2.  **Validation**: The system must ensure that the processor requesting access can access the page. This involves creating a new page table entry or updating an existing one to make it valid and active [CUDA_C_Programming_Guide:L21672-L21674].
3.  **Migration**: The physical page backing the virtual page must be moved or migrated to the processor requesting access. This operation is expensive, and the amount of work is proportional to the page size [CUDA_C_Programming_Guide:L21674-L21676].

## Performance Comparison

Hardware coherent systems provide significant performance benefits over software coherent systems, particularly in scenarios involving frequent concurrent accesses to the same memory page by both CPU and GPU threads [CUDA_C_Programming_Guide:L21677-L21679].

### Key Advantages

*   **Reduced Page Faults**: Hardware coherent systems do not need to use page faults to emulate coherency or migrate memory, eliminating the overhead associated with the migration process [CUDA_C_Programming_Guide:L21679-L21681].
*   **Lower Contention**: These systems operate at cache-line granularity rather than page-size granularity [CUDA_C_Programming_Guide:L21681-L21683].
    *   When multiple processors contend within a single cache line, only that specific cache line is exchanged, which is much smaller than the smallest page size [CUDA_C_Programming_Guide:L21683-L21685].
    *   If different processors access different cache lines within the same page, there is no contention [CUDA_C_Programming_Guide:L21685-L21687].

### Impact on Specific Scenarios

The differences in coherency mechanisms directly impact the performance of the following scenarios:

*   Atomic updates to the same address performed concurrently by both CPUs and GPUs [CUDA_C_Programming_Guide:L21687-L21689].
*   Signaling between a GPU thread and a CPU thread, or vice versa [CUDA_C_Programming_Guide:L21689-L21691].

## See Also

*   [Direct Unified Memory Access from host](concept/hardware-vs-software-coherency#direct-unified-memory-access-from-host)
*   Configuring huge pages for System-Allocated Memory
