# Difference between Unified Memory and Mapped Memory

The primary distinction between Unified Memory and Mapped Memory lies in the guarantee of memory access support across different systems.

CUDA Mapped Memory does not guarantee that all kinds of memory accesses, such as atomics, are supported on all systems. In contrast, Unified Memory provides this guarantee. However, the limited set of memory operations that are guaranteed to be portably supported by CUDA Mapped Memory is available on more systems than those supporting Unified Memory [CUDA_C_Programming_Guide:L21101-L21104].

## Key Differences

*   **Unified Memory**: Guarantees support for all kinds of memory accesses (including atomics) across systems.
*   **Mapped Memory**: Does not guarantee support for all memory operations (e.g., atomics) on all systems. It supports a limited set of portably guaranteed operations but has broader system availability.

## Availability

Mapped Memory is available on a wider range of systems compared to Unified Memory, making it a more portable option for basic memory operations, albeit with fewer guarantees regarding advanced memory access types like atomics [CUDA_C_Programming_Guide:L21101-L21104].
