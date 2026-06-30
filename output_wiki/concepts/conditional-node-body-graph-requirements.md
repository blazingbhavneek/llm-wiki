# Conditional Node Body Graph Requirements

Covers constraints on the body graphs of conditional nodes: single-device nodes, allowed node types (kernel, empty, memcpy, memset, child graph, conditional), restrictions on Dynamic Parallelism/Device Graph Launch, MPS limits, and memory access rules matching device graph requirements.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3143-L3164

Citation: [CUDA_C_Programming_Guide:L3143-L3164]

````text
## 6.2.8.7.8.2 Conditional Node Body Graph Requirements

## General requirements:

The graph’s nodes must all reside on a single device.

▶ The graph can only contain kernel nodes, empty nodes, memcpy nodes, memset nodes, child graph nodes, and conditional nodes.

## Kernel nodes:

▶ Use of CUDA Dynamic Parallelism or Device Graph Launch by kernels in the graph is not permitted.

▶ Cooperative launches are permitted so long as MPS is not in use.

## Memcpy/Memset nodes:

▶ Only copies/memsets involving device memory and/or pinned device-mapped host memory are permitted.

▶ Copies/memsets involving CUDA arrays are not permitted.

▶ Both operands must be accessible from the current device at time of instantiation. Note that the copy operation will be performed from the device on which the graph resides, even if it is targeting memory on another device.
````
