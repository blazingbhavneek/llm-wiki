# sycl Source Lines 6119-6674

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source sycl:L6119-L6674

Citation: [sycl:L6119-L6674]

````text
# Practical Tips

This chapter is home to a number of pieces of useful information, practical tips, advice, and techniques that have proven useful when programming C++ with SYCL. None of these topics are covered exhaustively, so the intent is to raise awareness and encourage learning more as needed.

## Getting the Code Samples and a Compiler

Chapter 1 covers how to get a SYCL compiler (e.g., oneapi.com/ implementations or github.com/intel/llvm) and where to get the code samples used in this book (github.com/Apress/data-parallel-CPP). This is mentioned again to emphasize how useful it can be to try the examples (including making modifications!) to gain hands-on experience. Join those who know what the code in Figure 1-1 actually prints out!

## Online Resources

Key online resources include

• Extensive resources at sycl.tech/

• The official SYCL home at khronos.org/sycl/ with great resources listed at khronos.org/sycl/resources

• Resources to help migrate from CUDA to C++ with SYCL at tinyurl.com/cuda2sycl

• Migration tool GitHub home github.com/oneapi-src/ SYCLomatic

## Platform Model

A C++ compiler with SYCL support is designed to act and feel like any other C++ compiler we have ever used. It is worth understanding the inner workings, at a high level, that enable a compiler with SYCL support to produce code for a host (e.g., CPU) and devices.

The platform model (Figure 13-1) used by SYCL specifies a host that coordinates and controls the compute work that is performed on the devices. Chapter 2 describes how to assign work to devices, and Chapter 4 dives into how to program devices. Chapter 12 describes using the platform model at various levels of specificity.

As we discussed in Chapter 2, there should always be a device to run on in a system using a properly configured SYCL runtime and compatible hardware. This allows device code to be written assuming that at least one device will be available. The choice of the devices on which to run device code is under program control—it is entirely our choice as programmers if, and how, we want to execute code on specific devices (device selection options are discussed in Chapter 12).

![](images/d1f6ee3e487d3795008369992dae71c8e7462d498c3a7597974eeebfa9572210.jpg)  
Figure 13-1. Platform model: can be used abstractly or with specificity

## Multiarchitecture Binaries

Since our goal is to have a single-source code to support a heterogeneous machine, it is only natural to want a single executable file to be the result.

A multiarchitecture binary (a.k.a. a fat binary) is a single binary file that has been expanded to include all the compiled and intermediate code needed for our heterogeneous machine. A multiarchitecture binary acts

like any other a.out or a.exe we are used to—but it contains everything needed for a heterogeneous machine. This helps to automate the process of picking the right code to run for a particular device. As we discuss next, one possible form of the device code in a fat binary is an intermediate format that defers the final creation of device instructions until runtime.

## Compilation Model

The single-source nature of SYCL allows compilations to act and feel like regular C++ compilations. There is no need for us to invoke additional passes for devices or deal with bundling device and host code. That is all handled automatically for us by the compiler. Of course, understanding the details of what is happening can be important for several reasons. This is useful knowledge if we want to target specific architectures more effectively, and it is important to understand if we need to debug a failure happening in the compilation process.

We will review the compilation model so that we are educated for when that knowledge is needed. Since the compilation model supports code that executes on both a host and potentially several devices simultaneously, the commands issued by the compiler, linker, and other supporting tools are more complicated than the C++ compilations we are used to (targeting only one architecture). Welcome to the heterogeneous world!

This heterogeneous complexity is intentionally hidden from us by the compiler and “just works.”

The compiler can generate target-specific executable code similar to traditional C++ compilers (ahead-of-time (AOT) compilation, sometimes referred to as offline kernel compilation), or it can generate an intermediate representation that can be just-in-time (JIT) compiled to a specific target at runtime.

Compilation can be “ahead-of-time” (AOT) or “just-in-time” (JIT ).

The compiler can only compile ahead of time if the device target is known ahead of time (at the time when we compile our program). Using JIT compilation will give more portability for our compiled program but requires the compiler and the runtime to perform additional work while our application is running.

For most devices, including GPUs, the most common practice is to rely on JIT compilation. Some devices (e.g., FPGAs) may have exceptionally slow compilation processes and therefore the practice is to use AOT compilation.

Use JIT unless you know there is a need (e.g., FPGA) or benefit to using AOT code.

By default, when we compile our code for most devices, the output for device code is stored in an intermediate form. At runtime, the device driver on the system will just-in-time compile the intermediate form into code to run on the device(s) to match what is available on the system.

