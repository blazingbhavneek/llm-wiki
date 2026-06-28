17 Mathematical Functions 405
17.1 Standard Functions 405
17.2 Intrinsic Functions 414

18 C++ Language Support 419
18.1 C++11 Language Features 419
18.2 C++14 Language Features 422
18.3 C++17 Language Features 422
18.4 C++20 Language Features 423
18.5 Restrictions 423
18.5.1 Host Compiler Extensions 423
18.5.2 Preprocessor Symbols 423
18.5.2.1 \_\_CUDA\_ARCH\_\_ 423
18.5.3 Qualifiers 425
18.5.3.1 Device Memory Space Specifiers 425
18.5.3.2 \_\_managed\_\_ Memory Space Specifier 426

18.5.3.3 Volatile Qualifier . 427
18.5.4 Pointers . 429
18.5.5 Operators . 430
18.5.5.1 Assignment Operator . 430
18.5.5.2 Address Operator . 430
18.5.6 Run Time Type Information (RTTI) . 430
18.5.7 Exception Handling . 430
18.5.8 Standard Library . 430
18.5.9 Namespace Reservations . 430
18.5.10 Functions . 431
18.5.10.1 External Linkage . 431
18.5.10.2 Implicitly-declared and non-virtual explicitly-defaulted functions . 431
18.5.10.3 Function Parameters . 432
18.5.10.4 Static Variables within Function . 435
18.5.10.5 Function Pointers . 437
18.5.10.6 Function Recursion . 437
18.5.10.7 Friend Functions . 437
18.5.10.8 Operator Function . 437
18.5.10.9 Allocation and Deallocation Functions . 437
18.5.11 Classes . 438
18.5.11.1 Data Members . 438
18.5.11.2 Function Members . 438
18.5.11.3 Virtual Functions . 438
18.5.11.4 Virtual Base Classes . 439
18.5.11.5 Anonymous Unions . 439
18.5.11.6 Windows-Specific . 439
18.5.12 Templates . 439
18.5.13 Trigraphs and Digraphs . 440
18.5.14 Const-qualified variables . 440
18.5.15 Long Double . 441
18.5.16 Deprecation Annotation . 441
18.5.17 Noreturn Annotation . 442
18.5.18 [[likely]] / [[unlikely]] Standard Attributes . 442
18.5.19 const and pure GNU Attributes . 442
18.5.20 \_nv\_pure\_\_ Attribute . 443
18.5.21 Intel Host Compiler Specific . 443
18.5.22 C++11 Features . 443
18.5.22.1 Lambda Expressions . 443
18.5.22.2 std::initializer\_list . 445
18.5.22.3 Rvalue references . 445
18.5.22.4 Constexpr functions and function templates . 445
18.5.22.5 Constexpr variables . 446
18.5.22.6 Inline namespaces . 446
18.5.22.7 thread\_local . 448
18.5.22.8 \_\_global\_\_ functions and function templates . 448
18.5.22.9 \_\_managed\_\_ and \_\_shared\_\_ variables . 449
18.5.22.10 Defaulted functions . 449
18.5.23 C++14 Features . 450
18.5.23.1 Functions with deduced return type . 451
18.5.23.2 Variable templates . 452
18.5.24 C++17 Features . 452
18.5.24.1 Inline Variable . 452
18.5.24.2 Structured Binding . 453
18.5.25 C++20 Features . 453

18.5.25.1 Module support . 453
18.5.25.2 Coroutine support . 453
18.5.25.3 Three-way comparison operator . 453
18.5.25.4 Consteval functions . 454
18.6 Polymorphic Function Wrappers . 454
18.7 Extended Lambdas . 457
18.7.1 Extended Lambda Type Traits . 458
18.7.2 Extended Lambda Restrictions . 459
18.7.3 Notes on \_\_host\_\_ \_\_device\_\_ lambdas . 469
18.7.4 \*this Capture By Value . 469
18.7.5 Additional Notes . 472
18.8 Relaxed Constexpr (-expt-relaxed-constexpr) . 472
18.9 Code Samples . 475
18.9.1 Data Aggregation Class . 475
18.9.2 Derived Class . 476
18.9.3 Class Template . 476
18.9.4 Function Template . 477
18.9.5 Functor Class . 477

9 Texture Fetching . 479
19.1 Nearest-Point Sampling . 479
19.2 Linear Filtering . 480
19.3 Table Lookup . 481

