# 6.2.8.5.2 Default Stream

Part of [Cuda C Programming Guide Reference](README.md). Source lines L2219-L2805.

- [Default Stream](../../../concepts/default-stream.md) — The default stream is the implicit stream (stream 0) used for kernel launches and memory operations that do not specify a stream parameter, with behavior varying based on the `--default-stream` compilation flag.
- [Explicit Synchronization](../../../concepts/explicit-synchronization.md) — Explicit synchronization in CUDA provides mechanisms for host threads and streams to coordinate execution states, including waiting for completion, querying status, and ordering operations via events.
- [Implicit Synchronization](../../../concepts/implicit-synchronization.md) — Implicit synchronization occurs when operations from different streams are separated by an operation on the NULL stream, preventing concurrency unless non-blocking streams are used.
- [Stream Overlap](../../../concepts/stream-overlap.md) — The amount of execution overlap between streams depends on device capabilities (concurrent data transfers, kernel execution overlap) and the order of commands issued.
- [Host Functions (Callbacks)](../../../concepts/host-functions-callbacks.md) — Host functions allow inserting CPU callbacks into a CUDA stream that execute after preceding commands complete, but must not make CUDA API calls to avoid deadlock.
- [Stream Priorities](../../../concepts/stream-priorities.md) — Stream priorities allow influencing task execution order via `cudaStreamCreateWithPriority`, serving as hints for the GPU scheduler rather than strict guarantees.
- [Programmatic Dependent Launch](../../../concepts/programmatic-dependent-launch.md) — A mechanism allowing a secondary kernel to launch before its primary dependency completes, enabling concurrent execution of independent work.
- [CUDA Graphs](../../../concepts/cuda-graphs.md) — CUDA Graphs present a model for work submission where a graph of operations is defined, instantiated, and then launched repeatedly, reducing CPU overhead and enabling optimizations.
- [CUDA User Objects](../../../concepts/cuda-user-objects.md) — CUDA User Objects provide a reference-counted mechanism to manage the lifetime of resources associated with asynchronous work and CUDA Graphs, using destructor callbacks similar to C++ shared_ptr.
- [Graph Update](../../../concepts/graph-update.md) — Graph update mechanisms allow modification of instantiated CUDA graphs without full re-instantiation, supporting both whole-graph and individual node updates under specific topological and parameter constraints.
