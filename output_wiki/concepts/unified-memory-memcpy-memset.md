# Memcpy()/Memset() Behavior With Unified Memory

Explains how cudaMemcpy*() and cudaMemset*() accept unified memory pointers, the role of cudaMemcpyKind as a performance hint, and best practices for performance optimization.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21800-L21815

Citation: [CUDA_C_Programming_Guide:L21800-L21815]

````text
## 24.2.2.5 Memcpy()/Memset() Behavior With Unified Memory

cudaMemcpy\*() and cudaMemset\*() accept any unified memory pointer as arguments.

For cudaMemcpy\*(), the direction specified as cudaMemcpyKind is a performance hint, which can have a higher performance impact if any of the arguments is a unified memory pointer.

Thus, it is recommended to follow the following performance advice:

▶ When the physical location of unified memory is known, use an accurate cudaMemcpyKind hint.

Prefer cudaMemcpyDefault over an inaccurate cudaMemcpyKind hint.

Always use populated (initialized) bufers: avoid using these APIs to initialize memory.

▶ Avoid using cudaMemcpy\*() if both pointers point to System-Allocated Memory: launch a kernel or use a CPU memory copy algorithm such as std::memcpy instead.
````
