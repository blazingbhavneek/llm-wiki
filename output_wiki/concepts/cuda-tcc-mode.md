# Tesla Compute Cluster (TCC) Mode

Describes TCC mode, a configuration for Tesla and Quadro GPUs on Windows via nvidia-smi. TCC mode disables all graphics functionality, optimizing the device for pure compute workloads.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L6119-L6121

Citation: [CUDA_C_Programming_Guide:L6119-L6121]

````text
Using NVIDIA’s System Management Interface (nvidia-smi), the Windows device driver can be put in TCC (Tesla Compute Cluster) mode for devices of the Tesla and Quadro Series.

TCC mode removes support for any graphics functionality.
````
