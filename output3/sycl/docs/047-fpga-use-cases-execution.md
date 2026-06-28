Real programs and algorithms often have control flow (e.g., if/else structures) that leaves some parts of the program inactive a certain percentage of the clock cycles. FPGA compilers typically perform optimizations that allow both sides of a branch to share the same hardware resources when it is possible, to minimize wasted spatial area and to maximize compute efficiency during control flow divergence. This makes control flow divergence much less expensive and less of a development concern than on other, especially vectorized architectures.

## Kernels Consume Chip “Area”

In existing implementations, each kernel in a SYCL application generates a spatial pipeline that consumes some resources of the FPGA (we can think about this as space or area on the device), which is conceptually shown in Figure 17-5.

![](images/fc6cef385dd1c0b0d40733cc550c181ff395a83a7a520d17b81606b175dac2be.jpg)  
Figure 17-5. Multiple kernels in the same FPGA binary: Kernels can run concurrently

Since a kernel uses its own area on the device, different kernels can execute concurrently. If one kernel is waiting for something such as a memory access, other kernels on the FPGA can continue executing because they are independent pipelines elsewhere on the chip. This idea, more formally described as independent forward progress across kernels, is a critical property of FPGA spatial compute.

## When to Use an FPGA

Like any accelerator architecture, predicting when an FPGA is the right choice of accelerator vs. an alternative often comes down to knowledge of the architecture, the application characteristics, and the system bottlenecks. This section describes some of the characteristics of an application to consider.

## Lots and Lots of Work

Like most modern compute accelerators, achieving good performance requires a large amount of work to be performed. If computing a single result from a single element of data, then it may not be useful to leverage an accelerator at all (of any kind). This is no different with FPGAs. Knowing that FPGA compilers leverage pipeline parallelism makes this more apparent. A pipelined implementation of an algorithm has many stages, often thousands or more, each of which should have different work within it in any clock cycle. If there isn’t enough work to occupy most of the pipeline stages most of the time, then efficiency will be low. We’ll call the average utilization of pipeline stages over time occupancy of the pipeline. This is different from the definition of occupancy used when optimizing other architectures such as GPUs!

There are multiple ways to generate work on an FPGA to fill the pipeline stages, which we’ll cover in coming sections.

## Custom Operations or Operation Widths

FPGAs were originally designed to perform efficient integer and bitwise operations and to act as glue logic that could adapt interfaces of other chips to work with each other. Although FPGAs have evolved into computational powerhouses instead of just glue logic solutions, they are still very efficient at bitwise operations, integer math operations on custom data widths or types, and operations on arbitrary bit fields in packet headers, for example.

The fine-grained architecture of an FPGA, described at the end of this chapter, means that novel and arbitrary data types can be efficiently implemented. For example, if we need a 33-bit integer multiplier or a 129-bit adder, FPGAs can provide these custom operations with great efficiency. Because of this flexibility, FPGAs are commonly employed in rapidly evolving domains, such as recently in artificial intelligence, where the data widths and operations have been changing faster than can be built into ASICs.

## Scalar Data Flow

An important aspect of FPGA spatial pipelines, apparent from Figure 17-4, is that the intermediate data between operations not only stays on-chip (is not stored to external memory), but that intermediate data between each pipeline stage has dedicated storage registers. FPGA parallelism often comes primarily from pipelining of computation such that many operations are being executed concurrently, each at a different stage of the pipeline. This results in scalar data flow being the common implementation (under the hood) even in arithmetically intense regions of a program and is fundamentally different from vector architectures where multiple computations are executed as lanes of a shared vector instruction.

The scalar nature of the parallelism in a spatial pipeline is important for many applications because it still applies even with tight data dependences across the units of work. These data dependences can be handled without loss of performance, as we will discuss later in this chapter when talking about loop-carried dependences. The result is that spatial pipelines, and therefore FPGAs, are a compelling architecture to target for algorithms where data dependences across units of work (such as work-items) can’t be broken and fine-grained communication must occur. Many optimization techniques for other accelerators focus on breaking these dependences through various complex approaches or managing communication at controlled scales through features such as sub-groups. FPGAs can instead perform well with communication through tight dependences and should be on your mind when working with classes of algorithms where such patterns exist.