Unlike AOT code, the goal of JIT code is to be able to be compiled at runtime to use whatever device is on a system. This may include devices that did not exist when the program was originally compiled to JIT code.

We can ask the compiler to compile ahead-of-time for specific devices or classes of devices. This has the advantage of saving runtime, but it has the disadvantage of added compile time and fatter binaries! Code that is compiled ahead-of-time is not as portable as just-in-time because it

cannot be adapted to match the available hardware at runtime. We can include both in our binary to get the benefits of both AOT and JIT.

To maximize portability, even when including some AOT code, we like to have JIT code in our binary too.

Compiling for a specific device ahead-of-time also helps us to check at build time that our program should work on that device. With just-in-time compilation, it is possible that a program will fail to compile at runtime (which can be caught using the mechanisms in Chapter 5). There are a few debugging tips for this in the upcoming “Debugging” section of this chapter, and Chapter 5 details how these errors can be caught at runtime to avoid requiring that our applications abort.

Figure 13-2 illustrates a compilation process from source code to fat binary (executable). Whatever combinations we choose are combined into a fat binary. The fat binary is employed by the runtime when the application executes (and it is the binary that we execute on the host!). At times, we may want to compile device code for a particular device in a separate compile. We would want the results of such a separate compilation to eventually be combined into our fat binary. This can be very useful for FPGA development when full compile (doing a full synthesis place-and-route) times can be very long and is in fact a requirement for FPGA development to avoid requiring the synthesis tools to be installed on a runtime system. Figure 13-3 shows the flow of the bundling/unbundling activity supported for such needs. We always have the option to compile everything at once, but during development, the option to break up compilation can be very useful.

Every C++ compiler supporting SYCL has a compilation model with the same goal, but the exact implementation details will vary. The specific diagrams shown here are courtesy of the DPC++ compiler toolchain implementors.

![](images/4f9fa3a2492182b11a7101b8df7affc8ebd26d7c7ed101e081520dbc272d7f75.jpg)  
Figure 13-2. Compilation process: ahead-of-time and just-intime options

![](images/2fec433e9e7e4b4d3cf6c5382913a948634642ca4675a4741ca6672ee85800e8.jpg)  
Figure 13-3. Compilation process: offload bundler/unbundler

## Contexts: Important Things to Know

As mentioned in Chapter 6, a context represents a device or set of devices on which we can execute kernels. We can think of a context as a convenient place for the runtime to stash some state about what it is doing. Programmers are not likely to directly interact with contexts outside of passing them around in most SYCL programs.

Devices can be subdivided into sub-devices. This can be useful for partitioning a problem. Since sub-devices are treated exactly as devices (same C++ type), everything we say about grouping devices applies to subdevices also.

## Chapter 13 Practical Tips

SYCL abstractly considers devices to be grouped together in platforms. Within a platform, devices may be able to interact in ways including sharing memory. Devices belonging to the same context must have the ability to access each other’s global memory using some mechanism. SYCL USM memory (Chapter 6) can be shared between devices only if they are in the same context. USM memory allocations are bound to contexts, not to devices, so a USM allocation within one context is not accessible to other contexts. Therefore, USM allocations are limited to use within a single context—possibly a subset of the device.

Contexts do not abstract what hardware cannot support. For instance, we cannot create a context to include two GPUs which cannot share memory with each other. Not all devices exposed from the same platform are required to be able to be grouped together in the same context.

When we create a queue, we can specify which context we wish to place it within. By default, the DPC++ compiler project implements a default context per platform and automatically assigns new queues to the default context. Other SYCL compilers are free to do the same but are not required to do so by the standard.

## Contexts are expensive to create—having less makes our applications more efficient.

Having all devices from a given platform always be placed in the same context has two advantages: (1) since a context is expensive to create, our application is more efficient; and (2) the maximum sharing supported by the hardware is allowed (e.g., USM).

# Adding SYCL to Existing C++ Programs

Adding the appropriate exploitation of parallelism to an existing C++ program is the first step to using SYCL. If a C++ application is already exploiting parallel execution, that may be a bonus, or it may be a headache. That is because the way we divide the work of an application into parallel execution greatly affects what we can do with it. When programmers talk about refactoring a program parallelism, they are referring to rearranging the flow of execution and data within a program to get it ready to exploit parallelism. This is a complex topic that we will only touch briefly upon. There is no one-size-fits-all answer on how to prepare an application for parallelism, but there are some tips worth noting.

