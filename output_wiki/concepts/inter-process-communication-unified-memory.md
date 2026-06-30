# Inter-Process Communication with Unified Memory

Explains that CUDA IPC does not support Managed Memory, but System-Allocated Memory on full-support systems is IPC-capable. Lists Linux mechanisms (mmap MAP_SHARED, POSIX IPC, memfd_create) for sharing memory across processes.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21585-L21602

Citation: [CUDA_C_Programming_Guide:L21585-L21602]

````text
## 24.2.1.2 Inter-Process Communication (IPC) with Unified Memory

Note: As of now, using IPC with Unified Memory can have significant performance implications.

Many applications prefer to manage one GPU per process, but still need to use Unified Memory, for example for over-subscription, and access it from multiple GPUs.

CUDA IPC (see Interprocess Communication) does not support Managed Memory: handles to this type of memory may not be shared through any of the mechanisms discussed in this section. On systems with full CUDA Unified Memory support, System-Allocated Memory is Inter-Process Communication (IPC) capable. Once access to System-Allocated Memory has been shared with other processes, the same Programming Model applies, similar to File-backed Unified Memory.

See the following references for more information on various ways of creating IPC-capable System-Allocated Memory under Linux:

▶ mmap with MAP\_SHARED

▶ POSIX IPC APIs

1 Linux memfd\_create

Note that it is not possible to share memory between diferent hosts and their devices using this technique.
````
