# Dynamic Parallelism Glossary

This glossary defines terms used in the context of Dynamic Parallelism within the CUDA C Programming Guide.

## Grid
A Grid is a collection of Threads. Threads in a Grid execute a Kernel Function and are divided into Thread Blocks [CUDA_C_Programming_Guide:L13644-L13679].

## Thread Block
A Thread Block is a group of threads which execute on the same multiprocessor (SM). Threads within a Thread Block have access to shared memory and can be explicitly synchronized [CUDA_C_Programming_Guide:L13644-L13679].

## Kernel Function
A Kernel Function is an implicitly parallel subroutine that executes under the CUDA execution and memory model for every Thread in a Grid [CUDA_C_Programming_Guide:L13644-L13679].

## Host
The Host refers to the execution environment that initially invoked CUDA. Typically the thread running on a system’s CPU processor [CUDA_C_Programming_Guide:L13644-L13679].

## Parent
A Parent Thread, Thread Block, or Grid is one that has launched new grid(s), the Child Grid(s). The Parent is not considered completed until all of its launched Child Grids have also completed [CUDA_C_Programming_Guide:L13644-L13679].

## Child
A Child thread, block, or grid is one that has been launched by a Parent grid. A Child grid must complete before the Parent Thread, Thread Block, or Grid are considered complete [CUDA_C_Programming_Guide:L13644-L13679].

## Thread Block Scope
Objects with Thread Block Scope have the lifetime of a single Thread Block. They only have defined behavior when operated on by Threads in the Thread Block that created the object and are destroyed when the Thread Block that created them is complete [CUDA_C_Programming_Guide:L13644-L13679].

## Device Runtime
The Device Runtime refers to the runtime system and APIs available to enable Kernel Functions to use Dynamic Parallelism [CUDA_C_Programming_Guide:L13644-L13679].