When adding parallelism to a C++ application, an easy approach to consider is to find an isolated point in the program where the opportunity for parallelism is the greatest. We can start our modification there and then continue to add parallelism in other areas as needed. A complicating factor is that refactoring (i.e., rearranging the program flow and redesigning data structures) may improve the opportunity for parallelism.

Once we find an isolated point in the program where the opportunity for parallelism is the greatest, we will need to consider how to use SYCL at that point in the program. That is what the rest of the book teaches.

At a high level, the key steps for introducing parallelism consist of the following:

1. Safety with concurrency (commonly called thread safety in conventional CPU programming): Adjusting the usage of all shared mutable data (data that can change and may be acted upon concurrently) to prevent data races. See Chapter 19.

2. Introducing concurrency and/or parallelism.

3. Tuning for parallelism (best scaling, optimizing for throughput or latency).

It is important to consider step #1 first. Many applications have already been refactored for concurrency, but many have not. With SYCL as the sole source of parallelism, we focus on safety for the data being used within kernels and possibly shared with the host. If we have other techniques in our program (OpenMP, MPI, TBB, etc.) that introduce parallelism, that is an additional concern on top of our SYCL programming. It is important to note that it is okay to use multiple techniques inside a single program— SYCL does not need to be the only source of parallelism within a program. This book does not cover the advanced topic of mixing with other parallelism techniques.

## Considerations When Using Multiple Compilers

C++ compilers that support SYCL also support linking with object code (libraries, object files, etc.) from other C++ compilers. In general, any issues that arise from using multiple compilers are the same as for any C++ compiler, requiring consideration of name mangling, targeting the same standard libraries, aligning calling conventions, etc. These are the same issues we must deal with when mixing and matching compilers for other languages such as Fortran or C.

In addition, applications must use the SYCL runtime that comes with the compiler used to build programs. It is not safe to mix and match SYCL compilers and SYCL runtimes—different runtimes may have different implementations and data layouts for important SYCL objects.

SYCL interoperability with non-SYCL source languages refers to the ability of SYCL to work with kernel functions or device functions that are written in other programming languages, such as OpenCL, C, or CUDA, or to consume code in an intermediate representation precompiled by another compiler. Refer to Chapter 20 for more information about interoperability with non-­SYCL source languages.

Finally, the same compiler toolchain that was used for compiling SYCL device code is also required to do the linking phase of our compilation. Using a linker from a different compiler toolchain to do the linking will not result in a functional program as compilers that are not SYCL-aware will not know how to properly integrate host and device code.

## Debugging

This section conveys some modest debugging advice, to ease the challenges unique to debugging a parallel program, especially one targeting a heterogeneous machine.

We should never forget that we have the option to debug our applications while they are running on a CPU device. This debugging tip is described as Method#2 in Chapter 2. Because the architectures of devices often include fewer debugging hooks than general-purpose CPUs, tools can often probe code on a CPU more precisely. An important difference when running everything on a CPU is that many errors relating to synchronization will disappear, including moving memory back and forth between the host and devices. While we eventually need to debug all such errors, this can allow incremental debugging so we can resolve some bugs before others. Experience will show that running on the device we are targeting as often as possible is important, as is leveraging portability to the CPU (and other devices) as part of the debugging process—running multiple devices will help expose issues and can help isolate whether a bug we encounter is device-specific.

## Debugging tip R unning on a CPU is a powerful debugging tool.

Parallel programming errors, specifically data races and deadlocks, are generally easier for tools to detect and eliminate when running all code on the host. Much to our chagrin, we will most often see program failures from such parallel programming errors when running on a combination of host and devices. When such issues strike, it is very useful to remember that pulling back to CPU-only is a powerful debugging tool. Thankfully, SYCL is carefully designed to keep this option available to us and easy to access.

Debugging tip I f a program is deadlocking, check that the host accessors are being destroyed properly and that work-items in kernels are obeying the synchronization rules from the SYCL specification.

The following compiler options are a good idea when we start debugging:

• -g: Put debug information in the output

• -ferror-limit=1: Maintain sanity when using C++ with template libraries such as those heavily used by SYCL

-Werror -Wall -Wpedantic: Have the compiler enforce good coding to help avoid producing incorrect code to debug at runtime

We really do not need to get bogged down fixing pedantic warnings just to use C++ with SYCL, so choosing to not use -Wpedantic is understandable.

When we leave our code to be compiled just-in-time during runtime, there is code we can inspect. This is highly dependent on the layers used by our compiler, so looking at the compiler documentation for suggestions is a good idea.

## Debugging Deadlock and Other Synchronization Issues

