# Choosing the Right Page Size

When managing Unified Memory, the choice of page size involves a trade-off between memory fragmentation and translation lookaside buffer (TLB) performance. The impact of this choice is more pronounced on GPUs than on CPUs.

## Trade-offs: Small vs. Large Pages

*   **Small Page Sizes**
    *   **Pros:** Lead to less virtual memory fragmentation.
    *   **Cons:** Result in more TLB misses.

*   **Large Page Sizes**
    *   **Pros:** Result in fewer TLB misses.
    *   **Cons:** Lead to more memory fragmentation and higher memory migration costs. Since memory migration typically operates on full pages, larger pages can cause larger latency spikes in applications [CUDA_C_Programming_Guide:L21640-L21646].

## GPU vs. CPU Performance Impact

TLB misses are generally significantly more expensive on the GPU compared to the CPU [CUDA_C_Programming_Guide:L21640-L21646].

*   **GPU Threads:** If a GPU thread frequently accesses random locations in Unified Memory mapped with a small page size, performance may be significantly slower compared to using a large enough page size [CUDA_C_Programming_Guide:L21640-L21646].
*   **CPU Threads:** A similar slowdown can occur on CPUs when randomly accessing large areas of memory mapped with small pages, but the effect is less pronounced [CUDA_C_Programming_Guide:L21640-L21646].

Consequently, applications might choose to trade off the minor slowdown associated with CPU fragmentation for the significant performance gains of reduced TLB misses on the GPU by using larger page sizes [CUDA_C_Programming_Guide:L21640-L21646].

## Tuning Recommendations

Applications should not tune their performance based on the physical page size of a given processor, as physical page sizes are subject to change depending on the hardware [CUDA_C_Programming_Guide:L21640-L21646]. The advice regarding TLB and fragmentation trade-offs applies specifically to virtual page sizes [CUDA_C_Programming_Guide:L21640-L21646].

For more details on the mechanics of page faults associated with these sizes, see the relevant section on page faults.
