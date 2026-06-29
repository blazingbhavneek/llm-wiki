# 10.31. Profiler Counter Function

Part of [Cuda C Programming Guide Reference](README.md). Source lines L11089-L11532.

- [Profiler Counter Function](../../../concepts/profiler-counter-function.md) — The __prof_trigger() function allows applications to increment per-multiprocessor hardware counters (0-7) for monitoring via nvprof.
- [Assertion in CUDA](../../../concepts/assertion-in-cuda.md) — Assertion support in CUDA devices (compute capability 2.x+) allows kernel execution to halt if an expression is zero, triggering debugger breakpoints or printing error messages to stderr.
- [Trap Function](../../../concepts/trap-function.md) — The __trap() function initiates a trap operation from any device thread, aborting kernel execution and raising an interrupt in the host program.
- [Breakpoint Function](../../../concepts/breakpoint-function.md) — The __brkpt() function suspends the execution of a kernel function when called from any device thread.
- [Formatted Output (printf) in CUDA](../../../concepts/printf-in-cuda.md) — CUDA provides device-side printf() support for compute capability 2.x and higher, allowing kernels to send formatted strings to a host-side buffer that is flushed via synchronization or memory operations.
- [Dynamic Global Memory Allocation](../../../concepts/dynamic-global-memory-allocation.md) — Dynamic global memory allocation allows CUDA kernels to allocate and free memory from a fixed-size device heap using functions like malloc and free, with allocations persisting for the lifetime of the context.
