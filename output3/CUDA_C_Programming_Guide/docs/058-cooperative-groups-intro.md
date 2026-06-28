## Chapter 11. Cooperative Groups

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

## 11.1. Introduction

Cooperative Groups is an extension to the CUDA programming model, introduced in CUDA 9, for organizing groups of communicating threads. Cooperative Groups allows developers to express the granularity at which threads are communicating, helping them to express richer, more eficient parallel decompositions.

Historically, the CUDA programming model has provided a single, simple construct for synchronizing cooperating threads: a barrier across all threads of a thread block, as implemented with the \_\_syncthreads() intrinsic function. However, programmers would like to define and synchronize groups of threads at other granularities to enable greater performance, design flexibility, and software reuse in the form of “collective” group-wide function interfaces. In an efort to express broader patterns of parallel interaction, many performance-oriented programmers have resorted to writing their own ad hoc and unsafe primitives for synchronizing threads within a single warp, or across sets of thread blocks running on a single GPU. Whilst the performance improvements achieved have often been valuable, this has resulted in an ever-growing collection of brittle code that is expensive to write, tune, and maintain over time and across GPU generations. Cooperative Groups addresses this by providing a safe and future-proof mechanism to enable performant code.

## 11.2. What’s New in Cooperative Groups

## 11.2.1. CUDA 13.0

▶ multi\_grid\_group was removed.

## 11.2.2. CUDA 12.2

barrier\_arrive and barrier\_wait member functions were added for grid\_group and thread\_block. Description of the API is available here.

## 11.2.3. CUDA 12.1

▶ invoke\_one and invoke\_one\_broadcast APIs were added.

## 11.2.4. CUDA 12.0

▶ The following experimental APIs are now moved to the main namespace:

▶ asynchronous reduce and scan update added in CUDA 11.7

1 thread\_block\_tile larger than 32 added in CUDA 11.1

It is no longer required to provide memory using the block\_tile\_memory object in order to create these large tiles on Compute Capability 8.0 or higher.

## 11.3. Programming Model Concept

The Cooperative Groups programming model describes synchronization patterns both within and across CUDA thread blocks. It provides both the means for applications to define their own groups of threads, and the interfaces to synchronize them. It also provides new launch APIs that enforce certain restrictions and therefore can guarantee the synchronization will work. These primitives enable new patterns of cooperative parallelism within CUDA, including producer-consumer parallelism, opportunistic parallelism, and global synchronization across the entire Grid.

The Cooperative Groups programming model consists of the following elements:

▶ Data types for representing groups of cooperating threads;

▶ Operations to obtain implicit groups defined by the CUDA launch API (e.g., thread blocks);

▶ Collectives for partitioning existing groups into new groups;

▶ Collective Algorithms for data movement and manipulation (e.g. memcpy\_async, reduce, scan);

▶ An operation to synchronize all threads within the group;

Operations to inspect the group properties;

▶ Collectives that expose low-level, group-specific and often HW accelerated, operations.

The main concept in Cooperative Groups is that of objects naming the set of threads that are part of it. This expression of groups as first-class program objects improves software composition, since collective functions can receive an explicit object representing the group of participating threads. This object also makes programmer intent explicit, which eliminates unsound architectural assumptions that result in brittle code, undesirable restrictions upon compiler optimizations, and better compatibility with new GPU generations.

To write eficient code, its best to use specialized groups (going generic loses a lot of compile time optimizations), and pass these group objects by reference to functions that intend to use these threads in some cooperative fashion.

Cooperative Groups requires CUDA 9.0 or later. To use Cooperative Groups, include the header file:

```c
// Primary header is compatible with pre-C++11, collective algorithm headers require
C++11
#include <cooperative_groups.h>
// Optionally include for memcpy_async() collective
#include <cooperative_groups/memcpy_async.h>
// Optionally include for reduce() collective
#include <cooperative_groups/reduce.h>
// Optionally include for inclusive_scan() and exclusive_scan() collectives
#include <cooperative_groups/scan.h>
```

and use the Cooperative Groups namespace:

```txt
using namespace cooperative_groups;
// Alternatively use an alias to avoid polluting the namespace with collective
← algorithms
namespace cg = cooperative_groups;
```

The code can be compiled in a normal way using nvcc, however if you wish to use memcpy\_async, reduce or scan functionality and your host compiler’s default dialect is not C++11 or higher, then you must add --std=c++11 to the command line.