20 Compute Capabilities . 483
20.1 Feature Availability . 483
20.1.1 Architecture-Specific Features . 483
20.1.2 Family-Specific Features . 484
20.1.3 Feature Set Compiler Targets . 484
20.2 Features and Technical Specifications . 485
20.3 Floating-Point Standard . 490
20.4 Compute Capability 5.x . 490
20.4.1 Architecture . 490
20.4.2 Global Memory . 491
20.4.3 Shared Memory . 492
20.5 Compute Capability 6.x . 492
20.5.1 Architecture . 492
20.5.2 Global Memory . 495
20.5.3 Shared Memory . 495
20.6 Compute Capability 7.x . 495
20.6.1 Architecture . 495
20.6.2 Independent Thread Scheduling . 496
20.6.3 Global Memory . 498
20.6.4 Shared Memory . 498
20.7 Compute Capability 8.x . 499
20.7.1 Architecture . 499
20.7.2 Global Memory . 500
20.7.3 Shared Memory . 500
20.8 Compute Capability 9.0 . 501
20.8.1 Architecture . 501
20.8.2 Global Memory . 501
20.8.3 Shared Memory . 502
20.8.4 Features Accelerating Specialized Computations . 502
20.9 Compute Capability 10.0 . 502

20.9.1 Architecture 502
20.9.2 Global Memory 503
20.9.3 Shared Memory 503
20.9.4 Features Accelerating Specialized Computations 504
20.10 Compute Capability 12.0 504
20.10.1 Architecture 504
20.10.2 Global Memory 505
20.10.3 Shared Memory 505
20.10.4 Features Accelerating Specialized Computations 505

21 Driver API 507
21.1 Context 509
21.2 Module 510
21.3 Kernel Execution 511
21.4 Interoperability between Runtime and Driver APIs 513
21.5 Driver Entry Point Access 513
21.5.1 Introduction 513
21.5.2 Driver Function Typedefs 514
21.5.3 Driver Function Retrieval 515
21.5.3.1 Using the Driver API 515
21.5.3.2 Using the Runtime API 516
21.5.3.3 Retrieve Per-thread Default Stream Versions 516
21.5.3.4 Access New CUDA features 517
21.5.4 Guidelines for cuGetProcAddress 518
21.5.4.1 Guidelines for Runtime API Usage 518
21.5.5 Determining cuGetProcAddress Failure Reasons 518

22 CUDA Environment Variables 521

23 Error Log Management 531
23.1 Background 531
23.2 Activation 531
23.3 Output 531
23.4 API Description 532
23.5 Limitations and Known Issues 533

24 Unified Memory Programming 535
24.1 Unified Memory Introduction 535
24.1.1 System Requirements for Unified Memory 536
24.1.2 Programming Model 538
24.1.2.1 Allocation APIs for System-Allocated Memory 540
24.1.2.2 Allocation API for CUDA Managed Memory: cudaMallocManaged() 541
24.1.2.3 Global-Scope Managed Variables Using \_\_managed\_\_ 542
24.1.2.4 Difference between Unified Memory and Mapped Memory 543
24.1.2.5 Pointer Attributes 543
24.1.2.6 Runtime detection of Unified Memory Support Level 544
24.1.2.7 GPU Memory Oversubscription 545
24.1.2.8 Performance Hints 545
24.2 Unified memory on devices with full CUDA Unified Memory support 550
24.2.1 System-Allocated Memory: in-depth examples 550
24.2.1.1 File-backed Unified Memory 552
24.2.1.2 Inter-Process Communication (IPC) with Unified Memory 553
24.2.2 Performance Tuning 553
24.2.2.1 Memory Paging and Page Sizes 554
24.2.2.2 Direct Unified Memory Access from host 556

24.2.2.3 Host Native Atomics 558  
24.2.2.4 Atomic accesses & synchronization primitives 558  
24.2.2.5 Memcpy()/Memset() Behavior With Unified Memory 559  
24.3 Unified memory on devices without full CUDA Unified Memory support 559  
24.3.1 Unified memory on devices with only CUDA Managed Memory support 559  
24.3.2 Unified memory on Windows or devices with compute capability 5.x 560  
24.3.2.1 Data Migration and Coherency 560  
24.3.2.2 GPU Memory Oversubscription 560  
24.3.2.3 Multi-GPU 560  
24.3.2.4 Coherency and Concurrency 561  
25 Lazy Loading 569  
25.1 What is Lazy Loading? 569  
25.2 Lazy Loading version support 570  
25.2.1 Driver 570  
25.2.2 Toolkit 570  
25.2.3 Compiler 570  
25.3 Triggering loading of kernels in lazy mode 570  
25.3.1 CUDA Driver API 571  
25.3.2 CUDA Runtime API 571  
25.4 Querying whether Lazy Loading is Turned On 571  
25.5 Possible Issues when Adopting Lazy Loading 572  
25.5.1 Concurrent Execution 572  
25.5.2 Allocators 572  
25.5.3 Autotuning 573  
26 Extended GPU Memory 575  
26.1 Preliminaries 575  
26.1.1 EGM Platforms: System topology 576  
26.1.2 Socket Identifiers: What are they? How to access them? 576  
26.1.3 Allocators and EGM support 576  
26.1.4 Memory management extensions to current APIs 576  
26.2 Using the EGM Interface 577  
26.2.1 Single-Node, Single-GPU 577  
26.2.2 Single-Node, Multi-GPU 577  
26.2.2.1 Using VMM APIs 578  
26.2.2.2 Using CUDA Memory Pool 578  
26.2.3 Multi-Node, Single-GPU 579  
27 Notices 581  
27.1 Notice 581  
27.2 OpenCL 582  
27.3 Trademarks 582

