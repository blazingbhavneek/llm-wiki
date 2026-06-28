# Programming for CPUs

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

Like other parallel processing hardware (e.g., GPUs), it is important to give the CPU a sufficiently large set of data elements to process. To demonstrate the importance of exploiting multilevel parallelism to handle a large set of data, consider a simple C++ STREAM Triad program, as shown in Figure 16-4.

```c
// C++ STREAM Triad workload
// __restrict is used to denote no memory aliasing among
// arguments
template <typename T>
double triad(T* __restrict VA, T* __restrict VB,
            T* __restrict VC, size_t array_size,
            const T scalar) {
    double ts = timer_start();
    for (size_t id = 0; id < array_size; id++) {
        VC[id] = VA[id] + scalar * VB[id];
    }
    double te = timer_end();
    return (te - ts);
}
```

Figure 16-4. STREAM Triad C++ loop

## A NOTE ABOUT STREAM TRIAD WORKLOAD

The STREAM Triad workload (www.cs.virginia.edu/stream) is an important and popular benchmark workload that CPU vendors use to demonstrate memory bandwidth capabilities. We use the STREAM Triad kernel to demonstrate code generation of a parallel kernel and the way that it is scheduled to achieve significantly improved performance through the techniques described in this chapter. STREAM Triad is a relatively simple workload but is sufficient to show many of the optimizations in an understandable way. There is a STREAM implementation from the University of Bristol, called BabelStream, that includes a C++ with SYCL version.

## Chapter 16 Programming for CPUs

The STREAM Triad loop may be trivially executed on a CPU using a single CPU core for serial execution. A good C++ compiler will perform loop vectorization to generate SIMD code for the CPU that has hardware to exploit instruction-level SIMD parallelism. For example, for an Intel Xeon processor with AVX-512 support, the Intel C++ compiler generates SIMD code as shown in Figure 16-5. Critically, the compiler’s transformation of the code reduced the number of loop iterations by doing more work per loop iteration (using SIMD instructions and loop unrolling).

Figure 16-5. AVX-512 assembly code for STREAM Triad C++ loop

As shown in Figure 16-5, the compiler was able to exploit instructionlevel parallelism in two ways. First is by using SIMD instructions, exploiting instruction-level data parallelism, in which a single instruction can process eight double-precision data elements simultaneously in parallel (per instruction). Second, the compiler applied loop unrolling to get the outof-order execution effect of these instructions that have no dependences between them, based on hardware multiway instruction scheduling.

If we try to execute this function on a CPU, it will probably run well for small array sizes—not great, though, since it does not utilize any multicore or threading capabilities of the CPU. If we try to execute this function with a large array size on a CPU, however, it will likely perform very poorly because the single thread will only utilize a single CPU core and will be bottlenecked when it saturates the memory bandwidth of that core.

## Exploiting Thread-Level Parallelism

To improve the performance of the STREAM Triad kernel, we can compute on a range of data elements that can be processed in parallel, by converting the loop to a parallel\_for kernel.

The body of this STREAM Triad SYCL parallel kernel looks exactly like the body of the STREAM Triad loop that executes in serial C++ on the CPU, as shown in Figure 16-6.

```cpp
constexpr int num_runs = 10;
constexpr size_t scalar = 3;

double triad(const std::vector<float>& vecA,
            const std::vector<float>& vecB,
            std::vector<float>& vecC) {
    assert(vecA.size() == vecB.size() &&
        vecB.size() == vecC.size());
    const size_t array_size = vecA.size();
    double min_time_ns = std::numeric_limits<double>::max();

    queue q{property::queue::enable_profiling{}};
    std::cout << "Running on device: "
           << q.get_device().get_info<info::device::name>()
           << "\n";

    buffer<float> bufA(vecA);
    buffer<float> bufB(vecB);
    buffer<float> bufC(vecC);

    for (int i = 0; i < num_runs; i++) {
        auto Q_event = q.submit([&](handler& h) {
            accessor A{bufA, h};
            accessor B{bufB, h};
            accessor C{bufC, h};

            h.parallel_for(array_size, [=](id<1> idx) {
                C[idx] = A[idx] + B[idx] * scalar;
            });
        });

        double exec_time_ns =
            Q_event.get_profiling_info<
                info::event_profiling::command_end>() -
            Q_event.get_profiling_info<
                info::event_profiling::command_start>();

        std::cout << "Execution time (iteration " << i
            << ") [sec]: "
            << (double)exec_time_ns * 1.0E-9 << "\n";
        min_time_ns = std::min(min_time_ns, exec_time_ns);
    }

    return min_time_ns;
}
```

