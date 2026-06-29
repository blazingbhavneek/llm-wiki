# CUDA Performance Overhead

## Dynamic-parallelism-enabled Kernel Overhead

When an application links against the device runtime library, system software active for controlling dynamic kernel launches may impose an overhead on any kernel running at that time [CUDA_C_Programming_Guide:L14215-L14220].

This overhead arises from the device runtime’s execution tracking and management software [CUDA_C_Programming_Guide:L14215-L14220]. It is important to note that this performance impact occurs regardless of whether the specific kernel being executed invokes kernel launches of its own [CUDA_C_Programming_Guide:L14215-L14220]. The presence of this overhead may result in decreased overall performance [CUDA_C_Programming_Guide:L14215-L14220].

## Caveats

*   The information presented here is based on a deterministic fallback due to a research subagent failure; content is strictly derived from the assigned source evidence [CUDA_C_Programming_Guide:L14215-L14220].