## Chapter 1. Overview

CUDA C++ Programming Guide (Legacy)

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

CUDA is a parallel computing platform and programming model developed by NVIDIA that enables dramatic increases in computing performance by harnessing the power of the GPU. It allows developers to accelerate compute-intensive applications using C, C++, and Fortran, and is widely adopted in fields such as deep learning, scientific computing, and high-performance computing (HPC).

# Chapter 2. What Is the CUDA C Programming Guide?

The CUDA C Programming Guide is the oficial, comprehensive resource that explains how to write programs using the CUDA platform. It provides detailed documentation of the CUDA architecture, programming model, language extensions, and performance guidelines. Whether you’re just getting started or optimizing complex GPU kernels, this guide is an essential reference for efectively leveraging CUDA’s full capabilities.

## Chapter 3. Introduction

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

## 3.1. The Benefits of Using GPUs

The Graphics Processing Unit (GPU)<sup>1</sup> provides much higher instruction throughput and memory bandwidth than the CPU within a similar price and power envelope. Many applications leverage these higher capabilities to run faster on the GPU than on the CPU (see GPU Applications). Other computing devices, like FPGAs, are also very energy eficient, but ofer much less programming flexibility than GPUs.

This diference in capabilities between the GPU and the CPU exists because they are designed with diferent goals in mind. While the CPU is designed to excel at executing a sequence of operations, called a thread, as fast as possible and can execute a few tens of these threads in parallel, the GPU is designed to excel at executing thousands of them in parallel (amortizing the slower single-thread performance to achieve greater throughput).

The GPU is specialized for highly parallel computations and therefore designed such that more transistors are devoted to data processing rather than data caching and flow control. The schematic Figure 1 shows an example distribution of chip resources for a CPU versus a GPU.

Devoting more transistors to data processing, for example, floating-point computations, is beneficial for highly parallel computations; the GPU can hide memory access latencies with computation, instead of relying on large data caches and complex flow control to avoid long memory access latencies, both of which are expensive in terms of transistors.

In general, an application has a mix of parallel parts and sequential parts, so systems are designed with a mix of GPUs and CPUs in order to maximize overall performance. Applications with a high degree of parallelism can exploit this massively parallel nature of the GPU to achieve higher performance than on the CPU.

![](images/6b6f0b2d5e268a5219ab8fefbe55c7fdccfba156660139d34582bffcdd7a126a.jpg)

![](images/f6d2c68196f468a1a2eeb3fcea14076b11e3212d45426df726a86c361c957ccd.jpg)  
Figure 1: The GPU Devotes More Transistors to Data Processing

## 3.2. CUDA®: A General-Purpose Parallel Computing Platform and Programming Model

In November 2006, NVIDIA<sup>®</sup> introduced CUDA<sup>®</sup>, a general purpose parallel computing platform and programming model that leverages the parallel compute engine in NVIDIA GPUs to solve many complex computational problems in a more eficient way than on a CPU.

CUDA comes with a software environment that allows developers to use C++ as a high-level programming language. As illustrated by Figure 2, other languages, application programming interfaces, or directives-based approaches are supported, such as FORTRAN, DirectCompute, OpenACC.

## 3.3. A Scalable Programming Model

The advent of multicore CPUs and manycore GPUs means that mainstream processor chips are now parallel systems. The challenge is to develop application software that transparently scales its parallelism to leverage the increasing number of processor cores, much as 3D graphics applications transparently scale their parallelism to manycore GPUs with widely varying numbers of cores.

The CUDA parallel programming model is designed to overcome this challenge while maintaining a low learning curve for programmers familiar with standard programming languages such as C.

At its core are three key abstractions — a hierarchy of thread groups, shared memories, and barrier synchronization — that are simply exposed to the programmer as a minimal set of language extensions.

These abstractions provide fine-grained data parallelism and thread parallelism, nested within coarsegrained data parallelism and task parallelism. They guide the programmer to partition the problem into coarse sub-problems that can be solved independently in parallel by blocks of threads, and each sub-problem into finer pieces that can be solved cooperatively in parallel by all threads within the block.