Parallel programming relies on the proper coordination between our work that happens in parallel. Data usage needs to be gated by when the data is ready for use—such data dependencies need to be encoded in the logic of our program for proper behavior.

Debugging dependency issues, especially with USM, can be a challenge when an error in our synchronization/dependency logic occurs. We may see a program hang (never complete) or generate erroneous information intermittently. In such cases, we may see behavior such as “it fails until I run it in the debugger—then it works perfectly!” Such intermittent failures often stem from dependencies which are not properly synchronized via waits, locks, explicit dependencies between queue submission, etc.

Useful debugging techniques include

• Switching from out-of-order to in-order queues

• Sprinkle queue.wait() calls around

Using either, or both, of these while debugging can help to identify where dependency information may be missing. If such change makes program failures change or disappear, it is a strong hint that we have an issue to correct in our synchronization/dependency logic. Once fixed, we remove these temporary debugging measures.

## Debugging Kernel Code

While debugging kernel code, start by running on a CPU device (as advised in Chapter 2). The code for device selectors in Chapter 2 can easily be modified to accept runtime options, or compiler-time options, to redirect work to the host device when we are debugging.

When debugging kernel code, SYCL defines a C++-style stream that can be used within a kernel (Figure 13-4). The DPC++ compiler also offers an experimental implementation of a C-style printf that has useful capabilities, with some restrictions.

```cpp
q.submit([&](handler &h) {
  stream out(1024, 256, h);
  h.parallel_for(range{8}, [=](id<1> idx) {
    out << "Testing my sycl stream (this is work-item ID:"
          << idx << "\)\n";
  });
});

Figure 13-4. sycl::stream
```

When debugging kernel code, experience encourages that we put breakpoints before parallel\_for or inside parallel\_for, but not actually on the parallel\_for. A breakpoint placed on a parallel\_for can trigger a breakpoint multiple times even after performing the next operation. This C++ debugging advice applies to many template expansions like those in SYCL, where a breakpoint on the template call will translate into a complicated set of breakpoints when it is expanded by the compiler. There may be ways that implementations can ease this, but the key point here is that we can avoid some confusion on all implementations by not setting the breakpoint precisely on the parallel\_for itself.

## Debugging Runtime Failures

When a runtime error occurs while compiling just-in-time, we are either dealing with a case where we used a feature explicitly that the available hardware cannot support (e.g., fp16 or simd8), a compiler/runtime bug, or we have accidentally programmed nonsense that was not detected until it tripped up the runtime and created difficult-to-understand runtime error messages. In all three cases, it can be a bit intimidating to dive into these bugs. Thankfully, even a cursory look may allow us to get a better idea of what caused a particular issue. It might yield some additional knowledge that will guide us to avoid the issue, or it may just help us submit a short bug report to the compiler team. Either way, knowing that some tools exist to help can be important.

Output from our program that indicates a runtime failure may look like these examples:

terminate called after throwing an instance of 'sycl::\_ V1::runtime\_error'

what(): Native API failed. Native API returns: ...

or

terminate called after throwing an instance of 'sycl::\_

V1::compile\_program\_error

what(): The program was built for 1 devices error: Kernel compiled with required subgroup size 8, which is unsupported on this platform

in kernel: 'typeinfo name for main::'lambda'(sycl::\_V1::nd\_ item<2>)'

error: backend compiler failed build.

-11 (PI\_ERROR\_BUILD\_PROGRAM\_FAILURE)

Seeing such exceptions here lets us know that our host program could have been constructed to catch this error. The first shows a bit of a catchall error for accessing any API that is not supported natively (in this case it was using a host side memory allocation not supported on the platform); the second is easier to realize that SIMD8 was specified for a device that did not support it (in this case it supported SIMD16 instead). Runtime compiler failures do not need to abort our application; we could catch them, or code to avoid them, or both. Chapter 5 dives into this topic.

When we see a runtime failure and have any difficulty debugging it quickly, it is worth simply trying a rebuild using ahead-of-time compilations. If the device we are targeting has an ahead-of-time compilation option, this can be an easy thing to try that may yield easierto-understand diagnostics. If our errors can be seen at compile time instead of JIT or runtime, often much more useful information will be found in the error messages from the compiler instead of the small amount of error information we usually see from a JIT or the runtime.

Figure 13-5 lists two of the flags and additional environment variables (supported on Windows and Linux) supported by compilers or runtimes to aid in advanced debugging. These are DPC++ compiler–specific advanced debug options that exist to inspect and control the compilation model. They are not discussed or utilized in this book; they are explained in detail online with the GitHub project at intel.github.io/llvm-docs EnvironmentVariables.html and tinyurl.com/IGCoptions.

