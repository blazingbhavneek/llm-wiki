# Read/Write Coherency

Explains that texture and surface memory is cached and not kept coherent with global/surface writes within the same kernel call. Reads return undefined data if written to in the same kernel call, requiring updates from previous kernel calls or memory copies.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3988-L3991

Citation: [CUDA_C_Programming_Guide:L3988-L3991]

````text
## 6.2.14.4 Read/Write Coherency

The texture and surface memory is cached (see Device Memory Accesses) and within the same kernel call, the cache is not kept coherent with respect to global memory writes and surface memory writes, so any texture fetch or surface read to an address that has been written to via a global write or a surface write in the same kernel call returns undefined data. In other words, a thread can safely read some texture or surface memory location only if this memory location has been updated by a previous kernel call or memory copy, but not if it has been previously updated by the same thread or another thread from the same kernel call.
````
