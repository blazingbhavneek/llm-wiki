# GPU Memory Oversubscription (Pre-6.x)

In the context of CUDA programming, GPU memory oversubscription refers to the ability of an application to allocate more managed memory than is physically available on the GPU. This capability is strictly dependent on the compute capability of the device.

## Limitations for Compute Capability < 6.0

Devices with a compute capability lower than 6.0 cannot allocate more managed memory than the physical size of the GPU memory [CUDA_C_Programming_Guide:L21833-L21836]. This means that for these older architectures, the total amount of managed memory requested by the application is capped at the physical memory capacity of the GPU, preventing oversubscription scenarios that might be supported on newer hardware.

## Context

This restriction is part of the managed memory features described in the CUDA C Programming Guide, specifically under the section detailing GPU memory oversubscription capabilities [CUDA_C_Programming_Guide:L21833-L21836].