<table><tr><td>Environment variables</td><td>Value</td><td>description</td></tr><tr><td>ONEAPI_DEVICE_SELECTOR</td><td>See online documentation for examples of the numerous options in the documents at intel.github.io.</td><td>Can be used to limit the choice of devices available when a SYCL-using application is run. Useful for limiting devices to a certain type (like GPUs or accelerators) or backends (like Level Zero or OpenCL).</td></tr><tr><td>SYCL_PI_TRACE</td><td>1 (basic),2 (advanced),-1 (all)</td><td>Runtime: Value of 1 enables tracing of Runtime Plugin Interface (PI) for plugin and device discovery; Value of 2 enables tracing of all PI calls. Value of -1 unleashes all levels of tracing.</td></tr><tr><td>SYCL_PRINT_EXECUTION_GRAPH</td><td>always(or ask to dump only select files by specifying:before_addCG,after_addCG, before_addCopyBack, after_addCopyBack, before_addHostAcc, or after_addHostAcc)</td><td>Runtime: create text files (with DOT extension) tracing the execution graph. Relatively easy to browse traces of what is happening during runtime.</td></tr><tr><td>IGC_ShaderDumpEnable</td><td>0 or 1</td><td>Linux only. Runtime: ask the Intel Graphics Compiler (JIT) to dump some information.</td></tr><tr><td>IGC_ShaderDumpEnableAll</td><td>0 or 1</td><td>Linux only. Runtime: ask the Intel Graphics Compiler (JIT) to dump lots of information.</td></tr></table>

## Figure 13-5. DPC++ compiler advanced debug options

These options are not described more within this book, but they are mentioned here to open up this avenue of advanced debugging as needed. These options may give us insight into how to work around an issue or bug. It is possible that our source code is inadvertently triggering an issue that can be resolved by correcting the source code. Otherwise, the use of these options is for very advanced debugging of the compiler itself. Therefore, they are associated more with compiler developers than with users of the compiler. Some advanced users find these options useful; therefore, they are mentioned here and never again in this book. To dig deeper, see DPC++ compiler GitHub project intel.github.io/llvm-docs/ EnvironmentVariables.html.

Debugging tip When other options are exhausted and we need to debug a runtime issue, we look for dump tools that might give us hints toward the cause.

## Queue Profiling and Resulting Timing Capabilities

