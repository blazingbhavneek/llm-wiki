# GPU Memory Oversubscription

Explains how Unified Memory allows applications to allocate and share arrays larger than individual processor memory capacities, enabling out-of-core processing without significant model complexity.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21189-L21192

Citation: [CUDA_C_Programming_Guide:L21189-L21192]

````text
## 24.1.2.7 GPU Memory Oversubscription

Unified Memory enables applications to oversubscribe the memory of any individual processor: in other words they can allocate and share arrays larger than the memory capacity of any individual processor in the system, enabling among others out-of-core processing of datasets that do not fit within a single GPU, without adding significant complexity to the programming model.
````
