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
