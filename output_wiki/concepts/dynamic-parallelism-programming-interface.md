# Dynamic Parallelism Programming Interface

The Dynamic Parallelism Programming Interface, also known as the Device Runtime API or CDP API, consists of CUDA C++ language extensions and an API layer that enables CUDA kernels to launch other kernels dynamically. This interface is described in the context of changes and additions to the CUDA C++ language extensions for supporting Dynamic Parallelism [CUDA_C_Programming_Guide:L13820-L13824].

## Device Runtime API

The language interface and API available to CUDA kernels using CUDA C++ for Dynamic Parallelism is referred to as the Device Runtime [CUDA_C_Programming_Guide:L13825-L13828]. It is substantially similar to the CUDA Runtime API available on the host [CUDA_C_Programming_Guide:L13825-L13828]. To facilitate ease of code reuse for routines that may run in either the host or device environments, the syntax and semantics of the CUDA Runtime API have been retained where possible [CUDA_C_Programming_Guide:L13825-L13828].

## Per-Thread Execution

As with all code in CUDA C++, the APIs and code outlined in the Device Runtime are per-thread code [CUDA_C_Programming_Guide:L13825-L13828]. This design enables each thread to make unique, dynamic decisions regarding what kernel or operation to execute next [CUDA_C_Programming_Guide:L13825-L13828].

There are no synchronization requirements between threads within a block to execute any of the provided device runtime APIs [CUDA_C_Programming_Guide:L13825-L13828]. This allows device runtime API functions to be called in arbitrarily divergent kernel code without causing deadlock [CUDA_C_Programming_Guide:L13825-L13828].