Many devices support queue profiling (device::has(aspect::queue\_ profiling)—for more on aspects in general, see Chapter 12. A simple and powerful interface makes it easy to access detailed timing information on queue submission, actual start of execution on the device, completion on the device, and completion of the command. This profiling will be more precise about the device timings than using host timing mechanisms (e.g., chrono) because they will generally not include host to/from device data transfer times. See the examples shown in Figure 13-6 and Figure 13-7 with sample outputs shown in Figure 13-8. The samples outputs shown in Figure 13-8 illustrate what is possible with this technique but have not been optimized and should not be used as representations of the merits of any particular system choice in any manner.

The aspect::queue\_profiling aspect indicates that the device supports queue profiling via property::queue::enable\_profiling. For such devices, we can specify property::queue::enable\_profiling when constructing a queue—a property list is an optional final parameter to the queue constructor. Doing so activates the SYCL runtime captures of profiling information for the command groups that are submitted to that queue. The captured information is then made available via the SYCL event class get\_profiling\_info member function. If the queue’s associated device does not have aspect::queue\_profiling, this will cause the constructor to throw a synchronous exception with the errc::feature\_not\_supported error code.

An event can be queried for profiling information using the get\_ profiling\_info member function of the event class, specifying one of the profiling info parameters enumerated in info::event\_profiling. The possible values for each info parameter and any restrictions are defined in the specification of the SYCL backend associated with the event. All info parameters in info::event\_profiling are specified in SYCL specification’s table entitled “Profiling information descriptors for the SYCL event class,” and the synopsis for info::event\_profiling is described in an Appendix of the specification under “Event information descriptors.” Each profiling descriptor returns a timestamp that represents the number of nanoseconds that have elapsed since some implementationdefined time base. All events that share the same backend are guaranteed to share the same time base; therefore, the difference between two timestamps from the same backend yields the number of nanoseconds that have elapsed between those events. As a final note, we do caution that enabling event profiling does increase overhead, so the best practice is to enable it during development or tuning and then to disable for production.

## Tip Due to slight overhead, enable queue profiling only during development or tuning—disable for production.

```cpp
CHAPTER 13 PRACTICAL TIPS

#include <iostream>
#include <sycl/sycl.hpp>
using namespace sycl;

// Array type and data size for this example.
constexpr size_t array_size = (1 << 16);
typedef std::array<int, array_size> IntArray;
// Define VectorAdd (see Figure 13-7)

void InitializeArray(IntArray &a) {
    for (size_t i = 0; i < a.size(); i++) a[i] = i;
}

int main() {
    IntArray a, b, sum;
    InitializeArray(a);
    InitializeArray(b);

    queue q(property::queue::enable_profiling{});

    std::cout << "Vector size: " << a.size()
        << "\nRunning on device: "
        << q.get_device().get_info<info::device::name>()
        << "\n";

    VectorAdd(q, a, b, sum);

    return 0;
}
```

Figure 13-6. Setting up to use queue profiling

```cpp
void VectorAdd(queue &q, const IntArray &a,
            const IntArray &b, IntArray &sum) {
    range<1> num_items{a.size Little};
    buffer a_buf(a), b_buf(b);
    buffer sum_buf(sum.data(), num_items);
    auto t1 =
        std::chrono::steady_clock::now();  // Start timing

    event e = q.submit([&](handler &h) {
        auto a_acc = a_buf.get_access<access::mode::read>(h);
        auto b_acc = b_buf.get_access<access::mode::read>(h);
        auto sum_acc =
            sum_buf.get_access<access::mode::write>(h);

        h.parallel_for(num_items, [=](id<1> i) {
            sum_acc[i] = a_acc[i] + b_acc[i];
        });
    });
    q.wait();

    double timeA =
        (e.template get_profiling_info<
            info::event_profiling::command_end>() -
        e.template get_profiling_info<
            info::event_profiling::command_start>());
    }

    auto t2 =
        std::chrono::steady_clock::now();  // Stop timing

    double timeB = (std::chrono::duration_cast<
                    std::chrono::microseconds>(t2 - t1)
                    .count());

    std::cout
        << "profiling: Vector add completed on device in "
        << timeA << " nanoseconds\n";
    std::cout << "chrono: Vector add completed on device in "
                << timeB * 1000 << " nanoseconds\n";
    std::cout << "chrono more than profiling by "
                << (timeB * 1000 - timeA) << " nanoseconds\n";
}
```

## Figure 13-7. Using queue profiling

## Chapter 13 Practical Tips

```txt
Vector size: 65536
Running on device: Intel(R) UHD Graphics P630 [0x3e96]
profiling: Vector add completed on device in 57602 nanoseconds
chrono: Vector add completed on device in 2.85489e+08 nanoseconds
chrono more than profiling by 2.85431e+08 nanoseconds

Vector size: 65536
Running on device: NVIDIA GeForce RTX 3060
profiling: Vector add completed on device in 17410 nanoseconds
chrono: Vector add completed on device in 3.6071e+07 nanoseconds
chrono more than profiling by 3.60536e+07 nanoseconds

Vector size: 65536
Running on device: Intel(R) Data Center GPU Max 1100
profiling: Vector add completed on device in 9440 nanoseconds
chrono: Vector add completed on device in 5.6976e+07 nanoseconds
chrono more than profiling by 5.69666e+07 nanoseconds
```

Figure 13-8. Three sample outputs from queue profiling example

## Tracing and Profiling Tools Interfaces

Tracing and profiling tools can help us understand our runtime behaviors in our application, and often shed light on opportunities to improve our algorithms. Insights are often portable, in that they can be generalized to a wide class of devices, so we recommend using whatever tracing and profiling tools you find most valuable on whatever platform you prefer. Of course, fine-tuning any platform can require being on the exact platform in question. For maximally portable applications, we encourage first looking for opportunities to tune with an eye toward making any adjustments as portable as possible.

When our SYCL programs are running on top of an OpenCL runtime and using the OpenCL backend, we can run our programs with the OpenCL Intercept Layer: github.com/intel/opencl-intercept-layer. This is a tool that can inspect, log, and modify OpenCL commands that an application (or higher-level runtime) is generating. It supports a lot of controls, but good ones to set initially are ErrorLogging, BuildLogging, and maybe CallLogging (though it generates a lot of output). Useful

dumps are possible with DumpProgramSPIRV. The OpenCL Intercept Layer is a separate utility and is not part of any specific OpenCL implementation, so it works with many SYCL compilers.

There are a number of additional excellent tools for collecting performance data that are popular for SYCL developers. They are open source (github.com/intel/pti-gpu) along with samples to help to get us started.

Two of the most popular tools are as follows:

onetrace: Host and device tracing tool for OpenCL and Level Zero backends with support of DPC++ (both for CPU and GPU) and OpenMP GPU offload

• oneprof: GPU HW metrics collection tool for OpenCL and Level Zero backends with support of DPC++ and OpenMP\* GPU offload

Both tools use information from instrumented runtimes, so they apply to GPUs and CPUs. SYCL, ISPC, and OpenMP support in compilers that use these runtimes can all benefit from these tools. Consult the websites for the tools to explore their applicability for your usage. In general, we can find a platform that is supported and use the tools to learn useful information about your program even if every platform we target is not supported. Much of what we learn about a program is useful everywhere.

## Initializing Data and Accessing Kernel Outputs

In this section, we dive into a topic that causes confusion for new users of SYCL and that leads to the most common (in our experience) first bugs that we encounter as new SYCL developers.

## Chapter 13 Practical Tips

Put simply, when we create a buffer from a host memory allocation (e.g., array or vector), we can’t access the host allocation directly until the buffer has been destroyed. The buffer owns any host allocation passed to it at construction time, for the buffer’s entire lifetime. There are rarely used mechanisms that do let us access the host allocation while a buffer is still alive (e.g., buffer mutex), but those advanced features don’t help with the early bugs described here.

## EVERYONE MAKES THIS ERROR—KNOWING THAT CAN HELP US DEBUG IT QUICKLY RATHER THAN PUZZLE OVER IT A LONG TIME!!!

If we construct a buffer from a host memory allocation, we must not directly access the host allocation until the buffer has been destroyed! While it is alive, the buffer owns the allocation. Understand buffer scope—and rules inside the scope!

A common bug appears when the host program accesses a host allocation while a buffer still owns that allocation. All bets are off once this happens because we don’t know what the buffer is using the allocation for. Don’t be surprised if the data is incorrect—the kernels that we’re trying to read the output from may not have even started running yet! As described in Chapters 3 and 8, SYCL is built around an asynchronous task graph mechanism. Before we try to use output data from task graph operations, we need to be sure that we have reached synchronization points in the code where the graph has executed and made data available to the host. Both buffer destruction and creation of host accessors are operations that cause this synchronization.

Figure 13-9 shows a common pattern of code that we often write, where we cause a buffer to be destroyed by closing the block scope within which it was defined. By causing the buffer to go out of scope and be destroyed, we can then safely read kernel results through the original host allocation that was passed to the buffer constructor.

```cpp
constexpr size_t N = 1024;

// Set up queue on any available device
queue q;

// Create host containers to initialize on the host
std::vector<int> in_vec(N), out_vec(N);

// Initialize input and output vectors
for (int i = 0; i < N; i++) in_vec[i] = i;
std::fill(out_vec.begin(), out_vec.end(), 0);

// Nuance: Create new scope so that we can easily cause
// buffers to go out of scope and be destroyed
{
    // Create buffers using host allocations (vector in this
    // case)
    buffer in_buf{in_vec}, out_buf{out_vec};

    // Submit the kernel to the queue
    q.submit([&](handler& h) {
        accessor in{in_buf, h};
        accessor out{out_buf, h};

        h.parallel_for(
            range{N}, [=](id<1> idx) { out[idx] = in[idx]; });
    });

    // Close the scope that buffer is alive within! Causes
    // buffer destruction which will wait until the kernels
    // writing to buffers have completed, and will copy the
    // data from written buffers back to host allocations
    // (our std::vectors in this case). After the buffer
    // destructor runs, caused by this closing of scope,
    // then it is safe to access the original in_vec and
    // out_vec again!
}

// Check that all outputs match expected value
// WARNING: The buffer destructor must have run for us to
// safely use in_vec and out_vec again in our host code.
// While the buffer is alive it owns those allocations,
// and they are not safe for us to use! At the least they
// will contain values that are not up to date. This code
// is safe and correct because the closing of scope above
// has caused the buffer to be destroyed before this point
// where we use the vectors again.
for (int i = 0; i < N; i++)
    std::cout << "out_vec[" << i << "]=" << out_vec[i]
        << "\n";
```

## Figure 13-9. Common pattern: buffer creation from a host allocation

There are two common reasons to associate a buffer with existing host memory like Figure 13-9:

1. To simplify initialization of data in a buffer. We can just construct the buffer from host memory that we (or another part of the application) have already initialized.

2. To reduce the characters typed because closing scope with a ‘}’ is slightly more concise (though more error prone) than creating a host\_accessor to the buffer.