## Figure 16-6. SYCL STREAM Triad parallel\_for kernel code

Even though the parallel kernel is very similar to the STREAM Triad function written as serial C++ with a loop, it runs much faster because the parallel\_for enables different elements of the array to be processed on multiple cores in parallel. Figure 16-7 shows how this kernel could be mapped to a CPU. Assume that we have a system with one socket, four cores, and two hardware threads per core (for a total of eight threads) and that the implementation processes data in work-groups containing 32 work-items each. If we have 1024 double-precision data elements to be processed, we will have 32 work-groups. The work-group scheduling can be done in a round-robin order, that is, thread-id = work-group-id mod 8. Essentially, each thread will execute four work-groups. Eight work-groups can be executed in parallel for each round. Note that, in this case, the work-group is a set of work-items that is implicitly formed by the SYCL compiler and runtime.

![](images/6d116c28e35cf6d190d735f8db310cbd0f0f9acef1d477f6085f93ce5b108486.jpg)  
Figure 16-7. A mapping of a STREAM Triad parallel kernel

Note that in the SYCL program, the exact way that data elements are partitioned and assigned to different processor cores (or threads) is not specified. This gives a SYCL implementation flexibility to choose how best to execute a parallel kernel on a specific CPU. With that said, an

implementation may provide some level of control to programmers to enable performance tuning (e.g., via compiler options or environment variables).

While a CPU may impose a relatively expensive thread context switch and synchronization overhead, having more software threads resident on a processor core may be beneficial because it gives each processor core a choice of work to execute. If one software thread is waiting for another thread to produce data, the processor core can switch to a different software thread that is ready to run without leaving the processor core idle.

## CHOOSING HOW TO BIND AND SCHEDULE THREADS

Choosing an effective scheme to partition and schedule the work among threads is important to tune an application on CPUs and other device types. Subsequent sections will describe some of the techniques.

## Thread Affinity Insight

Thread affinity designates the CPU cores on which specific threads execute. Performance can suffer if a thread moves around among cores— for instance, if threads do not execute on the same core, cache locality can become an inefficiency if data ping-pongs between different cores.

The DPC++ compiler’s runtime library supports several schemes for binding threads to cores through the environment variables DPCPP\_CPU CU\_AFFINITY, DPCPP\_CPU\_PLACES, DPCPP\_CPU\_NUM\_CUS, and DPCPP\_CPU\_ SCHEDULE, which are not defined by SYCL. Other implementations may expose similar environment variables.

The first of these is the environment variable DPCPP\_CPU\_CU\_

AFFINITY. Tuning using these environment variable controls is simple and low cost but can have large impact for many applications. The description of this environment variable is shown in Figure 16-8.

<table><tr><td>DPCPP_CPU_CU_AFFINITY</td><td>Description</td></tr><tr><td>spread</td><td>Bind successive threads to distinct sockets starting with socket 0 in a round-robin order</td></tr><tr><td>close</td><td>Bind successive threads to distinct hardware threads starting with thread 0 in a round-robin order</td></tr></table>

## Figure 16-8. DPCPP\_CPU\_CU\_AFFINITY environment variable

When the environment variable DPCPP\_CPU\_CU\_AFFINITY is specified, a software thread is bound to a hardware thread through the following formula:

spread: boundHT = ( tid mod numHT ) + (tid mod numSocket) × numHT) close: boundHT = tid mod (numSocket × numHT )

where

• tid denotes a software thread identifier

• boundHT denotes a hardware thread (logical core) that thread tid is bound to

• numHT denotes the number of hardware threads per socket

• numSocket denotes the number of sockets in the system

Assume that we run a program with eight threads on a dual-core dualsocket system—in other words, we have four cores with a total of eight threads to program. Figure 16-9 shows examples of how threads can map to the hardware threads and cores for different DPCPP\_CPU\_CU\_AFFINITY settings.

