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

## Getting Started

Three key concepts govern software optimization for an accelerator. These concepts should guide your optimization efforts.

## Amdahl’s Law

This may appear obvious, but it is the first step in making use of an accelerator. Amdahl’s law states that the fraction of time an application uses an accelerator $( { \cal F } _ { p } )$ limits the benefit of acceleration. The maximum speedup is bounded by $1 / ( 1 - F _ { p } )$ . If you use the accelerator of the time, you will get at most a $2 \times$ speedup, even with an infinitely powerful accelerator.

Note here that this is in terms of your program execution, not your program’s source code. The parallel kernels may represent a very small fraction of your overall source code, but if this is where you execution time is concentrated, you can still do well.

## Locality

An accelerator often has specialized memory with a disjoint address space. An application must allocate or move data into the right memory at the right time.

Accelerator memory is arranged in a hierarchy. Registers are more efficient to access than caches, and caches are more efficient to access than main memory. Bringing data closer to the point of execution improves efficiency.

There are many ways you can refactor your code to get your data closer to the execution. They will be outlined in the following sections. Here, we focus on three:

1. Allocate your data on the accelerator, and when copied there, keep it resident for as long as possible. Your application may have many offloaded regions. If you have data that is common between these regions, it makes sense to amortize the cost of the first copy, and just reuse it in place for the remaining kernel invocations.

2. Access contiguous blocks of memory as your kernel executes. The hardware will fetch contiguous blocks into the memory hierarchy, so you have already paid the cost for the entire block. After you use the first element of the block, the remaining elements are almost free to access so take advantage of it.

3. Restructure your code into blocks with higher data reuse. In a two-dimensional matrix, you can arrange your work to process one block of elements before moving onto the next block of elements. For example, in a stencil operation you may access the prior row, the current row, and the next row. As you walk over the elements in a block you reuse the data and avoid the cost of requesting it again.

## Work Size

Data-parallel accelerators are designed as throughput engines and are often specialized by replicating execution units many times. This is an easy way of getting higher performance on data-parallel algorithms since more of the elements can be processed at the same time.

However, fully utilizing a parallel processor can be challenging. For example, imagine you have 512 execution units, where each execution unit had eight threads, and each thread has 16-element vectors. You need to have a minimum of $5 1 2 \times 8 \times 1 6 = 6 5 5 3 6$ parallel activities scheduled at all times just to match this capacity. In addition, if each parallel activity is small, you need another large factor to amortize the cost of submitting this work to the accelerator. Fully utilizing a single large accelerator may require decomposing a computation into millions of parallel activities.

## Parallelization

Parallelism is essential to effective use of accelerators because they contain many independent processing elements that are capable of executing code in parallel. There are three ways to develop parallel code.

## Programming Language and APIs

There are many parallel programming languages and APIs that can be used to express parallelism. oneAPI is an open industry standard for heterogeneous computing. It supports parallel program development through the SYCL\* framework. The Intel<sup>®</sup> oneAPI products have a number of code generation tools to convert source programs into binaries that can be executed on different accelerators. The usual workflow is that a user starts with a serial program, identifies the parts of the code that take a long time to execute (referred to as hotspots), and converts them into parallel kernels that can be offloaded to an accelerator for execution.

## Compilers

Directive-based approaches like OpenMP\* are another way to develop parallel programs. In a directive-based approach, the programmer provides hints to the compiler about parallelism without modifying the code explicitly. This approach is easier than developing a parallel program from first principles.

## Libraries

A number of libraries like oneTBB, oneMKL, Intel<sup>®</sup> oneAPI Deep Neural Network Library (oneDNN), and Intel<sup>®</sup> Video Processing Library (Intel<sup>®</sup> VPL) provide highly-optimized versions of common computational operations run across a variety of accelerator architectures. Depending on the needs of the application, a user can directly call the functions from these libraries and get efficient implementations of these for the underlying architecture. This is the easiest approach to developing parallel programs, provided the library contains the required functions. For example, machine learning applications can take advantage of the optimized primitives in oneDNN. These libraries have been thoroughly tested for both correctness and performance, which makes programs more reliable when using them.

## Intel® Xe GPU Architecture