## LOOPS ARE FINE!

A common misconception on data flow architectures is that loops with either fixed or dynamic iteration counts lead to poor data flow performance because they aren’t simple feed-forward pipelines. At least with the Intel

FPGA toolchains, this is not true. Loop iterations can instead be a good way to produce high occupancy within the pipeline, and the compilers are built around the concept of allowing multiple loop iterations to execute in an overlapped way. Loops provide an easy mechanism to keep the pipeline busy with work!

## Low Latency and Rich Connectivity

More conventional uses of FPGAs which take advantage of the rich input and output transceivers on the devices apply equally well for developers using SYCL. For example, as shown in Figure 17-6, some FPGA accelerator cards have network interfaces that make it possible to stream data directly into the device, process it, and then stream the result directly back to the network. Such systems are often sought when processing latency needs to be minimized and where processing through operating system network stacks is too slow or needs to be offloaded to free CPU processing cycles.

![](images/edc6daa9f0cf56efabf7cd88f2add13cb203500a07004a831116f5759fe7283c.jpg)  
Figure 17-6. Low-latency I/O streaming: FPGA connects network data and computation tightly

The opportunities are almost limitless when considering direct input/ output through FPGA transceivers, but the options do come down to what is available on the circuit board that forms an accelerator. Because of the dependence on a specific accelerator card and variety of such uses, aside from describing the pipe language constructs in a coming section, this chapter doesn’t dive into these applications. We should instead read the vendor documentation associated with a specific accelerator card or search for an accelerator card that matches our specific interface needs.

## Customized Memory Systems

Memory systems on an FPGA, such as function private or work-group local memory, are built out of small blocks of on-chip memory. This is important because each memory system is custom built for the specific portion of an algorithm or kernel using it. FPGAs have significant onchip memory bandwidth, and combined with the formation of custom memory systems, they can perform very well on applications that have atypical access patterns and structures. Figure 17-7 shows some of the optimizations that can be performed by the compiler when a memory system is implemented on an FPGA.

![](images/1d7d64836ae8d93e29fdf5a68e8e4cdb4660954dca892cae0197da76bab2ef9b.jpg)  
Figure 17-7. FPGA memory systems are customized by the compiler for our specific code

Other architectures such as GPUs have fixed memory structures that are easy to reason about by experienced developers, but that can also be hard to optimize around in many cases. Many optimizations on other accelerators are focused on memory pattern modification to avoid bank conflicts, for example. If we have algorithms that would benefit from a custom memory structure, such as a different number of access ports per bank or an unusual number of banks, then FPGAs can offer immediate advantages. Conceptually, the difference is between writing code to use a fixed memory system efficiently (most other accelerators) vs. having the memory system custom designed by the compiler to be efficient with our specific code (FPGA).

## Running on an FPGA

There are two steps to run a kernel on an FPGA (as with any ahead-of-time compilation accelerator):

• Compiling the source to a binary which can be run on our hardware of interest

• Selecting the correct accelerator that we are interested in at runtime

To compile kernels so that they can run on FPGA hardware, we can use the command line:

$$
\text {icpx -fsycl -fintelfpga my\_source\_code.cpp -Xshardware}
$$

This command tells the compiler to turn all kernels in my\_source\_ code.cpp into binaries that can run on an Intel FPGA accelerator and then to package them within the host binary that is generated. When we execute the host binary (e.g., by running ./a.out on Linux), the runtime will automatically program any attached FPGA as required, before executing the submitted kernels, as shown in Figure 17-8.

![](images/c1b7d6996740a3fd5a7981843420cd003265de46f3e5623010213002efba8c15.jpg)  
Figure 17-8. FPGA programmed automatically at runtime

FPGA programming binaries are embedded within the compiled DPC++ executable that we run on the host. The FPGA is automatically configured behind the scenes for us.

When we run a host program and submit the first kernel for execution on an FPGA, there might be a slight delay before the kernel begins executing, while the FPGA is programmed. Resubmitting kernels for additional executions won’t see the same delay because the kernel is already programmed to the device and ready to run.

