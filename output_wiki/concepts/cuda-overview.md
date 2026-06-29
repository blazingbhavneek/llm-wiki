# CUDA Overview

CUDA is a parallel computing platform and programming model developed by NVIDIA that enables dramatic increases in computing performance by harnessing the power of the GPU. It allows developers to accelerate compute-intensive applications using C, C++, and Fortran, and is widely adopted in fields such as deep learning, scientific computing, and high-performance computing (HPC) [CUDA_C_Programming_Guide:L760-L760].

## History and Purpose

In November 2006, NVIDIA introduced CUDA, a general-purpose parallel computing platform and programming model that leverages the parallel compute engine in NVIDIA GPUs to solve many complex computational problems in a more efficient way than on a CPU [CUDA_C_Programming_Guide:L789-L789].

## Hardware Architecture: GPU vs. CPU

The Graphics Processing Unit (GPU) provides much higher instruction throughput and memory bandwidth than the CPU within a similar price and power envelope. Many applications leverage these higher capabilities to run faster on the GPU than on the CPU [CUDA_C_Programming_Guide:L772-L780].

The difference in capabilities between the GPU and the CPU exists because they are designed with different goals in mind:

*   **CPU Design:** The CPU is designed to excel at executing a sequence of operations, called a thread, as fast as possible. It can execute a few tens of these threads in parallel [CUDA_C_Programming_Guide:L772-L780].
*   **GPU Design:** The GPU is designed to excel at executing thousands of threads in parallel. This approach amortizes the slower single-thread performance to achieve greater throughput [CUDA_C_Programming_Guide:L772-L780].

The GPU is specialized for highly parallel computations. Consequently, more transistors are devoted to data processing rather than data caching and flow control. The GPU can hide memory access latencies with computation, instead of relying on large data caches and complex flow control to avoid long memory access latencies, both of which are expensive in terms of transistors [CUDA_C_Programming_Guide:L772-L780].

While other computing devices, like FPGAs, are also very energy efficient, they offer much less programming flexibility than GPUs [CUDA_C_Programming_Guide:L772-L780]. In general, an application has a mix of parallel and sequential parts, so systems are designed with a mix of GPUs and CPUs to maximize overall performance. Applications with a high degree of parallelism can exploit the massively parallel nature of the GPU to achieve higher performance than on the CPU [CUDA_C_Programming_Guide:L772-L780].

## Software Environment

CUDA comes with a software environment that allows developers to use C++ as a high-level programming language. Other languages, application programming interfaces, or directives-based approaches are supported, such as FORTRAN, DirectCompute, and OpenACC [CUDA_C_Programming_Guide:L791-L791].