If we use a host allocation to dump or verify the output values from a kernel, we need to put the buffer allocation into a block scope (or other scopes) so that we can control when it is destructed. We must then make sure that the buffer is destroyed before we access the host allocation to obtain the kernel output. Figure 13-9 shows this done correctly, while Figure 13-10 shows a common bug where the output is accessed while the buffer is still alive.

Advanced users may prefer to use buffer destruction to return result data from kernels into a host memory allocation. But for most users, and especially new developers, it is recommended to use scoped host accessors.

```cpp
constexpr size_t N = 1024;

// Set up queue on any available device
queue q;

// Create host containers to initialize on the host
std::vector<int> in_vec(N), out_vec(N);

// Initialize input and output vectors
for (int i = 0; i < N; i++) in_vec[i] = i;
std::fill(out_vec.begin(), out_vec.end(), 0);

// Create buffers using host allocations (vector in this
// case)
buffer in_buf{in_vec}, out_buf{out_vec};

// Submit the kernel to the queue
q.submit([&](handler& h) {
    accessor in{in_buf, h};
    accessor out{out_buf, h};

    h.parallel_for(range{N},
            [=](id<1> idx) { out[idx] = in[idx]; });
});

// BUG!!! We're using the host allocation out_vec, but the
// buffer out_buf is still alive and owns that allocation!
// We will probably see the initialiation value (zeros)
// printed out, since the kernel probably hasn't even run
// yet, and the buffer has no reason to have copied any
// output back to the host even if the kernel has run.
for (int i = 0; i < N; i++)
    std::cout << "out_vec[" << i << "]=" << out_vec[i]
        << "\n";
```