<table><tr><td rowspan="2">DPCPP_CPU_CU_AFFINITY</td><td colspan="2">socket0</td><td colspan="2">socket1</td></tr><tr><td>core0</td><td>core1</td><td>core2</td><td>core3</td></tr><tr><td>spread</td><td></td><td></td><td></td><td></td></tr><tr><td>close</td><td></td><td></td><td></td><td></td></tr></table>

Figure 16-9. Mapping threads to cores with hardware threads

In conjunction with the environment variable DPCPP\_CPU\_CU\_ AFFINITY, there are other environment variables that support CPU performance tuning:

DPCPP\_CPU\_NUM\_CUS = [n], which sets the number of threads used for kernel execution. Its default value is the number of hardware threads in the system.

DPCPP\_CPU\_PLACES = [ sockets | numa\_domains | cores | threads ], which specifies the places that the affinity will be set similar to OMP\_PLACES in OpenMP 5.1. The default setting is cores.

DPCPP\_CPU\_SCHEDULE = [ dynamic | affinity | static ], which specifies the algorithm for scheduling work-groups. Its default setting is dynamic.

dynamic: Enable the auto\_partitioner, which usually performs sufficient splitting to balance the load among worker threads.

affinity: Enable the affinity\_partitioner, which improves cache affinity and uses proportional splitting when mapping subranges to worker threads.

static: Enable the static\_partitioner, which distributes iterations among worker threads as uniformly as possible.

When running on CPUs using Intel’s OpenCL CPU runtime, workgroup scheduling is handled by the Threading Building Blocks (TBB) library. Using DPCPP\_CPU\_SCHEDULE determines which TBB partitioner is used. Note that the TBB partitioner also uses a grain size to control work splitting, with a default grain size of 1 which indicates that all work-groups can be executed independently. More information can be found at tinyurl.com/oneTBBpart.

A lack of thread affinity tuning does not necessarily mean lower performance. Performance often depends more on how many total threads are executing in parallel than on how well the thread and data are related and bound. Testing the application using benchmarks is one way to be certain whether the thread affinity has a performance impact or not. The STREAM Triad code, as shown in Figure 16-1, started with a lower performance without thread affinity settings. By controlling the affinity setting and using static scheduling of software threads through the environment variables (exports shown in the following for Linux), performance improved:

export DPCPP\_CPU\_PLACES=numa\_domains

export DPCPP\_CPU\_CU\_AFFINITY=close

By using numa\_domains as the places setting for affinity, the TBB task arenas are bound to NUMA nodes or sockets, and the work is uniformly distributed across task arenas. In general, the environment variable DPCPP CPU\_PLACES is recommended to be used together with DPCPP\_CPU\_CU\_ AFFINITY. These environment variable settings help us to achieve a \~30% performance gain on an Intel Xeon server system with 2 sockets, 28 cores per socket, and 2 hardware threads per core, running at 2.5 GHz. However, we can still do better to further improve the performance on this CPU.

## Be Mindful of First Touch to Memory

Memory is stored where it is first touched (used). Since the initialization loop in our example is executed by the host thread serially, all the memory is associated with the socket that the host thread is running on. Subsequent access by other sockets will then access data from memory attached to the initial socket (used for the initialization), which is clearly undesirable for performance. We can achieve a higher performance on the STREAM Triad kernel by parallelizing the initialization loop to control the first touch effect across sockets, as shown in Figure 16-10.

```dart
template <typename T>
void init(queue& deviceQueue, T* VA, T* VB, T* VC,
        size_t array_size) {
  range<1> numOfItems{array_size};

  buffer<T, 1> bufferA(VA, numOfItems);
  buffer<T, 1> bufferB(VB, numOfItems);
  buffer<T, 1> bufferC(VC, numOfItems);

  auto queue_event = deviceQueue.submit([&](handler& cgh) {
    auto aA = bufA.template get_access<sycl_write>(cgh);
    auto aB = bufB.template get_access<sycl_write>(cgh);
    auto aC = bufC.template get_access<sycl_write>(cgh);

    cgh.parallel_for<class Init<T>>(numOfItems, [=](id<1> wi) {
      aA[wi] = 2.0;
      aB[wi] = 1.0;
      aC[wi] = 0.0;
    });
  });

  queue_event.wait();
}
```