Selection of an FPGA device at runtime was covered in Chapter 2. We need to tell the host program where we want kernels to run because there are typically multiple accelerator options available, such as a CPU and GPU, in addition to the FPGA. To quickly recap one method to select an FPGA during program execution, we can use code like that in Figure 17-9.

```cpp
#include <sycl/ext/intel/fpga_extensions.hpp>  // For fpga_selector_v
#include <sycl/sycl.hpp>
using namespace sycl;

void say_device(const queue& q) {
    std::cout << "Device : "
        << q.get_device().get_info<info::device::name>()
        << "\n";
}

int main() {
    queue q{ext::intel::fpga_selector_v};
    say_device(q);

    q.submit([&](handler& h) {
        h.parallel_for(1024, [=](auto idx) {
            // ...
        });
    });

    return 0;
}
```

Figure 17-9. Choosing an FPGA device at runtime using the fpga\_ selector

## Compile Times

Rumors abound that compiling designs for an FPGA can take a long time, much longer than compiling for ISA-based accelerators. The rumors are true! The end of this chapter overviews the fine-grained architectural elements of an FPGA that lead to both the advantages of an FPGA and the computationally intensive compilation (place-and-route optimizations) that can take hours in some cases.

## Chap ter 17 Programming f or FPGAs

The compile time from source code to FPGA hardware execution is long enough that we don’t want to develop and iterate on our code exclusively in hardware. FPGA development flows offer several stages that minimize the number of hardware compilations, to make us productive despite the hardware compile times. Figure 17-10 shows the typical stages, where most of our time is spent on the early steps that provide fast turnaround and rapid iteration.

![](images/4ac4d4159654dccfbda432e2746046f84cedcc8dd3dfbef31ac17edd58db2cf8.jpg)  
Figure 17-10. Most verification and optimizations occur prior to lengthy hardware compilation

Emulation and static reports from the compiler are the cornerstones of FPGA code development in DPC++. The emulator acts as if it was an FPGA, including supporting relevant extensions and emulating the execution model, but runs on the host processor. Compilation time is therefore the same as we would expect from compilation to a CPU device, although we won’t see the performance boost that we would from execution on actual FPGA hardware. The emulator is great for establishing and testing functional correctness in an application.

Static reports, like emulation, are generated quickly by the toolchain. They report on the FPGA structures created by the compiler and on bottlenecks identified by the compiler. Both of these can be used to predict whether our design will achieve good performance when run on FPGA hardware and are used to optimize our code. Please read the vendor’s documentation for information on the reports, which are often improved from release to release of a toolchain (see documentation for the latest and greatest features!). Extensive documentation is provided by vendors on how to interpret and optimize based on the reports. This information would be the topic of another book, so we can’t dive into details in this single chapter.

## The FPGA Emulator

Emulation is primarily used to functionally debug our application, to make sure that it behaves as expected and produces correct results. There is no reason to do this level of development on actual FPGA hardware where compile times are longer. The emulation flow is activated by removing the -Xshardware flag from the icpx compilation command and at the same time using INTEL::fpga\_emulator\_selector\_v instead of INTEL::fpga\_selector\_v in our host code. We would compile using a command like

icpx -fsycl -fintelfpga my\_source\_code.cpp

By using fpga\_emulator\_selector\_v, which uses the host processor to emulate an FPGA, we maintain a rapid development and debugging process before we have to commit to the lengthier compile for actual FPGA hardware. An example of using INTEL::fpga\_emulator\_selector\_v instead of INTEL::fpga\_selector\_v is shown in Figure 17-11.

## Chap ter 17 Programming f or FPGAs

```cpp
#include <sycl/ext/intel/fpga_extensions.hpp>  // For fpga_selector_v
#include <sycl/sycl.hpp>
using namespace sycl;

void say_device(const queue& q) {
    std::cout << "Device : "
        << q.get_device().get_info<info::device::name>()
        << "\n";
}

int main() {
    queue q{ext::intel::fpga_emulator_selector_v};
    say_device(q);

    q.submit([&](handler& h) {
        h.parallel_for(1024, [=](auto idx) {
            // ...
        });
    });

    return 0;
}
```

Figure 17-11. Using fpga\_emulator\_selector\_v for rapid development and debugging