The Intel<sup>®</sup> X<sup>e</sup> GPU family consists of a series of microarchitectures, ranging from integrated/low power (X<sup>e</sup>- LP), to enthusiast/high performance gaming (X<sup>e</sup>-HPG), data center/AI (X<sup>e</sup>-HP) and high performance computing (X<sup>e</sup>-HPC).

Intel® Iris® Xe family

![](images/e6d76b68db83f6de54b4d6ae986065bcaf438168e3ec66b48c1dbd207e8d6612.jpg)

## X<sup>e</sup>-LP Execution Units (EUs)

An Execution Unit (EU) is the smallest thread-level building block of the Intel<sup>®</sup> Iris<sup>®</sup> X<sup>e</sup>-LP GPU architecture. Each EU is simultaneously multithreaded (SMT) with seven threads. The primary computation unit consists of a 8-wide Single Instruction Multiple Data (SIMD) Arithmetic Logic Units (ALU) supporting SIMD8 FP/INT operations and a 2-wide SIMD ALU supporting SIMD2 extended math operations. Each hardware thread has 128 general-purpose registers (GRF) of 32B wide.

Xe-LP-EU  
![](images/46a9cea8ece5f5a3a74a363737747ce73c8016c9a1db7f7d122774144dc5545c.jpg)  
X<sup>e</sup>-LP EU supports diverse data types FP16, INT16 and INT8 for AI applications. The following table shows the EU operation throughput of X<sup>e</sup>-LP GPU for various data types.

Intel<sup>®</sup> Iris<sup>®</sup> X<sup>e</sup>-LP GPU Compute Throughput Rates (Ops/clock/EU)

<table><tr><td>FP32</td><td>FP16</td><td>INT32</td><td>INT16</td><td>INT 8</td></tr><tr><td>8</td><td>16</td><td>8</td><td>16</td><td>32 (DP4A)</td></tr></table>

## X<sup>e</sup>-LP Dual Subslices

Each X<sup>e</sup>-LP Dual Subslice (DSS) consists of an EU array of 16 EUs, an instruction cache, a local thread dispatcher, Shared Local Memory (SLM), and a data port of 128B/cycle. It is called dual subslice because the hardware can pair two EUs for SIMD16 executions.

The SLM is 128KB of low latency and high bandwidth memory accessible from the EUs in the subslice. One important usage of SLM is to share atomic data and signals among the concurrent work-items executing in a subslice. For this reason, if a kernel’s work-group contains synchronization operations, all work-items of the work-group must be allocated to a single subslice so that they have shared access to the same 128KB SLM. The work-group size must be chosen carefully to maximize the occupancy and utilization of the subslice. In contrast, if a kernel does not access SLM, its work-items can be dispatched across multiple subslices.

The following table summarizes the computing capacity of a Intel<sup>®</sup> Iris<sup>®</sup> X<sup>e</sup>-LP subslice.

Intel<sup>®</sup> Iris<sup>®</sup> X<sup>e</sup>-LP subslice computing capacity

<table><tr><td>EUs</td><td>Threads</td><td>Operations</td></tr><tr><td>16</td><td> $7 \times 16 = 112$ </td><td> $112 \times 8 = 896$ </td></tr></table>

## X<sup>e</sup>-LP Slice

Each X<sup>e</sup>-LP slice consists of six (dual) subslices for a total of 96 EUs, up to 16MB L2 cache, 128B/cycle bandwidth to L2 and 128B/cycle bandwidth to memory.

Xe-LP slice  
![](images/7dae06dc26eeccefa65026106c5cba1b1e166bcdaa98d3d468ae4474e8d6cfba.jpg)

## X<sup>e</sup>-Core

Unlike the X<sup>e</sup>-LP and prior generations of Intel GPUs that used the Execution Unit (EU) as a compute unit, ${ \tt X } ^ { \tt e _ { - } }$ HPG and $\mathsf { X } ^ { \mathsf { e } . }$ -HPC use the $\mathsf { X } ^ { \mathsf { e } _ { \mathsf { - } } }$ core. This is similar to an ${ \tt X } ^ { \tt e \mathrm { \mathrm { - } \mathrm { 1 } \mathrm { P } } }$ dual subslice.

An $\mathsf { X } ^ { \mathsf { e } _ { \mathsf { - } } }$ core contains vector and matrix ALUs, which are referred to as vector and matrix engines.