Figure 16-10. STREAM Triad parallel initialization kernel to control first touch effects

Exploiting parallelism in the initialization code improves performance of the kernel when run on a CPU. In this instance, we achieve a \~2x performance gain on an Intel Xeon processor system.

The recent sections of this chapter have shown that by exploiting thread-level parallelism, we can utilize CPU cores and threads effectively. However, we need to exploit the SIMD vector-level parallelism in the CPU core hardware as well, to achieve peak performance.

SYCL parallel kernels benefit from thread-level parallelism across cores and hardware threads!

## SIMD Vectorization on CPU

While a well-written SYCL kernel without cross-work-item dependences can run in parallel effectively on a CPU, implementations can also apply vectorization to SYCL kernels to leverage SIMD hardware similar to the GPU support described in Chapter 15. Essentially, CPU processors may optimize memory loads, stores, and operations using SIMD instructions by leveraging the fact that most data elements are often in contiguous memory and take the same control flow paths through a data-parallel kernel. For example, in a kernel with a statement a[i] = a[i] + b[i], each data element executes with the same instruction stream load, load, add, and store by sharing hardware logic among multiple data elements and executing them as a group, which may be mapped naturally onto a hardware’s SIMD instruction set. Specifically, multiple data elements can be processed simultaneously by a single instruction.

The number of data elements that are processed simultaneously by a single instruction is sometimes referred to as the vector length (or SIMD width) of the instruction or processor executing it. In Figure 16-11, our instruction stream runs with four-way SIMD execution.

<table><tr><td colspan="4">Serial execution</td><td>SIMD execution</td></tr><tr><td>work-0</td><td>work-1</td><td>work-2</td><td>work 3</td><td>vector sub-group</td></tr><tr><td>load r0, a[0]</td><td>load r0, a[1]</td><td>load r0, a[2]</td><td>load r0, a[3]</td><td>simdload vr0, a[0...3]</td></tr><tr><td>load r1, b[0]</td><td>load r1, b[1]</td><td>load r1, b[2]</td><td>load r1, b[3]</td><td>simdload vr1, b[0...3]</td></tr><tr><td>add r0, r1</td><td>add r0, r1</td><td>add r0, r1</td><td>add r0, r1</td><td>simdadd vr0, vr1</td></tr><tr><td>store a[0], r0</td><td>store a[1], r0</td><td>store a[2], r0</td><td>store a[3], r0</td><td>simdstore a[0...3], vr0</td></tr></table>

Figure 16-11. Instruction stream for SIMD execution

CPU processors are not the only processors that implement SIMD instruction sets. Other processors such as GPUs implement SIMD instructions to improve efficiency when processing large sets of data. A key difference with Intel Xeon CPU processors, compared with other processor types, is having three fixed-size SIMD register widths 128-bit XMM, 256-bit YMM, and 512-bit ZMM instead of a variable length of SIMD width. When we write SYCL code with SIMD parallelism using sub-group or vector types (see Chapter 11), we need to be mindful of SIMD width and the number of SIMD vector registers in the hardware.

## Ensure SIMD Execution Legality

Semantically, the SYCL execution model ensures that SIMD execution can be applied to any kernel, and a set of work-items in each work-group (i.e., a sub-group) may be executed concurrently using SIMD instructions. Some implementations may instead choose to execute loops within a kernel using SIMD instructions, but this is possible if and only if all original data dependences are preserved, or data dependences are resolved by the compiler based on privatization and reduction semantics. Such implementation would likely report a sub-group size of one.

A single SYCL kernel execution can be transformed from processing a single work-item to a set of work-items using SIMD instructions within the work-group. Under the ND-range model, the fastest-growing (unit-stride) dimension is selected by the compiler vectorizer on which to generate SIMD code. Essentially, to enable vectorization given an ND-range, there should be no cross-work-item dependences between any two work-items in the same sub-group, or the compiler needs to preserve cross-work-item forward dependences in the same sub-group.

