# IPC Memory Pools

IPC capable memory pools allow easy, efficient, and secure sharing of GPU memory between processes [CUDA_C_Programming_Guide:L15705-L15710]. CUDA’s IPC memory pools provide the same security benefits as CUDA’s virtual memory management APIs [CUDA_C_Programming_Guide:L15705-L15710].

There are two phases to sharing memory between processes with memory pools [CUDA_C_Programming_Guide:L15705-L15710]:

1.  **Share Pool Access**: The processes first need to share access to the pool [CUDA_C_Programming_Guide:L15705-L15710]. This phase establishes and enforces security [CUDA_C_Programming_Guide:L15705-L15710].
2.  **Share Allocations**: The processes then share specific allocations from that pool [CUDA_C_Programming_Guide:L15705-L15710]. This phase coordinates what virtual addresses are used in each process and when mappings need to be valid in the importing process [CUDA_C_Programming_Guide:L15705-L15710].
