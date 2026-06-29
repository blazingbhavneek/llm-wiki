# System-Allocated Memory

On systems with full CUDA Unified Memory support, all memory is unified memory. This category includes memory allocated with standard system allocation APIs, such as `malloc()`, `mmap()`, and the C++ `new` operator, as well as automatic variables on CPU thread stacks, thread locals, and global variables [CUDA_C_Programming_Guide:L20962-L20978].

## First-Touch Policy

System-allocated memory may be populated on first touch, depending on the API and system settings used. The first-touch policy operates as follows:

1.  **Virtual Allocation**: The allocation APIs allocate virtual memory and return immediately [CUDA_C_Programming_Guide:L20962-L20978].
2.  **Physical Population**: Physical memory is populated only when a thread accesses the memory for the first time [CUDA_C_Programming_Guide:L20962-L20978].

The physical memory location is typically chosen "close" to the processor that performs the first access [CUDA_C_Programming_Guide:L20962-L20978]:

*   **GPU First Touch**: If a GPU thread accesses the memory first, physical GPU memory on the GPU where the thread runs is chosen [CUDA_C_Programming_Guide:L20962-L20978].
*   **CPU First Touch**: If a CPU thread accesses the memory first, physical CPU memory in the memory NUMA node of the CPU core that thread runs on is chosen [CUDA_C_Programming_Guide:L20962-L20978].

## CUDA Unified Memory Integration

System-allocated memory supports CUDA Unified Memory Hint and Prefetch APIs. Specifically, `cudaMemAdvise` and `cudaMemPrefetchAsync` may be used on system-allocated memory to manage data placement and usage hints [CUDA_C_Programming_Guide:L20962-L20978].