When the kernel execution of work-items is mapped to threads on CPUs, fine-grained synchronization is known to be costly, and the thread context switch overhead is high as well. It is therefore an important performance optimization to eliminate dependences between workitems within a work-group when writing a SYCL kernel for CPUs. Another effective approach is to restrict such dependences to the work-items within a sub-group, as shown for the read-before-write dependence in Figure 16-12. If the sub-group is executed under a SIMD execution model, the sub-group barrier in the kernel can be treated by the compiler as a noop, and no real synchronization cost is incurred at runtime.

```txt
const int n = 16, w = 16;

queue q;
range<2> G = {n, w};
range<2> L = {1, w};

int *a = malloc_shared<int>(n * (n + 1), q);

for (int i = 0; i < n; i++)
    for (int j = 0; j < n + 1; j++) a[i * n + j] = i + j;

q.parallel_for(
    nd_range<2>{G, L},
    [=](nd_item<2> it) [[sycl::reqd_sub_group_size(w)]] {
        // distribute uniform "i" over the sub-group with
        // 16-way redundant computation
        const int i = it.get_global_id(0);
        sub_group sg = it.get_sub_group();

        for (int j = sg.get_local_id()[0]; j < n; j += w) {
            // load a[i*n+j+1:16] before updating a[i*n+j:16]
            // to preserve loop-carried forward dependency
            auto va = a[i * n + j + 1];
            group_barrier(sg);
            a[i * n + j] = va + i + 2;
        }
        group_barrier(sg);
    })
    .wait();
```

## Figure 16-12. Using a sub-group to vectorize a loop with a forward dependence

The kernel is vectorized (with a vector length of 8 as an illustration), and its SIMD execution is shown in Figure 16-13. A work-group is formed with a group size of (1, 8), and the loop iterations inside the kernel are distributed over these sub-group work-items and executed with eight-way SIMD parallelism.

![](images/e7ef25c5fd8234288829c60314722097396364f51a993a2cc3055ce0866ea687.jpg)  
Figure 16-13. SIMD vectorization for a loop with a forward dependence

In this example, if the loop in the kernel dominates the performance, allowing SIMD vectorization across the sub-group will result in a significant performance improvement.

The use of SIMD instructions that process data elements in parallel is one way to let the performance of the kernel scale beyond the number of CPU cores and hardware threads.

## SIMD Masking and Cost

In real applications, we can expect conditional statements such as an if statement, conditional expressions such as a = b > a? a: b, loops with a variable number of iterations, switch statements, and so on. Anything that is conditional may lead to scalar control flows not executing the same code paths and just like on a GPU (Chapter 15) can lead to decreased performance. A SIMD mask is a set of bits with the value 1 or 0, which is generated from conditional statements in a kernel. Consider an example with A={1, 2, 3, 4}, B={3, 7, 8, 1} and the comparison expression a < b. The comparison returns a mask with four values {1, 1, 1, 0} that can be stored in a hardware mask register, to dictate which lanes of later SIMD instructions should execute the code that was guarded (enabled) by the comparison.

If a kernel contains conditional code, it is vectorized with masked instructions that are executed based on the mask bits associated with each data element (lane in the SIMD instruction). The mask bit for each data element is the corresponding bit in a mask register.

Using masking may result in lower performance than corresponding non-masked code. This may be caused by

• An additional mask blend operation on each load

• Dependence on the destination

Masking has a cost, so use it only when necessary. When a kernel is an ND-range kernel with explicit groupings of work-items in the execution range, care should be taken when choosing an ND-range work-group size to maximize SIMD efficiency by minimizing masking cost. When a workgroup size is not evenly divisible by a processor’s SIMD width, part of the work-group may execute with masking for the kernel.

Figure 16-14 shows how using merge masking creates a dependence on the destination register:

• With no masking, the processor executes two multiplies (vmulps) per cycle.

With merge masking, the processor executes two multiplies every four cycles as the multiply instruction (vmulps) preserves results in the destination register as shown in Figure 16-17.

Zero masking doesn’t have a dependence on the destination register and therefore can execute two multiplies (vmulps) per cycle.