![](images/f190407392ede5e45937cc76962b555206d0a61ac301b20e52cb75270fbbb8dd.jpg)  
Figure 2: GPU Computing Applications. CUDA is designed to support various languages and application programming interfaces.

This decomposition preserves language expressivity by allowing threads to cooperate when solving each sub-problem, and at the same time enables automatic scalability. Indeed, each block of threads can be scheduled on any of the available multiprocessors within a GPU, in any order, concurrently or sequentially, so that a compiled CUDA program can execute on any number of multiprocessors as illustrated by Figure 3, and only the runtime system needs to know the physical multiprocessor count.

This scalable programming model allows the GPU architecture to span a wide market range by simply scaling the number of multiprocessors and memory partitions: from the high-performance enthusiast GeForce GPUs and professional Quadro and Tesla computing products to a variety of inexpensive, mainstream GeForce GPUs (see CUDA-Enabled GPUs for a list of all CUDA-enabled GPUs).

![](images/9016fede602b17454ff279ffe9747922b58dd926a1b1305aa1451f087c3a24ed.jpg)  
Figure 3: Automatic Scalability

Note: A GPU is built around an array of Streaming Multiprocessors (SMs) (see Hardware Implementation for more details). A multithreaded program is partitioned into blocks of threads that execute independently from each other, so that a GPU with more multiprocessors will automatically execute the program in less time than a GPU with fewer multiprocessors.

## Chapter 4. Changelog

Table 1: Change Log

<table><tr><td>Version</td><td>Changes</td></tr><tr><td>13.0</td><td>Moved the instruction throughput table from the Performance Guidelines section of the CUDA C++ Programming Guide to the Instruction-optimization section of the CUDA C++ Best Practices Guide. Removed unsupported architectures and corrected entries for integer arithmetic and type conversion.</td></tr><tr><td>12.9</td><td>Added section Error Log Management and CUDA_LOG_FILE to CUDA Environment Variables</td></tr><tr><td>12.8</td><td>Added section TMA Swizzle</td></tr></table>

# Chapter 5. Programming Model

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

This chapter introduces the main concepts behind the CUDA programming model by outlining how they are exposed in C++.

An extensive description of CUDA C++ is given in Programming Interface.

Full code for the vector addition example used in this chapter and the next can be found in the vectorAdd CUDA sample.

## 5.1. Kernels

CUDA C++ extends C++ by allowing the programmer to define C++ functions, called kernels, that, when called, are executed N times in parallel by N diferent CUDA threads, as opposed to only once like regular C++ functions.

A kernel is defined using the \_\_global\_\_ declaration specifier and the number of CUDA threads that execute that kernel for a given kernel call is specified using a new <<<...>>>execution configuration syntax (see Execution Configuration). Each thread that executes the kernel is given a unique thread ID that is accessible within the kernel through built-in variables.

As an illustration, the following sample code, using the built-in variable threadIdx, adds two vectors A and B of size N and stores the result into vector C.

```lisp
// Kernel definition
__global__ void VecAdd(float* A, float* B, float* C)
{
    int i = threadIdx.x;
    C[i] = A[i] + B[i];
}

int main()
{
    ...
    // Kernel invocation with N threads
    VecAdd<<<1, N>>>(A, B, C);
    ...
}
```

Here, each of the N threads that execute VecAdd() performs one pair-wise addition.

## 5.2. Thread Hierarchy

For convenience, threadIdx is a 3-component vector, so that threads can be identified using a onedimensional, two-dimensional, or three-dimensional thread index, forming a one-dimensional, twodimensional, or three-dimensional block of threads, called a thread block. This provides a natural way to invoke computation across the elements in a domain such as a vector, matrix, or volume.

The index of a thread and its thread ID relate to each other in a straightforward way: For a onedimensional block, they are the same; for a two-dimensional block of size (Dx, Dy), the thread ID of a thread of index (x, y) is (x + y Dx); for a three-dimensional block of size (Dx, Dy, Dz), the thread ID of a thread of index (x, y, z) is (x + y Dx + z Dx Dy).

As an example, the following code adds two matrices A and B of size NxN and stores the result into matrix C.

```c
// Kernel definition
__global__ void MatAdd(float A[N][N], float B[N][N],
                       float C[N][N])
{
    int i = threadIdx.x;
    int j = threadIdx.y;
    C[i][j] = A[i][j] + B[i][j];
}

int main()
{
    ...
    // Kernel invocation with one block of N * N * 1 threads
    int numBlocks = 1;
    dim3 threadsPerBlock(N, N);
    MatAdd<<<numBlocks, threadsPerBlock>>>(A, B, C);
    ...
}
```

