## oneAPI GPU Optimization Guide

## Contents

Chapter 1: oneAPI GPU Optimization Guide
Introduction....4
Getting Started....5
Parallelization....6
Intel® Xe GPU Architecture....7
General-Purpose Computing on GPU....17
Execution Model Overview....18
Thread Mapping and GPU Occupancy....19
Kernels....34
Sub-Groups and SIMD Vectorization....34
Removing Conditional Checks....41
Registers and Performance....44
Shared Local Memory....65
Pointer Aliasing and the Restrict Directive....72
Synchronization among Threads in a Kernel....76
Considerations for Selecting Work-Group Size....86
Prefetch....90
Reduction....94
Kernel Launch....100
Executing Multiple Kernels on the Device at the Same Time....102
Submitting Kernels to Multiple Queues....104
Avoiding Redundant Queue Constructions....107
Programming Intel® XMX Using SYCL Joint Matrix Extension....111
Doing I/O in the Kernel....113
Optimizing Explicit SIMD Kernels....116
Using Libraries for GPU Offload....127
Using Performance Libraries....127
Using Standard Library Functions in SYCL Kernels....129
Efficiently Implementing Fourier Correlation Using oneAPI Math Kernel Library (oneMKL)....131
Boost Matrix Multiplication Performance with Intel® Xe Matrix Extensions....139
Host/Device Memory, Buffer and USM....141
Unified Shared Memory Allocations....142
Performance Impact of USM and Buffers....143
Avoiding Moving Data Back and Forth between Host and Device....147
Optimizing Data Transfers....151
Avoiding Declaring Buffers in a Loop....159
Buffer Accessor Modes....161
Host/Device Coordination....167
Asynchronous and Overlapping Data Transfers Between Host and Device....167
Using Multiple Heterogeneous Devices....172
Compilation....174
Just-In-Time Compilation....174
Ahead-Of-Time Compilation....177
Specialization Constants....177

Accuracy Versus Performance Tradeoffs in Floating-Point Computations....183  
OpenMP Offloading Tuning Guide....194  
OpenMP Directives....195  
OpenMP Execution Model....196  
Terminology....196  
Compiling and Running an OpenMP Application....197  
Offloading oneMKL Computations onto the GPU....199  
Tools for Analyzing Performance of OpenMP Applications....210  
OpenMP Offload Best Practices....211  
Multi-GPU and Multi-Stack Architecture and Programming....297  
Multi-Stack GPU Architecture....297  
Exposing the Device Hierarchy....303  
FLAT Mode Programming....305  
COMPOSITE Mode Programming....310  
Using Intel® oneAPI Math Kernel Library (oneMKL)....329  
Using Intel® MPI Library....340  
Advanced Topics....353  
Terminology....366  
Level Zero....371  
Immediate Command Lists....371  
Performance Profiling and Analysis....372  
Using the Timers....373  
Intel® VTuneTM Profiler....375  
Intel® Advisor....375  
Intel® Intercept Layer for OpenCLTM Applications....376  
Performance Tools in Intel® Profiling Tools Interfaces for GPU....376  
Configuring GPU Device....376  
Media Graphics Computing on GPU....378  
Optimizing Media Pipelines....378  
Media Engine Hardware....379  
Media API Options for Hardware Acceleration....381  
Media Pipeline Parallelism....382  
Media Pipeline Inter-operation and Memory Sharing....384  
SYCL-Blur Example....389  
Performance Analysis with Intel® Graphics Performance Analyzers....390  
References....404  
Terms and Conditions....405

# oneAPI GPU Optimization Guide

![](images/26d9ff77e6b85301d31c9ca0b95d5cffcc647a062b5cc976d38aaf1352fa49bb.jpg)

Welcome to the oneAPI GPU Optimization Guide. This document gives tips for getting the best GPU performance for oneAPI programs.

• Introduction

• Getting Started

• Parallelization

• Intel<sup>®</sup> X<sup>e</sup> GPU Architecture

• General-Purpose Computing on GPU

• Media Graphics Computing on GPU

• References

• Terms and Conditions

## Introduction

Designing high-performance heterogeneous-computing software taking advantages of accelerators like, GPUs, for example, requires you to think differently than you do for traditional homogeneous- computing software. You need to be aware of the hardware on which your code is intended to run, and the characteristics that control the performance of that hardware. Your goal is to structure the code such that it produces correct answers in a way that maximizes the hardware’s ability.