<table><tr><td>No Masking</td><td>Merge Masking</td><td>Zero Masking</td></tr><tr><td>vmulps zmm0, zmm6, zmm8</td><td>vmulps zmm0{k1}, zmm6, zmm8</td><td>vmulps zmm0{k1}{z}, zmm6, zmm8</td></tr><tr><td>vmulps zmm1, zmm7, zmm8</td><td>vmulps zmm1{k1}, zmm7, zmm8</td><td>vmulps zmm1{k1}{z}, zmm7, zmm8</td></tr><tr><td>Baseline</td><td>Slowdown 4x</td><td>Slowdown 1x</td></tr></table>

Figure 16-14. Three masking code generations for masking in kernel

Accessing cache-aligned data gives better performance than accessing nonaligned data. In many cases, the address is not known at compile time or is known and not aligned. When working with loops, a peeling on memory accesses may be implemented, to process the first few elements using masked accesses, up to the first aligned address, and then to process unmasked accesses followed by a masked remainder, through multiversioning techniques. This method increases code size, but improves data processing overall. When working with parallel kernels, we as programmers can improve performance by employing similar techniques by hand, or by ensuring that allocations are appropriately aligned to improve performance.

## Avoid Array of Struct for SIMD Efficiency

AOS (Array-of-Struct) structures lead to gathers and scatters, which can both impact SIMD efficiency and introduce extra bandwidth and latency for memory accesses. The presence of a hardware gather–scatter mechanism does not eliminate the need for this transformation—gather– scatter accesses commonly need significantly higher bandwidth and latency than contiguous loads. Given an AOS data layout of struct {float x; float y; float z; float w;} a[4], consider a kernel operating on it as shown in Figure 16-15.

```txt
cgh.parallel_for<class aos<T>>(numOfItems,=[](id<1> wi) {
  x[wi] = a[wi].x;   // lead to gather x0, x1, x2, x3
  y[wi] = a[wi].y;   // lead to gather y0, y1, y2, y3
  z[wi] = a[wi].z;   // lead to gather z0, z1, z2, z3
  w[wi] = a[wi].w;   // lead to gather w0, w1, w2, w3
});
```

## Figure 16-15. SIMD gather in a kernel

When the compiler vectorizes the kernel along a set of work-items, it leads to SIMD gather instruction generation due to the need for non-unitstride memory accesses. For example, the stride of a[0].x, a[1].x, a[2].x, and a[3].x is 4, not a more efficient unit-stride of 1.

<table><tr><td> $\mathbf{w}_{3}$ </td><td> $\mathbf{z}_{3}$ </td><td> $\mathbf{y}_{3}$ </td><td> $\mathbf{x}_{3}$ </td><td> $\mathbf{w}_{2}$ </td><td> $\mathbf{z}_{2}$ </td><td> $\mathbf{y}_{2}$ </td><td> $\mathbf{x}_{2}$ </td><td> $\mathbf{w}_{1}$ </td><td> $\mathbf{z}_{1}$ </td><td> $\mathbf{y}_{1}$ </td><td> $\mathbf{x}_{1}$ </td><td> $\mathbf{w}_{0}$ </td><td> $\mathbf{z}_{0}$ </td><td> $\mathbf{y}_{0}$ </td><td> $\mathbf{x}_{0}$ </td></tr></table>

In a kernel, we can often achieve a higher SIMD efficiency by eliminating the use of memory gather–scatter operations. Some code benefits from a data layout change that converts data structures written in an Array-of-Struct (AOS) representation to a Structure-of-Arrays (SOA) representation, that is, having separate arrays for each structure field to keep memory accesses contiguous when SIMD vectorization is performed. For example, consider a SOA data layout of struct {float x[4]; float y[4]; float z[4]; float w[4];} a; as shown here:

<table><tr><td> $\mathbf{w}_{3}$ </td><td> $\mathbf{w}_{2}$ </td><td> $\mathbf{w}_{1}$ </td><td> $\mathbf{w}_{0}$ </td><td> $\mathbf{z}_{3}$ </td><td> $\mathbf{z}_{2}$ </td><td> $\mathbf{z}_{1}$ </td><td> $\mathbf{z}_{0}$ </td><td> $\mathbf{y}_{3}$ </td><td> $\mathbf{y}_{2}$ </td><td> $\mathbf{y}_{1}$ </td><td> $\mathbf{y}_{0}$ </td><td> $\mathbf{x}_{3}$ </td><td> $\mathbf{x}_{2}$ </td><td> $\mathbf{x}_{1}$ </td><td> $\mathbf{x}_{0}$ </td></tr></table>

