# Pointer Attributes

The `cuPointerGetAttributes` query operates on stream ordered allocations. Because stream ordered allocations are not context associated, querying `CU_POINTER_ATTRIBUTE_CONTEXT` will succeed but return `NULL` in the output data pointer [CUDA_C_Programming_Guide:L15876-L15879].

The attribute `CU_POINTER_ATTRIBUTE_DEVICE_ORDINAL` can be used to determine the location of the allocation, which is useful when selecting a context for making peer-to-peer (p2p) copies using `cudaMemcpyPeerAsync` [CUDA_C_Programming_Guide:L15876-L15879].

The attribute `CU_POINTER_ATTRIBUTE_MEMPOOL_HANDLE` was added in CUDA 11.3 and can be useful for debugging and for confirming which pool an allocation comes from before doing inter-process communication (IPC) [CUDA_C_Programming_Guide:L15876-L15879].
