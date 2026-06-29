# 21.1. Context

Part of [Cuda C Programming Guide Reference](README.md). Source lines L20155-L20555.

- [CUDA Context](../../../concepts/cuda-context.md) — A CUDA context is analogous to a CPU process, encapsulating all resources and actions performed within the driver API, with each context maintaining its own distinct address space and managed via a stack per host thread.
- [CUDA Module](../../../concepts/cuda-module.md) — CUDA modules are dynamically loadable packages of device code and data, output by nvcc, that maintain symbol scope to allow interoperability between independent third-party modules within the same CUDA context.
- [Kernel Execution Parameters and Alignment](../../../concepts/kernel-execution-parameters.md) — cuLaunchKernel passes kernel arguments via an array of pointers or a parameter buffer, where the latter requires strict alignment matching device code requirements to handle differences between host and device representations.
- [Runtime and Driver API Interoperability](../../../concepts/runtime-driver-interoperability.md) — CUDA applications can mix Runtime and Driver API code, allowing contexts and device memory to be shared between the two interfaces through implicit context management and pointer casting.
- [Driver Entry Point Access](../../../concepts/driver-entry-point-access.md) — Driver Entry Point Access APIs allow retrieving the address of CUDA driver functions via function pointers, enabling ABI compatibility across different CUDA versions and access to new features with older toolkits.