A kernel can operate on the data with unit-stride (contiguous) vector loads and stores as shown in Figure 16-16, even when vectorized!

## Chapter 16 Programming for CPUs

```javascript
cgh.parallel_for<class aos<T>>(numOfItems, [=](id<1> wi) {
  x[wi] = a.x[wi];  // lead to unit-stride vector load x[0:4]
  y[wi] = a.y[wi];  // lead to unit-stride vector load y[0:4]
  z[wi] = a.z[wi];  // lead to unit-stride vector load z[0:4]
  w[wi] = a.w[wi];  // lead to unit-stride vector load w[0:4]
});
```

## Figure 16-16. SIMD unit-stride vector load in a kernel

The SOA data layout helps prevent gathers when accessing one field of the structure across the array elements and helps the compiler to vectorize kernels over the contiguous array elements associated with work-items. Note that such AOS-to-SOA or AOSOA data layout transformations are expected to be done at the program level (by us) considering all the places where those data structures are used. Doing it at just a loop level will involve costly transformations between the formats before and after the loop. However, we may also rely on the compiler to perform vectorload-and-shuffle optimizations for AOS data layouts with some cost. When a member of SOA (or AOS) data layout has a vector type, compiler vectorization may perform either horizontal expansion or vertical expansion based on underlying hardware to generate optimal code.

## Data Type Impact on SIMD Efficiency

C++ programmers often use integer data types whenever they know that the data fits into a 32-bit signed type, often leading to code such as

```lisp
int id = get_global_id(0); a[id] = b[id] + c[id];
```

However, given that the return type of the get\_global\_id(0) is size\_t (unsigned integer, often 64-bit), the conversion may reduce the optimization that a compiler can legally perform. This can then lead to SIMD gather/scatter instructions when the compiler vectorizes the code in the kernel, for example:

• Read of a[get\_global\_id(0)] may lead to a SIMD unit-stride vector load.

• Read of a[(int)get\_global\_id(0)] may lead to a nonunit-stride gather instruction.

This nuanced situation is introduced by the wraparound behavior (unspecified behavior and/or well-defined wraparound behavior in C++ standards) of data type conversion from size\_t to int (or uint), which is mostly a historical artifact from the evolution of C-based languages. Specifically, overflow across some conversions is undefined behavior, which allows the compiler to assume that such conditions never happen and to optimize more aggressively. Figure 16-17 shows some examples for those wanting to understand the details.

<table><tr><td>get_global_id(0)</td><td>a[(int)get_global_id(0)]</td><td>get_global_id(0)</td><td>a((uint)get_global_id(0)]</td></tr><tr><td>0x7FFFFFFFE</td><td>a[MAX_INT-1]</td><td>0xFFFFFFFE</td><td>a[MAX_UINT-1]</td></tr><tr><td>0x7FFFFFFF</td><td>a[MAX_INT (big positive)]</td><td>0xFFFFFFF</td><td>a[MAX_UINT]</td></tr><tr><td>0x80000000</td><td>a[MIN_INT (big negative)]</td><td>0x100000000</td><td>a[0]</td></tr><tr><td>0x80000001</td><td>a[MIN_INT+1]</td><td>0x100000001</td><td>a[1]</td></tr></table>

Figure 16-17. Examples of integer type value wraparound

SIMD gather/scatter instructions are slower than SIMD unit-stride vector load/store operations. To achieve an optimal SIMD efficiency, avoiding gathers/scatters can be critical for an application regardless of which programming language is used.

Most SYCL get\_\*\_id() family functions have the same detail, although many cases fit within MAX\_INT because the possible return values are bounded (e.g., the maximum id within a work-group). Thus, whenever legal, SYCL compilers can assume unit-stride memory addresses across the chunk of neighboring work-items to avoid gathers/scatters. For cases

that the compiler can’t safely generate linear unit-stride vector memory loads/stores because of possible overflow from the value of global IDs and/ or derivative value from global IDs, the compiler will generate gathers/ scatters.

