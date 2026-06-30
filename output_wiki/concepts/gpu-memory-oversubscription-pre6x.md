# GPU Memory Oversubscription on Pre-6.x

States the limitation that devices with compute capability lower than 6.0 cannot allocate more managed memory than the physical size of GPU memory.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21833-L21836

Citation: [CUDA_C_Programming_Guide:L21833-L21836]

````text

## 24.3.2.2 GPU Memory Oversubscription

Devices of compute capability lower than 6.0 cannot allocate more managed memory than the physical size of GPU memory.
````
