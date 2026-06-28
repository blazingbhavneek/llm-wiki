
Kernel programming originally became popular as a way to program GPUs. As kernel programming is generalized, it is important to understand how kernel style of programming affects the mapping of our code to a CPU.

The CPU has evolved over the years. A major shift occurred around 2005 when performance gains from increasing clock speeds diminished. Parallelism arose as the favored solution—instead of increasing clock speeds, CPU producers introduced multicore chips. Computers became more effective in performing multiple tasks at the same time!

While multicore prevailed as the path for increasing hardware performance, realizing that gain in software required nontrivial effort. Multicore processors required developers to come up with different algorithms so the hardware improvements could be noticeable, and this was not always easy. The more cores that we have, the harder it is to keep them busy efficiently. SYCL is one of the programming languages that address these challenges, with many constructs that help to exploit various forms of parallelism on CPUs (and other architectures).

This chapter discusses some particulars of CPU architectures, how CPU hardware typically executes SYCL applications and offers best practices when writing a SYCL code for a CPU platform.

## Performance Caveats

SYCL paves a portable path to parallelize our applications or to develop parallel applications from scratch. The performance of an application, when run on CPUs, is largely dependent upon the following factors:

• The underlying performance of the launch and execution of kernel code

• The percentage of the program that runs in a parallel kernel and its scalability

• CPU utilization, effective data sharing, data locality, and load balancing

• The amount of synchronization and communication between work-items

• The overhead introduced to create, resume, manage, suspend, destroy, and synchronize any threads that work-items execute on, which is impacted by the number of serial-to-parallel or parallel-to-serial transitions

• Memory conflicts caused by shared memory (including falsely shared memory)

• Performance limitations of shared resources such as memory, write combining buffers, and memory bandwidth

In addition, as with any processor type, CPUs may differ from vendor to vendor or even from product generation to product generation. The best practices for one CPU may not be best practices for a different CPU and configuration.

To achieve optimal performance on a CPU, understand as many characteristics of the CPU architecture as possible!

## The Basics of Multicore CPUs

Emergence and rapid advancements in multicore CPUs have driven substantial acceptance of shared memory parallel computing platforms. CPUs offer parallel computing platforms at laptop, desktop, and server levels, making them ubiquitous and exposing performance almost everywhere. The most common form of CPU architecture is cachecoherent non-uniform memory access (cc-NUMA), which is characterized by memory access times not being completely uniform. Many small dualsocket general-purpose CPU systems have this kind of memory system. This architecture has become dominant because the number of cores in a processor, as well as the number of sockets, continues to increase.

In a cc-NUMA CPU system, each socket connects to a subset of the total memory in the system. A cache-coherent interconnect glues all the sockets together and provides a single system memory view for programmers. Such a memory system is scalable, because the aggregate memory bandwidth scales with the number of sockets in the system. The benefit of the interconnect is that an application has transparent access to all the memory in the system, regardless of where the data resides. However, there is a cost: the latency to access data from memory is no longer consistent (i.e., we no longer have fixed access latency). The latency instead depends on where that data is stored in the system. In a good case, data comes from memory directly connected to the socket where code runs. In a bad case, data has to come from a memory connected to a socket far away in the system, and that cost of memory access can increase due to the number of hops in the interconnect between sockets on a cc-NUMA CPU system.

In Figure 16-1, a generic CPU architecture with cc-NUMA memory is shown. This is a simplified system architecture containing cores and memory components found in contemporary, general-purpose, multisocket systems today. Throughout the remainder of this chapter, the figure will be used to illustrate the mapping of corresponding code examples.

To achieve optimal performance, we need to be sure to understand the characteristics of the cc-NUMA configuration of a specific system. For example, recent servers from Intel make use of a mesh interconnect architecture. In this configuration, the cores, caches, and memory controllers are organized into rows and columns. Understanding the connectivity of processors with memory can be critical when working to achieve peak performance of the system.

![](images/55a9beb1271fd394c1d23de801a1aaf72cd7a42f06e9dafc28e40017131aff8a.jpg)  
Figure 16-1. Generic multicore CPU system

The system in Figure 16-1 has two sockets, each of which has two cores with four hardware threads per core. Each core has its own level 1 (L1) cache. L1 caches are connected to a shared last-level cache, which is connected to the memory system on the socket. The memory access latency within a socket is uniform, meaning that it is consistent and can be predicted with accuracy.