Under the philosophy of delivering optimal performance for users, the DPC++ compiler assumes no overflow, and captures the reality almost all of the time in practice, so the compiler can generate optimal SIMD code to achieve good performance. However, a compiler option -fnosycl-id-queries-fit-in-int is provided by the DPC++ compiler for us to tell the compiler that there will be an overflow and that vectorized accesses derived from the id queries may not be safe. This can have large performance impact and should be used whenever unsafe to assume no overflow. The key takeaway is that a programmer should ensure the value of global ID fit in 32-bit int. Otherwise, the compiler option -fno-sycl-idqueries-fit-in-int should be used to guarantee program correctness, which may result in a lower performance.

## SIMD Execution Using single\_task

Under a single-task execution model, there are no work-items to vectorize over. Optimizations related to the vector types and functions may be possible, but this will depend on the compiler. The compiler and runtime are given a freedom either to enable explicit SIMD execution or to choose scalar execution within the single\_task kernel, and the result will depend on the compiler implementation.

C++ compilers may map vector types occurring inside of a single\_ task to SIMD instructions when compiling to CPU. The vec load, store, and swizzle functions perform operations directly on vector variables, informing the compiler that data elements are accessing contiguous data starting from the same (uniform) location in memory and enabling us to request optimized loads/stores of contiguous data. As discussed in

Chapter 11, this interpretation of vec is valid—however, we should expect this functionality to be deprecated, eventually, in favor of a more explicit vector type (e.g., std::simd) once available.

```cpp
queue q;

bool *resArray = malloc_shared<bool>(1, q);
resArray[0] = true;

q.single_task([=]) {
    sycl::vec<int, 4> old_v =
        sycl::vec<int, 4>(0, 100, 200, 300);
    sycl::vec<int, 4> new_v = sycl::vec<int, 4>();

    new_v.rgba() = old_v.abgr();
    int vals[] = {300, 200, 100, 0};

    if (new_v.r() != vals[0] || new_v.g() != vals[1] ||
        new_v.b() != vals[2] || new_v.a() != vals[3]) {
        resArray[0] = false;
    }
}).wait();
```

Figure 16-18. Using vector types and swizzle operations in the single\_task kernel

In the example shown in Figure 16-18, under single-task execution, a vector with three data elements is declared. A swizzle operation is performed with old\_v.abgr(). If a CPU provides SIMD hardware instructions for some swizzle operations, we may achieve some performance benefits of using swizzle operations in applications.

## SIMD VECTORIZATION GUIDELINES

CPU processors implement SIM D instruction sets with different SIM D widths. In many cases, this is an implementation detail and is transparent to the application executing kernels on the CPU, as the compiler can determine an efficient group of data elements to process with a specific SIM D size rather than requiring us to use the SIM D instructions explicitly. Sub-groups may be used to more directly express cases where the grouping of data elements should be subject to SIM D execution in kernels.

Given computational complexity, selecting the code and data layouts that are most amenable to vectorization may ultimately result in higher performance. While selecting data structures, try to choose a data layout, alignment, and data width such that the most frequently executed calculation can access memory in a SIM D-friendly manner with maximum parallelism, as described in this chapter.

## Summary

To get the most out of thread-level parallelism and SIMD vector-level parallelism on CPUs, we need to keep the following goals in mind:

• Be familiar with all types of SYCL parallelism and the underlying CPU architectures that we wish to target.

• Exploit the right amount of parallelism—not more and not less—at a thread level that best matches hardware resources. Use vendor tooling, such as analyzers and profilers, to help guide our tuning work to achieve this.

• Be mindful of thread affinity and memory first touch impact on program performance.

Design data structures with a data layout, alignment, and data width such that the most frequently executed calculations can access memory in a SIMD-friendly manner with maximum SIMD parallelism.

• Be mindful of balancing the cost of masking vs. code branches.

• Use a clear programming style that minimizes potential memory aliasing and side effects.

Be aware of the scalability limitations of using vector types and interfaces. If a compiler implementation maps them to hardware SIMD instructions, a fixed vector size may not match the SIMD width of SIMD registers well across multiple generations of CPUs and CPUs from different vendors.

![](images/868235066d8e7e2264449cd4881213e1de8d6a1d21c1d417b7739516fa6b9a0f.jpg)

cc Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
