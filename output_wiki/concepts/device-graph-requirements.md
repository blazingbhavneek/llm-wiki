# Device Graph Requirements

Covers constraints for device graphs: single-device nodes, allowed node types (kernel, memcpy, memset, child graph), restrictions on CUDA Dynamic Parallelism, MPS cooperative launch limits, memory access rules for memcpy/memset (device/pinned host memory only, no CUDA arrays), and operand accessibility at instantiation.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2868-L2887

Citation: [CUDA_C_Programming_Guide:L2868-L2887]

````text
## 6.2.8.7.7.2 Device Graph Requirements

## General requirements:

▶ The graph’s nodes must all reside on a single device.

▶ The graph can only contain kernel nodes, memcpy nodes, memset nodes, and child graph nodes. Kernel nodes:

Use of CUDA Dynamic Parallelism by kernels in the graph is not permitted.

▶ Cooperative launches are permitted so long as MPS is not in use.

## Memcpy nodes:

▶ Only copies involving device memory and/or pinned device-mapped host memory are permitted.

▶ Copies involving CUDA arrays are not permitted.

▶ Both operands must be accessible from the current device at time of instantiation. Note that the copy operation will be performed from the device on which the graph resides, even if it is targeting memory on another device.
````
