# CUDA Programming Model

The CUDA parallel programming model is designed to address the challenge of developing application software that transparently scales its parallelism to leverage the increasing number of processor cores in mainstream chips, which are now parallel systems comprising multicore CPUs and manycore GPUs [CUDA_C_Programming_Guide:L795-L797]. The model aims to overcome the complexity of scaling parallelism while maintaining a low learning curve for programmers familiar with standard languages such as C [CUDA_C_Programming_Guide:L795-L797].

## Core Abstractions

At its core, the model exposes three key abstractions to the programmer as a minimal set of language extensions:

1.  **A hierarchy of thread groups**: This structure guides the programmer to partition problems into coarse sub-problems solved independently in parallel by blocks of threads, and further into finer pieces solved cooperatively by all threads within a block [CUDA_C_Programming_Guide:L799-L801].
2.  **Shared memories**: These allow threads within a block to cooperate when solving sub-problems [CUDA_C_Programming_Guide:L799-L801].
3.  **Barrier synchronization**: This ensures coordinated execution among cooperating threads [CUDA_C_Programming_Guide:L799-L801].

These abstractions provide fine-grained data parallelism and thread parallelism, which are nested within coarse-grained data parallelism and task parallelism [CUDA_C_Programming_Guide:L799-L801]. This decomposition preserves language expressivity by allowing threads to cooperate while enabling automatic scalability [CUDA_C_Programming_Guide:L806-L808].

## Scalability and Execution

The CUDA programming model enables automatic scalability by allowing each block of threads to be scheduled on any of the available multiprocessors within a GPU [CUDA_C_Programming_Guide:L806-L808]. Blocks can be scheduled in any order, concurrently or sequentially, meaning a compiled CUDA program can execute on any number of multiprocessors [CUDA_C_Programming_Guide:L806-L808]. The physical multiprocessor count is known only to the runtime system, allowing the software to adapt to the hardware [CUDA_C_Programming_Guide:L806-L808].

This scalable programming model allows the GPU architecture to span a wide market range by simply scaling the number of multiprocessors and memory partitions [CUDA_C_Programming_Guide:L806-L808]. This range includes high-performance enthusiast GeForce GPUs, professional Quadro and Tesla computing products, and inexpensive mainstream GeForce GPUs [CUDA_C_Programming_Guide:L806-L808].

## Implementation

The main concepts behind the CUDA programming model are exposed in C++ through language extensions [CUDA_C_Programming_Guide:L825-L825].