An X<sup>e</sup>-core of the ${ \tt X } ^ { \tt e _ { - \displaystyle H P C } }$ GPU contains 8 vector and 8 matrix engines, alongside a large 512KB L1 cache/ SLM. It powers the Intel<sup>®</sup> Data Center GPU Max Series. Each vector engine is 512 bit wide supporting 16 FP32 SIMD operations with fused FMAs. With 8 vector engines, the X<sup>e</sup>-core delivers 512 FP16, 256 FP32 and

128 FP64 operations/cycle. Each matrix engine is 4096 bit wide. With 8 matrix engines, the X<sup>e</sup>-core delivers 8192 int8 and 4096 FP16/BF16 operations/cycle. The X<sup>e</sup>-core provides 1024B/cycle load/store bandwidth to the memory system.

## Xe-core

![](images/3d329c67ee987b25e1b5f03f3b7f60fe83c1091605c20d26321581a97afaaf35.jpg)

## X<sup>e</sup>-Slice

An X<sup>e</sup>-slice contains 16 X<sup>e</sup>-core for a total of 8MB L1 cache, 16 ray tracing units and 1 hardware context.

## Xe-slice

![](images/552e908f361ffcb35ddabe7e8940a559bfbcc89aa8524e82b958228c1456e784.jpg)

## X<sup>e</sup>-Stack

An X<sup>e</sup>-stack contains up to 4 X<sup>e</sup>-slice: 64 X<sup>e</sup>-cores, 64 ray tracing units, 4 hardware contexts, 4 HBM2e controllers, 1 media engine, and 8 X<sup>e</sup>-Links of high speed coherent fabric. It also contains a shared L2 cache.

## Xe-stack

![](images/70919005ac7d6234ee06eda8d1e718c9d87bc849cb47e3ae66f05a4a93f59626.jpg)

## X<sup>e</sup>-HPC 2-Stack Data Center GPU Max

An X<sup>e</sup>-HPC 2-stack Data Center GPU Max, previously code named Ponte Vecchio or PVC, consists of up to 2 stacks:: 8 slices, 128 X<sup>e</sup>-cores, 128 ray tracing units, 8 hardware contexts, 8 HBM2e controllers, and 16 X<sup>e</sup>- Links.

Xe-HPC 2-Stack  
![](images/54e60d1c84d4e4f68c4ffc5444987a6b376b494154c4dcedaac25b8ec4175064.jpg)

## X<sup>e</sup>-HPG GPU

X<sup>e</sup>-HPG is the enthusiast or high performance gaming variant of the X<sup>e</sup> architecture. The microarchitecture is focused on graphics performance and supports hardware-accelerated ray tracing.

An X<sup>e</sup>-core of the X<sup>e</sup>-HPG GPU contains 16 vector and 16 matrix engines. It powers the Intel<sup>®</sup> Arc GPUs. Each vector engine is 256 bit wide, supporting 8 FP32 SIMD operations with fused FMAs. With 16 vector engines, the X<sup>e</sup>-core delivers 256 FP32 operations/cycle. Each matrix engine is 1024 bit wide. With 16 matrix engines, the X<sup>e</sup>-core delivers 4096 int8 and 2048 FP16/BF16 operations/cycle. The X<sup>e</sup>-core provides 512B/cycle load/ store bandwidth to the memory system.

An X<sup>e</sup>-HPG GPU consists of 8 X<sup>e</sup>-HPG-slice, which contains up to 4 X<sup>e</sup>-HPG-cores for a total of 4096 FP32 ALU units/shader cores.

## X<sup>e</sup>- Intel<sup>®</sup> Data Center GPU Flex Series

Intel<sup>®</sup> Data Center GPU Flex Series come in two configurations. The 150W option has 32 X<sup>e</sup>-cores on a PCIe Gen4 card. The 75W option has two GPUs for 16 X<sup>e</sup>-cores (8 X<sup>e</sup>-cores per GPU). Both configurations come with 4 X<sup>e</sup> media engines, the industry’s first AV1 hardware encoder and accelerator for data center, GDDR6 memory, ray tracing units, and built-in XMX AI acceleration.

Intel<sup>®</sup> Data Center GPU Flex Series are derivatives of the X<sup>e</sup>-HPG GPUs. An Intel<sup>®</sup> Data Center GPU Flex 170 consists of 8 X<sup>e</sup>-HPG-slices for a total of 32 X<sup>e</sup>-cores with 4096 FP32 ALU units/shader cores.