The two sockets are connected through a cache-coherent interconnect. Memory is distributed across the system, but all the memory may be transparently accessed from anywhere in the system. The memory read and write latency is non-uniform when accessing memory that isn’t in the socket where the code making the access is running, which means it imposes a potentially much longer and inconsistent latency when accessing data from a remote socket. A critical aspect of the interconnect, though, is coherency. We do not need to worry about inconsistent views of data in memory across the system and can instead focus on the performance impact of how we are accessing the distributed memory system. More advanced optimizations (e.g., atomic operation with a relaxed memory order) can enable operations that no longer require as much hardware memory consistency, but when we want the consistency, the hardware provides it for us.

Hardware threads in CPUs are the execution vehicles. These are the units that execute instruction streams. The hardware threads in Figure 16-1 are numbered consecutively from 0 to 15, which is a notation used to simplify discussions on the examples in this chapter. Unless otherwise noted, all references to a CPU system in this chapter are to the reference cc-NUMA system shown in Figure 16-1.

# The Basics of SIMD Hardware

In 1996, a widely deployed SIMD instruction set was MMX extensions on top of the x86 architecture. Many SIMD instruction set extensions have since followed both on Intel architectures and more broadly across the industry. A CPU core carries out its job by executing instructions, and the specific instructions that a core knows how to execute are defined by the instruction set (e.g., x86, x86\_64, AltiVec, NEON) and instruction set extensions (e.g., SSE, AVX, AVX-512) that it implements. Many of the operations added by instruction set extensions are focused on SIMD.

SIMD instructions allow multiple calculations to be carried out simultaneously on a single core by using registers and hardware bigger than the fundamental unit of data being processed. For example, using 512-bit registers we can perform eight 64-bit calculations with a single machine instruction.

This example shown in Figure 16-2 could, in theory, give us up to an eight times speed-up. In reality, it is likely to be somewhat curtailed as a portion of the eight times speed-up serves to remove one bottleneck and expose the next, such as memory throughput. In general, the performance benefit of using SIMD varies depending on the specific scenario, and in a few cases such as extensive branch divergence, gather/scatter for nonunit-stride memory access, and cache-line split for SIMD loads and stores, it can even perform worse than simpler non-SIMD equivalent code. That said, considerable gains are achievable on today’s processors when we know when and how to apply (or have the compiler apply) SIMD. As with all performance optimizations, programmers should measure the gains on a typical target machine before putting it into production. There are more details on expected performance gains in the following sections of this chapter.

![](images/e80b3950b4855965f0c642d596e1231967f961f5b5538ace689f4a9bc5beb4a2.jpg)  
Figure 16-2. SIMD execution in a CPU hardware thread

The cc-NUMA CPU architecture with SIMD units forms the foundation of a multicore processor, which can exploit a wide spectrum of parallelism starting from instruction-level parallelism in at least the five different ways as shown in Figure 16-3.

![](images/9fdd7f9e27c3d9cd46725522db97dd5d393c32bda993109f12c0fb21e63421de.jpg)  
Figure 16-3. Five ways for executing instructions in parallel

In Figure 16-3, instruction-level parallelism can be achieved through both out-of-order execution of scalar instructions and SIMD parallelism within a single thread. Thread-level parallelism can be achieved through executing multiple threads on the same core or on multiple cores at different scales. More specifically, thread-level parallelism can be exposed from the following:

• Modern CPU architectures allow one core to execute the instructions of two or more threads simultaneously.

Multicore architectures that contain two or more cores within each processor. The operating system perceives each of its execution cores as a discrete processor, with all of the associated execution resources.

Multiprocessing at the processor (chip) level, which can be accomplished by executing separate threads of code. As a result, the processor can have one thread running from an application and another thread running from an operating system, or it can have parallel threads running from within a single application.

Distributed processing, which can be accomplished by executing processes consisting of multiple threads on a cluster of computers, which typically communicate through message passing frameworks.

As multiprocessor computers and multicore technology become more and more common, it is important to use parallel processing techniques as standard practice to increase performance. Later sections of this chapter will introduce the coding methods and performance-tuning techniques within SYCL that allow us to achieve peak performance on multicore CPUs.
