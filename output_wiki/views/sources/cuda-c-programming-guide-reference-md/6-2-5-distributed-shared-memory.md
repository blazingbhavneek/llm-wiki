# 6.2.5. Distributed Shared Memory

Part of [Cuda C Programming Guide Reference](README.md). Source lines L1851-L2218.

- [Distributed Shared Memory](../../../concepts/distributed-shared-memory.md) — Distributed Shared Memory (DSM) is a feature introduced in compute capability 9.0 that allows threads in a thread block cluster to access the shared memory of all participating thread blocks within that cluster, providing a partitioned shared memory address space for read, write, and atomic operations.
- [Page-Locked Host Memory](../../../concepts/page-locked-host-memory.md) — Page-locked (pinned) host memory is a type of host memory allocation that enables concurrent data transfers, zero-copy access, and higher bandwidth on certain systems, allocated via CUDA runtime functions like `cudaHostAlloc()` or `cudaHostRegister()`.
- [Memory Synchronization Domains](../../../concepts/memory-synchronization-domains.md) — Memory Synchronization Domains, introduced in Hopper architecture (CUDA 12.0), alleviate memory fence interference by isolating traffic into distinct domains, allowing the GPU to reduce the 'net cast' of waiting operations.
- [Asynchronous Concurrent Execution](../../../concepts/asynchronous-concurrent-execution.md) — CUDA exposes independent tasks such as host and device computation, and various memory transfers, which can operate concurrently depending on the device's compute capability and hardware resources.
- [Streams](../../../concepts/streams.md) — Streams are ordered sequences of commands that enable concurrent execution across multiple streams, managed via creation and destruction APIs with automatic resource cleanup.