Targeting data center cloud gaming, media streaming and video analytics applications, Intel<sup>®</sup> Data Center GPU Flex Series provide hardware accelerated AV1 encoder, delivering a 30% bit-rate improvement without compromising on quality. It supports 8 simultaneous 4K streams or more than 30 1080p streams per card. AI models can be applied to the decoded streams utilizing Intel<sup>®</sup> Data Center GPU Flex Series’ X<sup>e</sup>-cores.

Media streaming and delivery software stacks lean on Intel<sup>®</sup> Video Processing Library (Intel VPL) to decode and encode acceleration for all the major codecs including AV1. Media distributors can choose from the two leading media frameworks FFMPEG or GStreamer, both enabled for acceleration with Intel VPL on Intel CPUs and GPUs.

In parallel to Intel VPL accelerating decoding and encoding of media streams, Intel<sup>®</sup> oneAPI Deep Neural Network Library (oneDNN) delivers AI optimized kernels enabled to accelerate inference modes in TensorFlow or PyTorch frameworks, or with the OpenVINO model optimizer and inference engine to further accelerate inference and speed customer deployment of their workloads.

## Terminology and Configuration Summary

The following table maps legacy GPU terminologies (used in Generation 9 through Generation 12 Intel<sup>®</sup> Core<sup>TM</sup> architectures) to their new names in the Intel<sup>®</sup> Iris<sup>®</sup> X<sup>e</sup> GPU (Generation 12.7 and newer) architecture paradigm.

Architecture Terminology Changes

<table><tr><td>Old Term</td><td>New Intel Term</td><td>Generic Term</td><td>New Abbreviation</td></tr><tr><td>Execution Unit (EU)</td><td>XeVector Engine</td><td>Vector Engine</td><td>XVE</td></tr><tr><td>Systolic/&quot;DPAS part of EU&quot;</td><td>XeMatrix eXtension</td><td>Matrix Engine</td><td>XMX</td></tr><tr><td>Subslice (SS) or Dual Subslice (DSS)</td><td>Xe-core</td><td>NA</td><td>XC</td></tr><tr><td>Slice</td><td>Render Slice / Compute Slice</td><td>Slice</td><td>SLC</td></tr><tr><td>Tile</td><td>Stack</td><td>Stack</td><td>STK</td></tr></table>

The following table lists the hardware characteristics across the X<sup>e</sup> family GPUs.

X<sup>e</sup> Configurations

<table><tr><td>Architecture</td><td>Xe-LP (TGL)</td><td>Xe-HPG (Arc A770)</td><td>Xe-HPG (Data Center GPU Flex 170)</td><td>Xe-HPC (Data Center GPU Max 1550)</td></tr><tr><td>Slice count</td><td>1</td><td>8</td><td>8</td><td>4 x 2</td></tr><tr><td>XC (DSS/SS) count</td><td>6</td><td>32</td><td>32</td><td>64 x 2</td></tr><tr><td>XVE (EU) / XC</td><td>16</td><td>16</td><td>16</td><td>8</td></tr><tr><td>XVE count</td><td>96</td><td>512</td><td>512</td><td>512 x 2</td></tr><tr><td>Threads / XVE</td><td>7</td><td>8</td><td>8</td><td>8</td></tr><tr><td>Thread count</td><td>672</td><td>4096</td><td>4096</td><td>4096 x 2</td></tr><tr><td>FLOPs / clk - single precision, MAD</td><td>1536</td><td>8192</td><td>8192</td><td>16384 x 2</td></tr><tr><td>FLOPs / clk - double precision, MAD</td><td>NA</td><td>NA</td><td>NA</td><td>16384 x 2</td></tr><tr><td>FLOPs / clk - FP16 DP4AS</td><td>NA</td><td>65536</td><td>65536</td><td>262144 x 2</td></tr><tr><td>GTI bandwidth bytes / unslice-clk</td><td>r:128, w:128</td><td>r:512, w:512</td><td>r:512, w:512</td><td>r:1024, w:1024</td></tr><tr><td>LL cache size</td><td>3.84MB</td><td>16MB</td><td>16MB</td><td>up to 408MB</td></tr><tr><td>SLM size</td><td>6 × 128KB × 2</td><td>32 × 128KB × 2</td><td>32 × 128KB × 2</td><td>64 × 128KB × 2</td></tr><tr><td>FMAD, SP (ops / XVE / clk)</td><td>8</td><td>8</td><td>8</td><td>16</td></tr><tr><td>SQRT, SP (ops / XVE / clk)</td><td>2</td><td>2</td><td>2</td><td>4</td></tr></table>