## Figure 13-10. Common bug: reading data directly from host allocation during buffer lifetime

To avoid these bugs, we recommend using host accessors instead of buffer scoping when getting started using C++ with SYCL. Host accessors provide access to a buffer from the host, and once their constructor has finished running, we are guaranteed that any previous writes (e.g., from kernels submitted before the host\_accessor was created) to the buffer have executed and are visible. This book uses a mixture of both styles (i.e., host accessors and host allocations passed to the buffer constructor) to provide familiarity with both. Using host accessors tends to be less error prone when getting started. Figure 13-11 shows how a host accessor can be used to read output from a kernel, without destroying the buffer first.

```cpp
constexpr size_t N = 1024;

// Set up queue on any available device
queue q;

// Create host containers to initialize on the host
std::vector<int> in_vec(N), out_vec(N);

// Initialize input and output vectors
for (int i = 0; i < N; i++) in_vec[i] = i;
std::fill(out_vec.begin(), out_vec.end(), 0);

// Create buffers using host allocations (vector in this
// case)
buffer in_buf{in_vec}, out_buf{out_vec};

// Submit the kernel to the queue
q.submit([&](handler& h) {
    accessor in{in_buf, h};
    accessor out{out_buf, h};

    h.parallel_for(range{N},
            [=](id<1> idx) { out[idx] = in[idx]; });
});

// Check that all outputs match expected value
// Use host accessor! Buffer is still in scope / alive
host_accessor A{out_buf};

for (int i = 0; i < N; i++)
    std::cout << "A[" << i << "]=" << A[i] << "\n";

Figure 13-11. Recommendation: Use a host accessor to read
kernel results
```

Host accessors can be used whenever a buffer is alive, such as at both ends of a typical buffer lifetime—for initialization of the buffer content and for reading of results from our kernels. Figure 13-12 shows an example of this pattern.

```cpp
constexpr size_t N = 1024;

// Set up queue on any available device
queue q;

// Create buffers of size N
buffer<int> in_buf{N}, out_buf{N};

// Use host accessors to initialize the data
{  // CRITICAL: Begin scope for host_accessor lifetime!
  host_accessor in_acc{in_buf}, out_acc{out_buf};
  for (int i = 0; i < N; i++) {
    in_acc[i] = i;
    out_acc[i] = 0;
  }
} // CRITICAL: Close scope to make host accessors go out
  // of scope!

// Submit the kernel to the queue
q.submit([&](handler& h) {
  accessor in{in_buf, h};
  accessor out{out_buf, h};

  h.parallel_for(range{N},
              =[=(id<1> idx) { out[idx] = in[idx]; });
});

// Check that all outputs match expected value
// Use host accessor!  Buffer is still in scope / alive
host_accessor A{out_buf};

for (int i = 0; i < N; i++)
  std::cout << "A[" << i << "]=" << A[i] << "\n";

Figure 13-12. Recommendation: Use host accessors for buffer
initialization and reading of results
```
````
