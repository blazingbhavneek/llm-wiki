# CUDA Dynamic Parallelism (CDP1) Kernel Overhead

When dynamic parallelism is enabled, system software active for controlling dynamic launches may impose an overhead on any kernel running at that time, regardless of whether the kernel itself invokes other kernel launches [CUDA_C_Programming_Guide:L14902-L14907].

This overhead arises from the device runtime’s execution tracking and management software [CUDA_C_Programming_Guide:L14902-L14907]. It is generally incurred for applications that link against the device runtime library [CUDA_C_Programming_Guide:L14902-L14907].

A potential consequence of this overhead is decreased performance for specific operations, such as library calls, when they are executed from the device compared to when they are executed from the host side [CUDA_C_Programming_Guide:L14902-L14907].

For the version of dynamic parallelism introduced in later architectures (CDP2), see the corresponding documentation on Dynamic-parallelism-enabled Kernel Overhead.
