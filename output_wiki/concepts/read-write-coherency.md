# Read/Write Coherency

Texture and surface memory are cached, and within the same kernel call, the cache is not kept coherent with respect to global memory writes and surface memory writes [CUDA_C_Programming_Guide:L3987-L3990].

Consequently, any texture fetch or surface read to an address that has been written to via a global write or a surface write in the same kernel call returns undefined data [CUDA_C_Programming_Guide:L3987-L3990].

A thread can safely read a texture or surface memory location only if that location has been updated by a previous kernel call or memory copy, but not if it has been previously updated by the same thread or another thread from the same kernel call [CUDA_C_Programming_Guide:L3987-L3990].