There is a limit to the number of threads per block, since all threads of a block are expected to reside on the same streaming multiprocessor core and must share the limited memory resources of that core. On current GPUs, a thread block may contain up to 1024 threads.

However, a kernel can be executed by multiple equally-shaped thread blocks, so that the total number of threads is equal to the number of threads per block times the number of blocks.

Blocks are organized into a one-dimensional, two-dimensional, or three-dimensional grid of thread blocks as illustrated by Figure 4. The number of thread blocks in a grid is usually dictated by the size of the data being processed, which typically exceeds the number of processors in the system.

The number of threads per block and the number of blocks per grid specified in the <<<...>>> syntax can be of type int or dim3. Two-dimensional blocks or grids can be specified as in the example above.

Each block within the grid can be identified by a one-dimensional, two-dimensional, or threedimensional unique index accessible within the kernel through the built-in blockIdx variable. The dimension of the thread block is accessible within the kernel through the built-in blockDim variable.

Extending the previous MatAdd() example to handle multiple blocks, the code becomes as follows.

![](images/0be285e9962edca3bf42816b9e1fec14a2fb8cb19634bfcdb35909d0febb2aca.jpg)  
Figure 4: Grid of Thread Blocks

```lisp
// Kernel definition
__global__ void MatAdd(float A[N][N], float B[N][N],
float C[N][N])
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    int j = blockIdx.y * blockDim.y + threadIdx.y;
    if (i < N && j < N)
        C[i][j] = A[i][j] + B[i][j];
}

int main()
{
    ...
    // Kernel invocation
    dim3 threadsPerBlock(16, 16);
    dim3 numBlocks(N / threadsPerBlock.x, N / threadsPerBlock.y);
    MatAdd<<<numBlocks, threadsPerBlock>>>(A, B, C);
    ...
}
```

A thread block size of 16x16 (256 threads), although arbitrary in this case, is a common choice. The grid is created with enough blocks to have one thread per matrix element as before. For simplicity, this example assumes that the number of threads per grid in each dimension is evenly divisible by the number of threads per block in that dimension, although that need not be the case.

Thread blocks are required to execute independently. It must be possible to execute blocks in any order, in parallel or in series. This independence requirement allows thread blocks to be scheduled in any order and across any number of cores as illustrated by Figure 3, enabling programmers to write code that scales with the number of cores.

Threads within a block can cooperate by sharing data through some shared memory and by synchronizing their execution to coordinate memory accesses. More precisely, one can specify synchronization points in the kernel by calling the \_\_syncthreads() intrinsic function; \_\_syncthreads() acts as a barrier at which all threads in the block must wait before any is allowed to proceed. Shared Memory gives an example of using shared memory. In addition to \_\_syncthreads(), the Cooperative Groups API provides a rich set of thread-synchronization primitives.

For eficient cooperation, shared memory is expected to be a low-latency memory near each processor core (much like an L1 cache) and \_\_syncthreads() is expected to be lightweight.

## 5.2.1. Thread Block Clusters

With the introduction of NVIDIA Compute Capability 9.0, the CUDA programming model introduces an optional level of hierarchy called Thread Block Clusters that are made up of thread blocks. Similar to how threads in a thread block are guaranteed to be co-scheduled on a streaming multiprocessor, thread blocks in a cluster are also guaranteed to be co-scheduled on a GPU Processing Cluster (GPC) in the GPU.

Similar to thread blocks, clusters are also organized into a one-dimension, two-dimension, or threedimension grid of thread block clusters as illustrated by Figure 5. The number of thread blocks in a cluster can be user-defined, and a maximum of 8 thread blocks in a cluster is supported as a portable cluster size in CUDA. Note that on GPU hardware or MIG configurations which are too small to support 8 multiprocessors the maximum cluster size will be reduced accordingly. Identification of these smaller configurations, as well as of larger configurations supporting a thread block cluster size beyond 8, is architecture-specific and can be queried using the cudaOccupancyMaxPotentialClusterSize API.

![](images/18a1686bf7842f122d77757b1264f489903200c94690b8704ee93c34a0ad98bc.jpg)  
Figure 5: Grid of Thread Block Clusters

Note: In a kernel launched using cluster support, the gridDim variable still denotes the size in terms of number of thread blocks, for compatibility purposes. The rank of a block in a cluster can be found using the Cluster Group API.

A thread block cluster can be enabled in a kernel either using a compile-time kernel attribute using \_cluster\_dims\_\_(X,Y,Z) or using the CUDA kernel launch API cudaLaunchKernelEx. The example below shows how to launch a cluster using a compile-time kernel attribute. The cluster size using kernel attribute is fixed at compile time and then the kernel can be launched using the classical <<< >>>. If a kernel uses compile-time cluster size, the cluster size cannot be modified when launching the kernel.

