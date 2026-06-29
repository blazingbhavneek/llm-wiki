# Device Memory Accesses

An instruction that accesses addressable memory—specifically global, local, shared, constant, or texture memory—might need to be re-issued multiple times depending on the distribution of the memory addresses across the threads within a warp. The impact of this distribution on instruction throughput is specific to each type of memory [CUDA_C_Programming_Guide:L6407-L6418].

## Global Memory

Global memory resides in device memory and is accessed via 32-, 64-, or 128-byte memory transactions. These transactions must be naturally aligned, meaning that only segments of device memory whose first address is a multiple of their size (32, 64, or 128 bytes) can be read or written [CUDA_C_Programming_Guide:L6407-L6418].

When a warp executes an instruction that accesses global memory, the hardware coalesces the memory accesses of the threads within the warp into one or more of these memory transactions. The number of transactions required depends on the size of the word accessed by each thread and the distribution of the memory addresses across the threads [CUDA_C_Programming_Guide:L6407-L6418].

### Throughput and Coalescing

The efficiency of global memory access is determined by how well the accesses are coalesced. In general, the more transactions are necessary, the more unused words are transferred in addition to the words accessed by the threads, which reduces instruction throughput [CUDA_C_Programming_Guide:L6407-L6418]. For example, if a 32-byte memory transaction is generated for each thread’s 4-byte access, the throughput is divided by 8 [CUDA_C_Programming_Guide:L6407-L6418].

As a general rule, the more scattered the addresses are, the more reduced the throughput is [CUDA_C_Programming_Guide:L6407-L6418].

### Optimization Strategies

To maximize global memory throughput, it is important to maximize coalescing by following these practices:

1.  **Access Patterns**: Follow the most optimal access patterns based on the specific Compute Capability (5.x, 6.x, 7.x, 8.x, 9.0, 10.0, and 12.0) [CUDA_C_Programming_Guide:L6419-L6426].
2.  **Data Types**: Use data types that meet the size and alignment requirements [CUDA_C_Programming_Guide:L6419-L6426].
3.  **Padding**: Pad data in some cases, such as when accessing a two-dimensional array, to ensure proper alignment and coalescing [CUDA_C_Programming_Guide:L6419-L6426].

The specific details on how global memory accesses are handled and how many transactions are necessary vary with the compute capability of the device [CUDA_C_Programming_Guide:L6407-L6418].
