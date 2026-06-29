# CDP1 CUDA C++ Reference

This section describes the changes and additions to the CUDA C++ language extensions for supporting Dynamic Parallelism (CDP1). For the CDP2 version of this document, see the CUDA C++ Reference.

## Device Runtime Overview

The language interface and API available to CUDA kernels using CUDA C++ for Dynamic Parallelism is referred to as the **Device Runtime** [CUDA_C_Programming_Guide:L14486-L14495]. This interface is substantially similar to the CUDA Runtime API available on the host [CUDA_C_Programming_Guide:L14486-L14495]. Where possible, the syntax and semantics of the CUDA Runtime API have been retained to facilitate ease of code reuse for routines that may run in either the host or device environments [CUDA_C_Programming_Guide:L14486-L14495].

## Per-Thread Execution Model

As with all code in CUDA C++, the APIs and code outlined in the Device Runtime are per-thread code [CUDA_C_Programming_Guide:L14486-L14495]. This design enables each thread to make unique, dynamic decisions regarding what kernel or operation to execute next [CUDA_C_Programming_Guide:L14486-L14495].

There are no synchronization requirements between threads within a block to execute any of the provided device runtime APIs [CUDA_C_Programming_Guide:L14486-L14495]. This allows the device runtime API functions to be called in arbitrarily divergent kernel code without causing deadlock [CUDA_C_Programming_Guide:L14486-L14495].