```txt
// Kernel definition
// Compile time cluster size 2 in X-dimension and 1 in Y and Z dimension
__global__ void __cluster_dims__(2, 1, 1) cluster_kernel(float *input, float* output)
{
}

int main()
{
```

```cpp
float *input, *output;
    // Kernel invocation with compile time cluster size
    dim3 threadsPerBlock(16, 16);
    dim3 numBlocks(N / threadsPerBlock.x, N / threadsPerBlock.y);

    // The grid dimension is not affected by cluster launch, and is still enumerated
    // using number of blocks.
    // The grid dimension must be a multiple of cluster size.
    cluster_kernel<<<numBlocks, threadsPerBlock>>>(input, output);
}
```

A thread block cluster size can also be set at runtime and the kernel can be launched using the CUDA kernel launch API cudaLaunchKernelEx. The code example below shows how to launch a cluster kernel using the extensible API.

```lisp
// Kernel definition
// No compile time attribute attached to the kernel
__global__ void cluster_kernel(float *input, float* output)
{
}

int main()
{
    float *input, *output;
    dim3 threadsPerBlock(16, 16);
    dim3 numBlocks(N / threadsPerBlock.x, N / threadsPerBlock.y);

    // Kernel invocation with runtime cluster size
    {
        cudaLaunchConfig_t config = {0};
        // The grid dimension is not affected by cluster launch, and is still enumerated
        // using number of blocks.
        // The grid dimension should be a multiple of cluster size.
        config.gridDim = numBlocks;
        config.blockDim = threadsPerBlock;

        cudaLaunchAttribute attribute[1];
        attribute[0].id = cudaLaunchAttributeClusterDimension;
        attribute[0].val.clusterDim.x = 2; // Cluster size in X-dimension
        attribute[0].val.clusterDim.y = 1;
        attribute[0].val.clusterDim.z = 1;
        config.attrs = attribute;
        config.numAttrs = 1;

        cudaLaunchKernelEx(&config, cluster_kernel, input, output);
    }
}
```

In GPUs with compute capability 9.0, all the thread blocks in the cluster are guaranteed to be coscheduled on a single GPU Processing Cluster (GPC) and allow thread blocks in the cluster to perform hardware-supported synchronization using the Cluster Group API cluster.sync(). Cluster group also provides member functions to query cluster group size in terms of number of threads or number of blocks using num\_threads() and num\_blocks() API respectively. The rank of a thread or block in the cluster group can be queried using dim\_threads() and dim\_blocks() API respectively.

Thread blocks that belong to a cluster have access to the Distributed Shared Memory. Thread blocks in a cluster have the ability to read, write, and perform atomics to any address in the distributed shared memory. Distributed Shared Memory gives an example of performing histograms in distributed shared memory.

## 5.2.2. Blocks as Clusters

With \_\_cluster\_dims\_\_, the number of launched clusters is kept implicit and can only be calculated manually.

```lisp
__cluster_dims__((2, 2, 2)) __global__ void foo();

// 8x8x8 clusters each with 2x2x2 thread blocks.
foo<<<dim3(16, 16, 16), dim3(1024, 1, 1)>>();
```

In the above example, the kernel is launched as a grid of 16x16x16 thread blocks, or in fact a grid of 8x8x8 clusters. Alternatively, with another compile-time kernel attribute \_\_block\_size\_\_, one is allowed to launch a grid explicitly configured with the number of thread block clusters.

```txt
// Implementation detail of how many threads per block and blocks per cluster
// is handled as an attribute of the kernel.
__block_size__((1024, 1, 1), (2, 2, 2)) __global__ void foo();

// 8x8x8 clusters.
foo<<<dim3(8, 8, 8)>>();
```

\_block\_size\_\_ requires two fields each being a tuple of 3 elements. The first tuple denotes block dimension and second cluster size. The second tuple is assumed to be (1,1,1) if it’s not passed. To specify the stream, one must pass 1 and 0 as the second and third arguments within <<<>>> and lastly the stream. Passing other values would lead to undefined behavior.

Note that it is illegal for the second tuple of \_\_block\_size\_\_ and \_\_cluster\_dims\_\_ to be specified at the same time. It’s also illegal to use \_\_block\_size\_\_ with an empty \_\_cluster\_dims\_\_. When the second tuple of \_\_block\_size\_\_ is specified, it implies the “Blocks as Clusters” being enabled and the compiler would recognize the first argument inside <<<>>> as the number of clusters instead of thread blocks.

## 5.3. Memory Hierarchy

CUDA threads may access data from multiple memory spaces during their execution as illustrated by Figure 6. Each thread has private local memory. Each thread block has shared memory visible to all threads of the block and with the same lifetime as the block. Thread blocks in a thread block cluster can perform read, write, and atomics operations on each other’s shared memory. All threads have access to the same global memory.