## General-Purpose Computing on GPU

Traditionally, GPUs are used for creating computer graphics such as images, videos, etc. Due to their large number of execution units for massive parallelism, modern GPUs are also used for computing tasks that are conventionally performed on CPU. This is commonly referred to as General-Purpose Computing on GPU or GPGPU.

Many high performance computing and machine learning applications benefit greatly from GPGPU.

• Execution Model Overview

• Thread Mapping and GPU Occupancy

• Kernels

• Using Libraries for GPU Offload

• Host/Device Memory, Buffer and USM

• Inter-process Communication

• Host/Device Coordination

• Using Multiple Heterogeneous Devices

• Compilation

• OpenMP Offloading Tuning Guide

• Multi-GPU and Multi-Stack Architecture and Programming

• Level Zero

• Performance Profiling and Analysis

• Configuring GPU Device

## Execution Model Overview

The General Purpose GPU (GPGPU) compute model consists of a host connected to one or more compute devices. Each compute device consists of many GPU Compute Engines (CE), also known as Execution Units (EU) or X<sup>e</sup> Vector Engines (XVE or VE). The compute devices may also include caches, shared local memory (SLM), high-bandwidth memory (HBM), and so on, as shown in the figure below. Applications are then built as a combination of host software (per the host framework) and kernels submitted by the host to run on the VEs with a predefined decoupling point.

## General Purpose Compute Model

![](images/aa9e91ae4e19e54ab4399eb0369dcf43a153453328746582b38fee1646bdc9a4.jpg)

The GPGPU compute architecture contains two distinct units of execution: a host program and a set of kernels that execute within the context set by the host. The host interacts with these kernels through a command queue. Each device may have its own command queue. When a command is submitted into the command queue, the command is checked for dependencies and then executed on a VE inside the compute unit clusters. Once the command has finished executing, the kernel communicates an end of life cycle through “end of thread” message.

The GP execution model determines how to schedule and execute the kernels. When a kernel-enqueue command submits a kernel for execution, the command defines an index space or N-dimensional range. A kernel-instance consists of the kernel, the argument values associated with the kernel, and the parameters that define the index space. When a compute device executes a kernel-instance, the kernel function executes for each point in the defined index space or N-dimensional range.

An executing kernel function is called a work-item, and a collection of these work-items is called a workgroup. A compute device manages work-items using work-groups. Individual work-items are identified by either a global ID, or a combination of the work-group ID and a local ID inside the work-group.

The work-group concept, which essentially runs the same kernel on several unit items in a group, captures the essence of data parallel computing. The VEs can organize work-items in SIMD vector format and run the same kernel on the SIMD vector, hence speeding up the compute for all such applications.

A device can compute each work-group in any arbitrary order. Also, the work-items within a single workgroup execute concurrently, with no guarantee on the order of progress. A high level work-group function, like Barriers, applies to each work-item in a work-group, to facilitate the required synchronization points. Such a work-group function must be defined so that all work-items in the work-group encounter precisely the same work-group function.

Synchronization can also occur at the command level, where the synchronization can happen between commands in host command-queues. In this mode, one command can depend on execution points in another command or multiple commands.

Other types of synchronization based on memory-order constraints inside a program include Atomics and Fences. These synchronization types control how a memory operation of any particular work-item is made visible to another, which offers micro-level synchronization points in the data-parallel compute model.

Note that an Intel GPU device is equipped with many Vector Engines. Each VE is a multi-threaded SIMD processor. The compiler generates SIMD code to map several work-items to be executed simultaneously within a given hardware thread. The SIMD-width for a kernel is a heuristic driven compiler choice. Common SIMD-width examples are SIMD-8, SIMD-16, and SIMD-32.

For a given SIMD-width, if all kernel instances within a thread are executing the same instruction, the SIMD lanes can be maximally utilized. If one or more of the kernel instances choose a divergent branch, then the thread executes the two paths of the branch and merges the results by mask. The VE’s branch unit keeps track of such branch divergence and branch nesting.
