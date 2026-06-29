# CPU Virtual Memory

When using CUDA stream-ordered memory allocator APIs, avoid setting VRAM limitations with “ulimit -v” as this is not supported [CUDA_C_Programming_Guide:L15880-L15883].
