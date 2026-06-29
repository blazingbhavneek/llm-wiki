# GPU Memory Oversubscription with Unified Memory

Unified Memory enables applications to oversubscribe the memory of any individual processor. This capability allows software to allocate and share arrays that are larger than the memory capacity of any single processor within the system [CUDA_C_Programming_Guide:L21189-L21192].

This feature facilitates out-of-core processing for datasets that do not fit within the memory of a single GPU, while avoiding significant complexity in the programming model [CUDA_C_Programming_Guide:L21189-L21192].