There are also two additional read-only memory spaces accessible by all threads: the constant and texture memory spaces. The global, constant, and texture memory spaces are optimized for diferent memory usages (see Device Memory Accesses). Texture memory also ofers diferent addressing modes, as well as data filtering, for some specific data formats (see Texture and Surface Memory).

The global, constant, and texture memory spaces are persistent across kernel launches by the same application.

![](images/f56179ef6c3f5276d5d206c35260449c97976c5bff3489427fea800dbd89fd64.jpg)  
Figure 6: Memory Hierarchy

## 5.4. Heterogeneous Programming

As illustrated by Figure 7, the CUDA programming model assumes that the CUDA threads execute on a physically separate device that operates as a coprocessor to the host running the C++ program. This is the case, for example, when the kernels execute on a GPU and the rest of the C++ program executes on a CPU.

The CUDA programming model also assumes that both the host and the device maintain their own separate memory spaces in DRAM, referred to as host memory and device memory, respectively. Therefore, a program manages the global, constant, and texture memory spaces visible to kernels through calls to the CUDA runtime (described in Programming Interface). This includes device memory allocation and deallocation as well as data transfer between host and device memory.

Unified Memory provides managed memory to bridge the host and device memory spaces. Managed memory is accessible from all CPUs and GPUs in the system as a single, coherent memory image with a common address space. This capability enables oversubscription of device memory and can greatly simplify the task of porting applications by eliminating the need to explicitly mirror data on host and device. See Unified Memory Programming for an introduction to Unified Memory.

## 5.5. Asynchronous SIMT Programming Model

In the CUDA programming model a thread is the lowest level of abstraction for doing a computation or a memory operation. Starting with devices based on the NVIDIA Ampere GPU Architecture, the CUDA programming model provides acceleration to memory operations via the asynchronous programming model. The asynchronous programming model defines the behavior of asynchronous operations with respect to CUDA threads.

The asynchronous programming model defines the behavior of Asynchronous Barrier for synchronization between CUDA threads. The model also explains and defines how cuda::memcpy\_async can be used to move data asynchronously from global memory while computing in the GPU.

## 5.5.1. Asynchronous Operations

An asynchronous operation is defined as an operation that is initiated by a CUDA thread and is executed asynchronously as-if by another thread. In a well formed program one or more CUDA threads synchronize with the asynchronous operation. The CUDA thread that initiated the asynchronous operation is not required to be among the synchronizing threads.

Such an asynchronous thread (an as-if thread) is always associated with the CUDA thread that initiated the asynchronous operation. An asynchronous operation uses a synchronization object to synchronize the completion of the operation. Such a synchronization object can be explicitly managed by a user (e.g., cuda::memcpy\_async) or implicitly managed within a library (e.g., cooperative\_groups::memcpy\_async).

A synchronization object could be a cuda::barrier or a cuda::pipeline. These objects are explained in detail in Asynchronous Barrier and Asynchronous Data Copies using cuda::pipeline. These synchronization objects can be used at diferent thread scopes. A scope defines the set of threads that may use the synchronization object to synchronize with the asynchronous operation. The following table defines the thread scopes available in CUDA C++ and the threads that can be synchronized with each.

![](images/5755007a4a94054c2f6b20f13648d7ccb76195690a54441356b8050757788bb4.jpg)  
Figure 7: Heterogeneous Programming  
Note: Serial code executes on the host while parallel code executes on the device.

<table><tr><td>Thread Scope</td><td>Description</td></tr><tr><td>cuda::thread_scope::thread_scope_thread</td><td>Only the CUDA thread which initiated asynchronous operations synchronizes.</td></tr><tr><td>cuda::thread_scope::thread_scope_block</td><td>All or any CUDA threads within the same thread block as the initiating thread synchronizes.</td></tr><tr><td>cuda::thread_scope::thread_scope_device</td><td>All or any CUDA threads in the same GPU device as the initiating thread synchronizes.</td></tr><tr><td>cuda::thread_scope::thread_scope_system</td><td>All or any CUDA or CPU threads in the same system as the initiating thread synchronizes.</td></tr></table>

These thread scopes are implemented as extensions to standard C++ in the CUDA Standard C++ library.

## 5.6. Compute Capability

The compute capability of a device is represented by a version number, also sometimes called its “SM version”. This version number identifies the features supported by the GPU hardware and is used by applications at runtime to determine which hardware features and/or instructions are available on the present GPU.

The compute capability comprises a major revision number X and a minor revision number Y and is denoted by X.Y.

