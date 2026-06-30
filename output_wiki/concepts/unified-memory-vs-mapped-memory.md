# Difference between Unified Memory and Mapped Memory

Explains the core difference: Mapped Memory lacks guaranteed support for all memory operations (e.g., atomics) across systems, while Unified Memory guarantees portability for these operations.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21101-L21104

Citation: [CUDA_C_Programming_Guide:L21101-L21104]

````text
## 24.1.2.4 Diference between Unified Memory and Mapped Memory

The main diference between Unified Memory and Mapped Memory is that CUDA Mapped Memory does not guarantee that all kinds of memory accesses (for example atomics) are supported on all systems, while Unified Memory does. The limited set of memory operations that are guaranteed to be portably supported by CUDA Mapped Memory is available on more systems than Unified Memory.
````
