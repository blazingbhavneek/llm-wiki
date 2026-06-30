# Host Native Atomics

Describes hardware-accelerated atomic accesses to CPU-resident memory on NVLink-connected coherent systems, eliminating the need for page fault emulation.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21750-L21753

Citation: [CUDA_C_Programming_Guide:L21750-L21753]

````text
## 24.2.2.3 Host Native Atomics

Some devices, including NVLink-connected devices in hardware coherent systems, support hardwareaccelerated atomic accesses to CPU-resident memory. This implies that atomic accesses to host memory do not have to be emulated with a page fault. For these devices, the attribute cudaDevAttrHostNativeAtomicSupported is set to 1.
````
