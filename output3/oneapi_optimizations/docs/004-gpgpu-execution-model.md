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

## Thread Mapping and GPU Occupancy

The SYCL execution model exposes an abstract view of GPU execution. The SYCL thread hierarchy consists of a 1-, 2-, or 3-dimensional grid of work-items. These work-items are grouped into equal sized thread groups called work-groups. Threads in a work-group are further divided into equal sized vector groups called subgroups (see the illustration that follows).

Work-item A work-item represents one of a collection of parallel executions of a kernel.

Sub-group A sub-group represents a short range of consecutive work-items that are processed together as a SIMD vector of length 8, 16, 32, or a multiple of the native vector length of a CPU with Intel<sup>®</sup> UHD Graphics.

Work-group A work-group is a 1-, 2-, or 3-dimensional set of threads within the thread hierarchy. In SYCL, synchronization across work-items is only possible with barriers for the work-items within the same work-group.

## nd\_range

An nd\_range divides the thread hierarchy into 1-, 2-, or 3-dimensional grids of work-groups. It is represented by the global range, the local range of each work-group.

## Thread Hierarchy

![](images/14acddaf2ae319de26714b79e1a70009e3656312d34fa70115cf9e485a53ab76.jpg)  
The diagram above illustrates the relationship among ND-Range, work-group, sub-group, and work-item.

## Thread Synchronization

SYCL provides two synchronization mechanisms that can be called within a kernel function. Both are only defined for work-items within the same work-group. SYCL does not provide any global synchronization mechanism inside a kernel for all work-items across the entire nd\_range.

• \`\`mem\_fence\`\` inserts a memory fence on global and local memory access across all work-items in a work-group.

• \`\`barrier\`\` inserts a memory fence and blocks the execution of all work-items within the work-group until all work-items have reached its location.

## Mapping Work-Groups to $\mathsf { x e } .$ -cores for Maximum Occupancy
