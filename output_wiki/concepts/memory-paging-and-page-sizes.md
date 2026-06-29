# Memory Paging and Page Sizes in Unified Memory

This section defines the necessary terms regarding virtual addressing, memory pages, and page sizes to explain why paging matters for performance in Unified Memory systems [CUDA_C_Programming_Guide:L21616-L21639].

## Virtual Addressing and Pages

All currently supported systems for Unified Memory use a virtual address space [CUDA_C_Programming_Guide:L21616-L21639]. This means that memory addresses used by an application represent a virtual location which might be mapped to a physical location where the memory actually resides [CUDA_C_Programming_Guide:L21616-L21639].

Because all systems use a virtual address space, there are two types of memory pages [CUDA_C_Programming_Guide:L21616-L21639]:

*   **Virtual pages**: This represents a fixed-size contiguous chunk of virtual memory per process tracked by the operating system, which can be mapped into physical memory [CUDA_C_Programming_Guide:L21616-L21639]. Note that the virtual page is linked to the mapping: for example, a single virtual address might be mapped into physical memory using different page sizes [CUDA_C_Programming_Guide:L21616-L21639].
*   **Physical pages**: This represents a fixed-size contiguous chunk of memory the processor’s main Memory Management Unit (MMU) supports and into which a virtual page can be mapped [CUDA_C_Programming_Guide:L21616-L21639].

## Page Sizes by Architecture

Currently, all x86_64 CPUs use 4KiB physical pages [CUDA_C_Programming_Guide:L21616-L21639]. Arm CPUs support multiple physical page sizes - 4KiB, 16KiB, 32KiB and 64KiB - depending on the exact CPU [CUDA_C_Programming_Guide:L21616-L21639]. Finally, NVIDIA GPUs support multiple physical page sizes, but prefer 2MiB physical pages or larger [CUDA_C_Programming_Guide:L21616-L21639]. Note that these sizes are subject to change in future hardware [CUDA_C_Programming_Guide:L21616-L21639].

The default page size of virtual pages usually corresponds to the physical page size, but an application may use different page sizes as long as they are supported by the operating system and the hardware [CUDA_C_Programming_Guide:L21616-L21639]. Typically, supported virtual page sizes must be powers of 2 and multiples of the physical page size [CUDA_C_Programming_Guide:L21616-L21639].

## Page Tables and TLBs

The logical entity tracking the mapping of virtual pages into physical pages is referred to as a page table [CUDA_C_Programming_Guide:L21616-L21639]. Each mapping of a given virtual page with a given virtual size to physical pages is called a page table entry (PTE) [CUDA_C_Programming_Guide:L21616-L21639].

All supported processors provide specific caches for the page table to speed up the translation of virtual addresses to physical addresses [CUDA_C_Programming_Guide:L21616-L21639]. These caches are called translation lookaside buffers (TLBs) [CUDA_C_Programming_Guide:L21616-L21639].

## Performance Tuning Considerations

There are two important aspects for performance tuning of applications [CUDA_C_Programming_Guide:L21616-L21639]:

1.  The choice of virtual page size [CUDA_C_Programming_Guide:L21616-L21639].
2.  Whether the system offers a combined page table used by both CPUs and GPUs, or separate page tables for each CPU and GPU individually [CUDA_C_Programming_Guide:L21616-L21639].

### Choosing the Right Page Size

Further details on selecting the optimal page size are covered in the section on choosing the right page size [CUDA_C_Programming_Guide:L21616-L21639].
