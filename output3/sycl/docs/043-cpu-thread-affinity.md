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
