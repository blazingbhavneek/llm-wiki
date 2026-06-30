# CUDA Stream-Ordered Memory Addendums

Covers specific behaviors and limitations for async memcpy, pointer attributes, graph memset nodes, and CPU virtual memory limits when using stream-ordered allocators.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L15863-L15883

Citation: [CUDA_C_Programming_Guide:L15863-L15883]

````text
## 15.13. Addendums

## 15.13.1. cudaMemcpyAsync Current Context/DeviceSensitivity

In the current CUDA driver, any async memcpy involving memory from cudaMallocAsync should be done using the specified stream’s context as the calling thread’s current context. This is not necessary for cudaMemcpyPeerAsync, as the device primary contexts specified in the API are referenced instead of the current context.

## 15.13.2. cuPointerGetAttribute Query

Invoking cuPointerGetAttribute on an allocation after invoking cudaFreeAsync on it results in undefined behavior. Specifically, it does not matter if an allocation is still accessible from a given stream: the behavior is still undefined.

## 15.13.3. cuGraphAddMemsetNode

cuGraphAddMemsetNode does not work with memory allocated via the stream ordered allocator. However, memsets of the allocations can be stream captured.

## 15.13.4. Pointer Attributes

The cuPointerGetAttributes query works on stream ordered allocations. Since stream ordered allocations are not context associated, querying CU\_POINTER\_ATTRIBUTE\_CONTEXT will succeed but return NULL in \*data. The attribute CU\_POINTER\_ATTRIBUTE\_DEVICE\_ORDINAL can be used to determine the location of the allocation: this can be useful when selecting a context for making p2h2p copies using cudaMemcpyPeerAsync. The attribute CU\_POINTER\_ATTRIBUTE\_MEMPOOL\_HANDLE was added in CUDA 11.3 and can be useful for debugging and for confirming which pool an allocation comes from before doing IPC.

## 15.13.5. CPU Virtual Memory

When using CUDA stream-ordered memory allocator APIs, avoid setting VRAM limitations with “ulimit -v” as this is not supported.
````
