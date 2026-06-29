# 21.5.4. Guidelines for cuGetProcAddress

Part of [Cuda C Programming Guide Reference](README.md). Source lines L20556-L21100.

- [Guidelines for cuGetProcAddress](../../../concepts/cugetprocaddress-guidelines.md)
- [cudaGetDriverEntryPointByVersion](../../../concepts/cudagetdriverentrypointbyversion.md)
- [cuGetProcAddress Error Handling](../../../concepts/cugetprocaddress-error-handling.md)
- [CUDA Environment Variables](../../../concepts/cuda-environment-variables.md) — Overview of CUDA environment variables used for configuring device enumeration, compilation, execution, module loading, and error logging.
- [Error Log Management](../../../concepts/error-log-management.md) — Error Log Management is a legacy mechanism introduced in CUDA Toolkit 12.9 that reports CUDA API errors in plain English, replacing generic return codes with descriptive messages.
- [Unified Memory Introduction](../../../concepts/unified-memory-introduction.md) — Unified Memory is a programming model introduced in CUDA 7.0 that provides a single, unified memory pool accessible by both CPU and GPU, with support varying based on device compute capability.
- [Unified Memory Support Levels](../../../concepts/unified-memory-support-levels.md) — CUDA Unified Memory support is categorized into four levels (Full, Managed Only, Managed Without Full Support, None) detectable via specific device properties such as pageableMemoryAccess, concurrentManagedAccess, and managedMemory.
- [Unified Memory Programming Model](../../../concepts/unified-memory-programming-model.md) — Unified Memory is a programming model that eliminates the need for separate host/device allocations and explicit memory transfers by allowing applications to allocate memory via system APIs, CUDA Managed Memory APIs, or managed variables.
- [System-Allocated Memory](../../../concepts/system-allocated-memory.md) — System-allocated memory refers to standard system memory (malloc, mmap, new) that is treated as unified memory on supported systems, utilizing first-touch policy for physical allocation and supporting CUDA Unified Memory APIs.
- [cudaMallocManaged](../../../entities/cudamallocmanaged.md) — An API for allocating CUDA Managed Memory that is syntactically identical to cudaMalloc.
- [__managed__ Variables](../../../concepts/managed-variables.md) — Global-scope managed variables using __managed__ keyword behave like cudaMallocManaged, simplifying data exchange between host and device by eliminating manual memory allocation and copying.