oneAPI is a cross-industry, open, standards-based, unified programming model that delivers a common developer experience across accelerator architectures. A unique feature of accelerators is that they are additive to the main CPU on the platform. The primary benefit of using an accelerator is to improve the behavior of your software by partitioning it across the host and accelerator to specialize portions of the computation that run best on the accelerator. Accelerator architectures can offer a benefit through specialization of compute hardware for certain classes of computations. This enables them to deliver best results for software specialized to the accelerator architecture.

The primary focus of this document is GPUs. Each section focuses on different topics to guide you in your path to creating optimized solutions. The Intel<sup>®</sup> oneAPI Toolkits provide the languages and development tools you will use to optimize your code. This includes compilers, debuggers, profilers, analyzers, and libraries.

## Productive Performance

While this document focuses on GPUs, you may also need your application to run on CPUs and other types of accelerators. Since accelerator architectures are specialized, you need to specialize your code to achieve best performance. Specialization includes restructuring and tuning the code to create the best mapping of the application to the hardware. In extreme cases, this may require redesigning your algorithms for each accelerator to best expose the right type of computation. The value of oneAPI is that it allows each of these variations to be expressed in a common language with device-specific variants launched on the appropriate accelerator.

## Performance Considerations

The first consideration in using a GPU is to identify which parts of the application can benefit. This is usually compute-intensive code that has the right ratio of memory access to computation, and has the right data dependence patterns to map onto the GPU. GPUs include local memory and typically provide massive parallelism. This determines which characteristics of the code are most important when deciding what to offload.

The Intel<sup>®</sup> Advisor tool included in the Intel<sup>®</sup> oneAPI Base Toolkit is designed to analyze your code, including memory access to computation ratio, and help you identify the best opportunities for parallel execution. The profilers in Intel<sup>®</sup> Advisor measure the data movement in your functions, the memory access patterns, and the amount of computation in order to project how code will perform when mapped onto different accelerators. The code regions with highest potential benefit should be your first targets for acceleration.

GPUs often exploit parallelism at multiple levels. This includes overlap between host and device, parallelism across the compute cores, overlap between compute and memory accesses, concurrent pipelines, and vector computations. Exploiting all levels of parallelism requires a good understanding of the GPU architecture, the programming language, the libraries, and the analysis tools providing performance insights at your disposal.

Keep all the compute resources busy. There must be enough but you only have one task, 99% of the device will be idle. Often you create many more independent tasks than available compute resources so that the hardware can schedule more work as prior tasks complete.

Minimize the synchronization between the host and the device. The host launches a kernel on the device and waits for its completion. Launching a kernel incurs overhead, so structure the computation to minimize the number of times a kernel is launched.

Minimize the data transfer between host and device. Data typically starts on the host and is copied to the device as input to the computation. When a computation is finished, the results must be transferred back to the host. For best performance, minimize data transfer by keeping intermediate results on the device between computations. Reduce the impact of data transfer by overlapping computation and data movement so the compute cores never have to wait for data.

Keep the data in faster memory and use an appropriate access pattern. GPU architectures have different types of memory and these have different access costs. Registers, caches, and scratchpads are cheaper to access than local memory, but have smaller capacity. When data is loaded into a register, cache line, or memory page, use an access pattern that will use all the data before moving to the next chunk. When memory is banked, use a stride that avoids all the compute cores trying to access the same memory bank simultaneously.

## Profiling and Tuning

After you have designed your code for high performance, the next step is to measure how it runs on the target accelerator. Add timers to the code, collect traces, and use tools like Intel<sup>®</sup> VTune<sup>TM</sup> Profiler to observe the program as it runs. The information collected can identify where hardware is bottlenecked and idle, illustrate how behavior compares with peak hardware roofline, and identify the most important hotspots to focus optimization efforts.

## Source Code Examples

Throughout the guide, we use real code examples to illustrate optimization techniques. All the examples in this guide can be found in the oneAPI-samples GitHub repo. Now it is the perfect time to download the examples and set up your environment by following the instructions there.

We try hard to keep the examples as short and easy to follow as possible so optimization techniques in each example are not clouded by complexities of the example and can be quickly grasped. Code snippets from the examples are referenced throughout the text.

There is an old saying “I hear and I forget. I see and I remember. I do and I understand.”. It is strongly suggested that you pause to try the example on a real machine when a code snippet is encountered while reading the text.

Welcome to Intel<sup>®</sup> oneAPI GPU Optimization Guide!