The major revision number indicates the core GPU architecture of a device. Devices with the same major revision number share the same fundamental architecture. The table below lists the major revision numbers corresponding to each NVIDIA GPU architecture.

Table 2: GPU Architecture and Major Revision Numbers

<table><tr><td>Major Revision Number</td><td>NVIDIA GPU Architecture</td></tr><tr><td>9</td><td>NVIDIA Hopper GPU Architecture</td></tr><tr><td>8</td><td>NVIDIA Ampere GPU Architecture</td></tr><tr><td>7</td><td>NVIDIA Volta GPU Architecture</td></tr><tr><td>6</td><td>NVIDIA Pascal GPU Architecture</td></tr><tr><td>5</td><td>NVIDIA Maxwell GPU Architecture</td></tr><tr><td>3</td><td>NVIDIA Kepler GPU Architecture</td></tr></table>

The minor revision number corresponds to an incremental improvement to the core architecture, pos-

sibly including new features.

Table 3: Incremental Updates in GPU Architectures

<table><tr><td>Compute Capability</td><td>NVIDIA GPU Architecture</td><td>Based On</td></tr><tr><td>7.5</td><td>NVIDIA Turing GPU Architecture</td><td>NVIDIA Volta GPU Architecture</td></tr></table>

CUDA-Enabled GPUs lists of all CUDA-enabled devices along with their compute capability. Compute Capabilities gives the technical specifications of each compute capability.

Note: The compute capability version of a particular GPU should not be confused with the CUDA version (for example, CUDA 7.5, CUDA 8, CUDA 9), which is the version of the CUDA software platform. The CUDA platform is used by application developers to create applications that run on many generations of GPU architectures, including future GPU architectures yet to be invented. While new versions of the CUDA platform often add native support for a new GPU architecture by supporting the compute capability version of that architecture, new versions of the CUDA platform typically also include software features that are independent of hardware generation.

The Tesla and Fermi architectures are no longer supported starting with CUDA 7.0 and CUDA 9.0, respectively.

# Chapter 6. Programming Interface

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

CUDA C++ provides a simple path for users familiar with the C++ programming language to easily write programs for execution by the device.

It consists of a minimal set of extensions to the C++ language and a runtime library.

The core language extensions have been introduced in Programming Model. They allow programmers to define a kernel as a C++ function and use some new syntax to specify the grid and block dimension each time the function is called. A complete description of all extensions can be found in C++ Language Extensions. Any source file that contains some of these extensions must be compiled with nvcc as outlined in Compilation with NVCC.

The runtime is introduced in CUDA Runtime. It provides C and C++ functions that execute on the host to allocate and deallocate device memory, transfer data between host memory and device memory, manage systems with multiple devices, etc. A complete description of the runtime can be found in the CUDA reference manual.

The runtime is built on top of a lower-level C API, the CUDA driver API, which is also accessible by the application. The driver API provides an additional level of control by exposing lower-level concepts such as CUDA contexts - the analogue of host processes for the device - and CUDA modules - the analogue of dynamically loaded libraries for the device. Most applications do not use the driver API as they do not need this additional level of control and when using the runtime, context and module management are implicit, resulting in more concise code. As the runtime is interoperable with the driver API, most applications that need some driver API features can default to use the runtime API and only use the driver API where needed. The driver API is introduced in Driver API and fully described in the reference manual.

## 6.1. Compilation with NVCC

Kernels can be written using the CUDA instruction set architecture, called PTX, which is described in the PTX reference manual. It is however usually more efective to use a high-level programming language such as C++. In both cases, kernels must be compiled into binary code by nvcc to execute on the device.

nvcc is a compiler driver that simplifies the process of compiling C++ or PTX code: It provides simple and familiar command line options and executes them by invoking the collection of tools that implement the diferent compilation stages. This section gives an overview of nvcc workflow and command options. A complete description can be found in the nvcc user manual.

## 6.1.1. Compilation Workflow

## 6.1.1.1 Ofline Compilation

Source files compiled with nvcc can include a mix of host code (i.e., code that executes on the host) and device code (i.e., code that executes on the device). nvcc’s basic workflow consists in separating device code from host code and then:

▶ compiling the device code into an assembly form (PTX code) and/or binary form (cubin object),

▶ and modifying the host code by replacing the <<<...>>> syntax introduced in Kernels (and described in more details in Execution Configuration) by the necessary CUDA runtime function calls to load and launch each compiled kernel from the PTX code and/or cubin object.

The modified host code is output either as C++ code that is left to be compiled using another tool or as object code directly by letting nvcc invoke the host compiler during the last compilation stage.

Applications can then:

Either link to the compiled host code (this is the most common case),

▶ Or ignore the modified host code (if any) and use the CUDA driver API (see Driver API) to load and execute the PTX code or cubin object.
