## Terminology

Terminologies : header-rows: 1

<table><tr><td></td><td></td><td>parent) executing on a VE and forwarded to the Thread Dispatcher by the TS unit. A child thread may or may not have child threads depending on whether it is a branch-node or a leaf-node thread. All pre-allocated resources such as URB and scratch memory for a child thread are managed by its parent thread. See also Parent Thread.</td></tr><tr><td>Command</td><td></td><td>Directive fetched from a ring buffer in memory by the Command Streamer and routed down a pipeline. Should not be confused with instructions which are fetched by the instruction cache subsystem and executed on a VE.</td></tr><tr><td>Command Streamer</td><td>CS or CSI</td><td>Functional unit of the Graphics Processing Engine that fetches commands, parses them, and routes them to the appropriate pipeline.</td></tr><tr><td>Core</td><td></td><td>Alternative name for a VE in the multi-processor system. See EU.</td></tr><tr><td>Dual Sub-slice</td><td>DSS</td><td>The collection of Vector Engines (VE) or Execution Units (EU) that have a common set of shared function units, such as sampler, dataport, and pixel port.</td></tr><tr><td>End of Thread</td><td>EOT</td><td>A message sideband signal on the Output message bus signifying that the message requester thread is terminated. A thread must have at least one SEND instruction with the EOT bit in the message descriptor field set to properly terminate.</td></tr><tr><td>Exception</td><td></td><td>Type of (normally rare) interruption to VE/EU execution of a thread's instructions. An exception occurrence causes the VE/EU thread to begin executing the System Routine, which is designed to handle exceptions.</td></tr><tr><td>Execution Channel</td><td></td><td>Single lane of a SIMD operand.</td></tr><tr><td>Execution Size</td><td>ExecSize</td><td>Execution Size indicates the number of data elements processed by an SIMD instruction. It is one of the instruction fields and can be changed per instruction.</td></tr><tr><td>Execution Unit</td><td>EU</td><td>An EU is a multi-threaded processor within the multi-processor system. Each EU is a fully-capable processor containing instruction fetch and decode, register files, source operand swizzle and SIMD ALU, etc. An EU is also referred to as a Core.</td></tr><tr><td>Execution Unit Identifier</td><td>EUID</td><td>A 4-bit field within a thread state register (SR0) that identifies the row and column location of the EU where a thread is located. A thread can be uniquely identified by the EUID and TID.</td></tr><tr><td>Execution Width</td><td>ExecWidth</td><td>The width of each of several data elements that may be processed by a single SIMD instruction.</td></tr><tr><td>General Register File</td><td>GRF</td><td>Large read/write register file shared by all the EUs/VEs for operand sources and destinations. This is the most commonly used read-write register space organized as an array of 256-bit registers for a thread.</td></tr><tr><td>General State Base Address</td><td></td><td>The Graphics Address of a block of memory-resident "state data", which includes state blocks, scratch space, constant buffers, and kernel programs. The contents of this memory block are referenced via offsets from the contents of the General State Base Address register. See Graphics Processing Engine.</td></tr><tr><td>Graphics Processing Engine</td><td>GPE</td><td>Collective name for the Subsystem, the 3D and Media pipelines, and the Command Streamer.</td></tr><tr><td>Memory-Mapped Input/Output</td><td>MMIO</td><td>A method for performing input/output between the CPU/GPU and peripheral devices.</td></tr><tr><td>Message</td><td></td><td>Messages are data packages transmitted from a thread to another thread, another shared function, or another fixed function. Message passing is the primary communication mechanism of Intel GPU architecture.</td></tr><tr><td>Parent Thread</td><td></td><td>A thread corresponding to a root-node or a branch-node in thread generation hierarchy. A parent</td></tr><tr><td></td><td></td><td>thread may be a root thread or a child thread depending on its position in the thread generation hierarchy. |</td></tr><tr><td>Resource Streamer</td><td>RS</td><td>Functional unit of the Graphics Processing Engine that examines the commands in the ring buffer in an attempt to pre-process certain long latency items for the remainder of the graphics processing.</td></tr><tr><td>Root Thread</td><td></td><td>A root-node thread. A thread corresponds to a root-node in a thread generation hierarchy. It is a kind of thread associated with the media fixed function pipeline. A root thread is originated from the VFE unit and forwarded to the Thread Dispatcher by the TS unit. A root thread may or may not have child threads. A root thread may have scratch memory managed by TS. A root thread with children has its URB resource managed by the VFE.</td></tr><tr><td>Single Instruction Multiple Data</td><td>SIMD</td><td>A parallel processing architecture that exploits data parallelism at the instruction level. It can also be used to describe the instructions in such an architecture or to describe the amount of data parallelism in a particular instruction (SIMD8 for example).</td></tr><tr><td>Spawn</td><td></td><td>To initiate a thread for execution on an EU/VE. Done by the thread spawner as well as most FF units in the 3D Pipeline.</td></tr><tr><td>Sub-Register</td><td></td><td>Subfield of a SIMD register. A SIMD register is an aligned fixed size register for a register file or a register type. For example, a GRF register, r2, is a 256-bits wide, 256-bit aligned register. A sub-register, r2.3:d, is the fourth dword of GRF register r2.</td></tr><tr><td>Subsystem</td><td></td><td>The name given to the resources shared by the FF units, including shared functions and EUs/VEs.</td></tr><tr><td>Surface</td><td></td><td>A rendering operand or destination, including textures, buffers, and render targets.</td></tr><tr><td>Surface State</td><td></td><td>State associated with a render surface.</td></tr><tr><td>Surface State Base Pointer</td><td></td><td>Base address used when referencing binding table and surface state data.</td></tr><tr><td>Synchronized Root Thread</td><td></td><td>A root thread that is dispatched by TS upon a 'dispatch root thread' message.</td></tr><tr><td>System IP</td><td>SIP</td><td>There is one global System IP register for all the threads. From a thread's point of view, this is a virtual read only register. Upon an exception, hardware performs some bookkeeping and then jumps to SIP.</td></tr><tr><td>System Routine</td><td></td><td>Sequence of instructions that handles exceptions. SIP is programmed to point to this routine, and all threads encountering an exception will call it.</td></tr><tr><td>Thread</td><td></td><td>An instance of a kernel program executed on an EU/VE. The life cycle for a thread starts from the executing the first instruction after being dispatched from Thread Dispatcher to an EU/VE to the execution of the last instruction - a send instruction with EOT that signals the thread termination. Threads in the system may be independent from each other or communicate with each other through Message Gateway share function.</td></tr><tr><td>Thread Dispatcher</td><td>TD, TDL</td><td>Functional unit that arbitrates thread initiation requests from Fixed Functions units and instantiates the threads on EUs/VEs.</td></tr><tr><td>Thread Identifier</td><td>TID</td><td>The field within a thread state register (SR0) that identifies which thread slots on an EU/VE a thread occupies. A thread can be uniquely identified by the EUID and TID.</td></tr><tr><td>Thread Payload</td><td></td><td>Before a thread starting execution, some amount of data is pre-loaded into the thread's GRF (starting at r0). This data is typically a combination of control information provided by the spawning entity (FF Unit) and data read from the URB.</td></tr><tr><td>Thread Spawner</td><td>TS</td><td>The second and the last fixed function stage of the media pipeline that initiates new threads on behalf of generic/media processing.</td></tr><tr><td>Unsynchronized Root Thread</td><td></td><td>A root thread that is automatically dispatched by TS.</td></tr></table>

## Level Zero

Level Zero is the low-level interface that enables oneAPI libraries to exploit the hardware capabilities of target devices. This section provides an insight into the architectural design followed in the Intel® Graphics Compute Runtime for oneAPI Level Zero. Implementation details and optimization guidelines are explained, as well as a description of the different features available for the different supported platforms.

• Immediate Command Lists

## Immediate Command Lists

## Introduction

Immediate command lists is a feature provided by Level-Zero specification to allow for very low latency submission usage models. In this scheme, commands appended on the command list such as launching a kernel or performing a memory copy are immediately submitted to the device for execution. This is different from a regular command list where multiple commands can be stitched and submitted together for execution .

Distinctions between an immediate command list compared to a regular command list include (but not limited to) the following:

• An immediate command list is an implicit command queue and is therefore created using a command queue descriptor.

• Commands appended to an immediate command list are submitted for execution immediately on the device.

• Immediate command lists are not required to be closed or reset.

• Synchronization of immediate command lists cannot be performed via zeCommandQueueSynchronize or zeFenceHostSynchronize as there is no command queue handle associated with the immediate command list. Recommendation is to use events to confirm commands submitted to the immediate command list have completed.

Since the intention of immediate command lists is to primarily provide a razor thin submission interface to the device, they are well suited to be used in workloads which have tendency to launch small or short running kernels and also need to run multiple iterations of such kernels. Examples of workloads with such characteristics can be found in HPC environments and also ML/DL frameworks.

## Programming Model

Following code shows how to create an immediate command list and submitting a kernel with it. Synchronization is achieved by querying the event status.

```matlab
ze_command_queue_desc_t cmdQueueDesc = {ZE_STRUCTURE_TYPE_COMMAND_QUEUE_DESC};
cmdQueueDesc.pNext = nullptr;
cmdQueueDesc.flags = 0;
cmdQueueDesc.priority = ZE_COMMAND_QUEUE_PRIORITY_NORMAL;
cmdQueueDesc.ordinal = queueGroupOrdinal;
cmdQueueDesc.index = 0;
```

```cpp
cmdQueueDesc.mode = ZE_COMMAND_QUEUE_MODE_ASYNCHRONOUS;
zeCommandListCreateImmediate(context, device, &cmdQueueDesc, &cmdList);

zeCommandListAppendLaunchKernel(cmdList, kernel, &dispatchTraits,
                          events[0], 0, nullptr);
// If Async mode, use event for sync
zeEventHostSynchronize(events[0], std::numeric_limits<uint64_t>::max() - 1);
```

Immediate command lists may also be used to implement in-order queues. In this case, commands submitted to the list are chained together using events, as seen below.

```cpp
zeCommandListAppendMemoryCopy(cmdList, deviceBuffer, hostBuffer, allocSize,
                          events[0],
                          0, nullptr);

zeCommandListAppendMemoryCopy(cmdList, stackBuffer, deviceBuffer, allocSize,
                          events[1],
                          1,
                          &events[0]);

zeEventHostSynchronize(events[1], std::numeric_limits<uint64_t>::max() - 1));
```

As with regular lists, immediate command lists may also be synchronous. In this case, synchronization is performed implicitly and each command submitted to the list is immediately submitted, and is guaranteed to have completed upon return from the call.

```txt
ze_command_queue_desc_t cmdQueueDesc = {ZE_STRUCTURE_TYPE_COMMAND_QUEUE_DESC};
cmdQueueDesc.pNext = nullptr;
cmdQueueDesc.flags = 0;
cmdQueueDesc.priority = ZE_COMMAND_QUEUE_PRIORITY_NORMAL;
cmdQueueDesc.ordinal = queueGroupOrdinal;
cmdQueueDesc.index = 0;
cmdQueueDesc.mode = ZE_COMMAND_QUEUE_MODE_SYNCHRONOUS;
zeCommandListCreateImmediate(context, device, &cmdQueueDesc, &cmdList);

zeCommandListAppendLaunchKernel(cmdList, kernel, &dispatchTraits,
                                nullptr, 0, nullptr);

// At this point, kernel has been executed
```

For more code samples, please refer compute-benchmarks repository https://github.com/intel/compute benchmarks. Scenarios such as create\_command\_list\_immediate\_l0.cpp and execute\_command\_list\_immediate\_l0.cpp serve as good starting points.

## Performance Profiling and Analysis

Understanding the behavior of your system is critical to making informed decisions about optimization choices. Some tools like profilers, analyzers, or debuggers are full-featured. Other tools like interval timers, kernel timers, and print statements are lighter weight. But all of them serve an important purpose in the optimization process.

This section covers topics related to these tools’ use for software optimization.

• Using the Timers

• Intel<sup>®</sup> VTune<sup>TM</sup> Profiler

• Intel<sup>®</sup> Advisor

• Intel<sup>®</sup> Intercept Layer for OpenCL<sup>TM</sup> Applications

• Performance Tools in Intel<sup>®</sup> Profiling Tools Interfaces for GPU

## Using the Timers

The standard C++ chrono library can be used for tracking times with varying degrees of precision in SYCL. The following example shows how to use the chrono timer class to time kernel execution from the host side.

```cpp
#include <sycl/sycl.hpp>
#include <iostream>
using sycl;

// Array type and data size for this example.
constexpr size_t array_size = (1 << 16);
typedef std::array<int, array_size> IntArray;

double VectorAdd(queue &q, const IntArray &a, const IntArray &b, IntArray &sum) {
    range<1> num_items{a.size()};

    buffer a_buf(a);
    buffer b_buf(b);
    buffer sum_buf(sum.data(), num_items);

    auto t1 = std::chrono::steady_clock::now();   // Start timing

    q.submit([&](handler &h) {
        // Input accessors
        auto a_acc = a_buf.get_access<access::mode::read>(h);
        auto b_acc = b_buf.get_access<access::mode::read>(h);

        // Output accessor
        auto sum_acc = sum_buf.get_access<access::mode::write>(h);

        h.parallel_for(num_items, [=](id<1> i) { sum_acc[i] = a_acc[i] + b_acc[i]; });
    }).wait();

    auto t2 = std::chrono::steady_clock::now();   // Stop timing

    return(std::chrono::duration_cast<std::chrono::microseconds>(t2 - t1).count());
}

void InitializeArray(IntArray &a) {
    for (size_t i = 0; i < a.size(); i++) a[i] = i;
}

int main() {
    default_selector d_selector;

    IntArray a, b, sum;

    InitializeArray(a);
    InitializeArray(b);

    queue q(d_selector);

    std::cout << "Running on device: "
            << q.get_device().get_info<info::device::name>() << "\n";
    std::cout << "Vector size: " << a.size() << "\n";

    double t = VectorAdd(q, a, b, sum);
```

```cpp
std::cout << "Vector add successfully completed on device in " << t << " microseconds\n";
return 0;
}
```

Note that this timing is purely from the host side. The actual execution of the kernel on the device may start much later, after the submission of the kernel by the host. SYCL provides a profiling capability that let you keep track of the time it took to execute kernels.

```cpp
#include <sycl/sycl.hpp>
#include <array>
#include <iostream>
using namespace sycl;

// Array type and data size for this example.
constexpr size_t array_size = (1 << 16);
typedef std::array<int, array_size> IntArray;

double VectorAdd(queue &q, const IntArray &a, const IntArray &b, IntArray &sum) {
    range<1> num_items{a.size()};

    buffer a_buf(a);
    buffer b_buf(b);
    buffer sum_buf(sum.data(), num_items);

    event e = q.submit([&](handler &h) {
        // Input accessors
        auto a_acc = a_buf.get_access<access::mode::read>(h);
        auto b_acc = b_buf.get_access<access::mode::read>(h);

        // Output accessor
        auto sum_acc = sum_buf.get_access<access::mode::write>(h);

        h.parallel_for(num_items, [=](id<1> i) { sum_acc[i] = a_acc[i] + b_acc[i]; });
    });
    q.wait();
    return(e.template get_profiling_info<info::event_profiling::command_end>() -
        e.template get_profiling_info<info::event_profiling::command_start>());
}

void InitializeArray(IntArray &a) {
    for (size_t i = 0; i < a.size(); i++) a[i] = i;
}

int main() {
    default_selector d_selector;

    IntArray a, b, sum;

    InitializeArray(a);
    InitializeArray(b);

    queue q(d_selector, property::queue::enable_profiling{});

    std::cout << "Running on device: "
        << q.get_device().get_info<info::device::name>() << "\n";
    std::cout << "Vector size: " << a.size() << "\n";

    double t = VectorAdd(q, a, b, sum);
```

```cpp
std::cout << "Vector add successfully completed on device in " << t << " nanoseconds\n";
return 0;
}
```

When these examples are run, it is quite possible that the time reported by chrono is much larger than the time reported by the SYCL profiling class. This is because the SYCL profiling does not include any data transfer times between the host and the offload device.

## Intel® VTuneTM Profiler

The Intel<sup>®</sup> VTune<sup>TM</sup> Profiler is a performance analysis tool for optimizing CPU, GPU, and other accelerator applications. It helps developers find performance bottlenecks in their applications and identify where and how the applications can be optimized to benefit most from available hardware resources. In terms of GPU performance, it can:

• Find out if the application is CPU or GPU-bound

• Calculate hardware utilization

• Report XVE stalls

• Report locations of stalls, and types of stalls in Intel<sup>®</sup> Data Center GPU Max Series

• Identify hot computing tasks or kernels that could be candidates for further optimizations

• Analyze data transfers and bandwidth utilization

• Identify memory/cache units that bottleneck the performance

• Find inefficient data access patterns in your algorithm and memory access that cause significant stalls

• Determine efficiencies of SIMD instructions generated by the compiler

• Provide quick insights into data collected from multiple GPUs using Application Performance Snapshot

For details and techniques on optimizing GPU performance using VTune Profiler, please see

Software Optimization for Intel® GPUs

Optimize Applications for Intel® GPUs with Intel® VTune™ Profiler

## Intel® Advisor

The Intel<sup>®</sup> Advisor is a tool for assisting developers to design and optimize high-performing applications. In terms of GPU performance, it provides:

• Offload Modeling

• Roofline and Performance Insights

Offload Modeling produces upper-bound speedup estimates using a bound-and-bottleneck performance model. It takes CPU metrics and application characteristics as input and applies an analytical model to estimate execution time and characteristics on a target GPU. It can:

• Identify code regions that benefit from offloading

• Find performance bottlenecks

• Project performance gains with offloading

• Project performance gains if existing code executes on next-generation GPUs

• Provide optimization guidance

Roofline and Performance Insights visualize the actual performance of GPU kernels and inherent hardwareimposed performance ceilings, and determine the main performance limiting factors even on a multi-tile/ multi-card GPU system. It helps developers to find:

• The maximum achievable performance with the current hardware resources

• If the current implementation performs optimally on current hardware

• The best candidates to optimize if the current implementation is not optimal

• The limiting performance factors such as memory bandwidth, compute capacity for each candidate

For details and techniques on optimizing GPU performance using Intel<sup>®</sup> Advisor, please see

Intel® Advisor Performance Optimization Cookbook

## Intel® Intercept Layer for OpenCLTM Applications

The Intercept Layer for OpenCL Applications is a command-line tool for tracing and analyzing OpenCL applications. It has a set of features for logging host and device activities, dumping and disassembling kernel binaries, etc. If your oneAPI applications use OpenCL backend, you may find this tool is helpful for performance tuning.

More information including the source code is available at the github repository Intercept Layer for OpenCL Applications.

## Performance Tools in Intel® Profiling Tools Interfaces for GPU

Intel® Profiling Tools Interfaces for GPU has a set of tracing and profiling tools for Intel<sup>®</sup> oneAPI applications in the tools folder. These lightweight command-line tools support both Level Zero and OpenCL backends.

In addition to device activities, the tools are capable of tracing host activities from Level Zero or OpenCL runtime layer all the way up to MPI layer. You can use the tools to quickly identify bottlenecks on device and host. You can also use the tools to profile GPU hardware performance counters , for example, thread occupancies, memory traffic, cache utilization and function unit utilization etc.. Furthermore, You can run the tool unitrace to profile GPU kernels at instruction level, pinpoint instructions that stalls the execution unit or the vector engine and report reasons of the stalls.

The performance data generated in JSON format can be viewed in a browser using a trace viewer such as https://ui.perfetto.dev.

Please check the tools folder for detailed information and the source code of each tool.

## Configuring GPU Device

To extract the best end-to-end performance from applications, you may sometimes need to modify device settings at a system level. Depending on whether sudo access is required, a system administrator may need to apply these settings.

## GPU Drivers or Plug-ins (Optional)

You can develop oneAPI applications using C++ and SYCL\* that run on Intel, AMD\*, or NVIDIA\* GPUs.

To develop and run applications for specific GPUs, you must first install the corresponding drivers or plug-ins:

• To use an Intel GPU, install the latest Intel GPU drivers.

• To use an AMD GPU (Linux only):

• Read the oneAPI for AMD GPUs Guide from Codeplay.

• Download oneAPI for AMD GPUs.

• To use an NVIDIA GPU (Linux and Windows):

• Read the oneAPI for NVIDIA® GPUs Guide from Codeplay.

• Download oneAPI for NVIDIA® GPUs GPUs.

## Performance Impact of Pinning GPU Frequency

When applications use GPUs for large portions of their computations, we recommend that you pin the GPU at an optimal frequency. Some examples of these applications are High-Performance Computing workloads, which have computationally intensive portions in their algorithms offloaded to the device.

For applications that are memory bound, with kernels running for a very short time but spend more time in data exchanges, the effects of pinning the GPU to a higher frequency might be less pronounced or even detrimental.

The maximum fused GPU frequency, which is the theoretical hardware maximum frequency, can be obtained using sysfs handles, for example:

```txt
for (( i=1; i<$num_cards; i++ ))
do
    for (( j=0; j<$num_tiles; j++ ))
    do
        cat /sys/class/drm/card$i/gt/gt$j/rps_RP0_freq_mhz;
    done
done
```

You can also obtain the current maximum software frequency, which you can dynamically modify with rps\_max\_freq\_mhz:

```shell
for (( i=1; i<\$num_cards; i++ ))
do
    for (( j=0; j<\$num_tiles; j++ ))
    do
        cat /sys/class/drm/card\$i/gt/gt\$j/rps_max_freq_mhz;
    done
done
```

The default policy in the Linux\* kernel mode driver (i915) for server platforms is to set the frequency request range where: rps\_min\_freq\_mhz = rps\_max\_freq\_mhz = rps\_boost\_freq\_mhz = rps\_RP0\_freq\_mhz

You can set the frequency using sysfs handles provided by the DRM Linux kernel driver:

```shell
for (( i=1; i<\$num_cards; i++ ))
do
  for (( j=0; j<\$num_tiles; j++ ))
  do
    echo \$desired_freq > /sys/class/drm/card\$i/gt/gt\$j/rps_min_freq_mhz;
    echo \$desired_freq > /sys/class/drm/card\$i/gt/gt\$j/rps_max_freq_mhz;
    echo \$desired_freq > /sys/class/drm/card\$i/gt/gt\$j/rps_boost_freq_mhz;
  done
done
```

Notes regarding frequency pinning:

• Firmware is final arbiter on granted frequency.

• Some throttling may occur for thermal/power budget reasons.

• Once the frequency is pinned to a fixed value, there is no dynamic scaling. For server platforms, the current i915 policy pins frequency to rps\_max\_freq\_mhz at boot time.

## Switching Intel<sup>®</sup> X<sup>e</sup> Link On/Off

Intel<sup>®</sup> X<sup>e</sup> Link is a high-speed connectivity fabric hardware that provides accelerated data transfer capabilities for scale-up and scale-out operations. These are typically used for inter-GPU and inter-node data transfer operations for HPC applications deployed at cluster scale. However, for applications that do not use these capabilities, it could be beneficial to turn off the power to this resource to allow for lower frequency throttling on the GPU compute engines.

The following examples describe how to turn off power to Intel<sup>®</sup> X<sup>e</sup> Link:

```shell
modprobe -r iaf;
for i in {0..\$num_cards}; do
  cat /sys/class/drm/card$i/iaf_power_enable;
done;

for i in {0..\$num_cards}; do
  echo 0 > /sys/class/drm/card$i/iaf_power_enable;
```

```shell
done;

for i in {0..\$numcards}; do
  cat /sys/class/drm/card$i/iaf_power_enable;
done
```

\$num\_cards can be obtained by listing the /sys/class/drm/ directory and noting how many card\* subdirectories exist.

## Time Slice Considerations

The performance of workloads can vary depending on the amount of time slice given to each context. To control the time slice duration, you can use a parameter to allow fine-tuning of the time slice at a per-engine level. The released driver default is set to five ms. If a workload needs a higher time slice, configure the parameter accordingly. The following example sets the time slice to 50 ms on all engines and devices:

```txt
for i in /sys/class/drm/card*/engine/*/timeslice_duration_ms; do
    echo 50 >\$i;
done;
```

You must initiate this process any time the driver loads since the echo is not persistent across reboots. You can use udev scripts to run the process automatically.

## Media Graphics Computing on GPU

We have focused on GPGPU optimization techniques and tools so far. When it comes to media graphics computing, a new set of optimization techniques and tools are also needed for maximizing utilization efficiency of the hardware, especially the dedicated units, for example, the media engines.

• Optimizing Media Pipelines

• Performance Analysis with Intel<sup>®</sup> Graphics Performance Analyzers

## Optimizing Media Pipelines

Media operations are ideal candidates for hardware acceleration because they are relatively large algorithms with well-defined inputs and outputs. Video processing hardware capabilities can be accessed via industrystandard frameworks, Intel<sup>®</sup> Video Processing Library (Intel<sup>®</sup> VPL), or low-level/operating system specific approaches like Video Acceleration API (VA-API) for Linux or Microsoft\* DirectX\* for Windows. Which path to choose depends on many factors. However, the basic principles like parallelization by multiple streams and maximizing data locality apply for all options.

The main differences between video processing and GPGPU work apply to all accelerator API options. Many typical GPGPU optimizations focus on optimizing how large grids of work are partitioned across multiple processing units. Hardware-accelerated media operations are implemented in silicon. They work in units of frames and usually work is partitioned by streams of frames.

Media optimization steps don’t match the GPGPU workflow described in other sections. However, they can be easily added before or after GPGPU work. Media steps will supply inputs to or take outputs from GPGPU steps. For example:

![](images/6b76cab6c597c0a67fca93fafa11263a98ebb0727f79d476b2ab34e2eb3f2484.jpg)

• Media Engine Hardware

• Media API Options for Hardware Acceleration

• Media Pipeline Parallelism

• Media Pipeline Inter-operation and Memory Sharing

• SYCL-Blur Example

Video streaming is prevalent in our world today. We stream meetings at work. We watch movies at home. We expect good quality. Taking advantage of this new media engine hardware gives you the option to stream faster, stream at higher quality and/or stream at lower power. This hardware solution is an important consideration for End-to-End performance in pipelines working with video data.

## Media Engine Hardware

As described in Intel<sup>®</sup> X<sup>e</sup> Architecture section, Xe- Intel® Data Center GPU Flex Series and some other Intel<sup>®</sup> GPUs contain media engine which provide fully-accelerated video decode, encode and processing capabilities. This is sometimes called Intel<sup>®</sup> Quick Sync Video. The media engine runs completely independent of compute engines (vector and matrix engines).

![](images/c99b74538d2f14a57f2754caf4f7cfe67eea8ebe288f98908d4a7be0bd45435f.jpg)

Several components can be used by applications:

• MFX/Multi-format codec: hardware decode and encode. Some configurations include two forms of encode. 1) motion estimation + bit packing and 2) full fixed function/low power

• SFC/scaler and format conversion: resize (primarily intended for downscaling), conversion between color formats such as NV12 and BGRA

• Video Quality Engine: multiple frame processing operations, such as denoise and deinterlace.

This hardware has its own instruction queue and clock, so fully fixed function work can be very low power if configured to use low power pathways. This can also leave the slice capabilities on the GPU free for other work.

## Supported codecs

New codec capabilities are added with each new GPU hardware generation.

<table><tr><td></td><td></td><td>AVC</td><td>MPEG 2</td><td>JPEG</td><td>VP8</td><td>HEVC 8-bit</td><td>HEVC 8-bit 422</td><td>HEVC 8-bit 444</td><td>HEVC 10-bit</td><td>HEVC 10-bit 422</td></tr><tr><td>CPU</td><td></td><td>D/E*</td><td>D</td><td>D/E</td><td></td><td>D/E</td><td></td><td></td><td>D/E</td><td></td></tr><tr><td rowspan="6">Media SDK GPU</td><td> $5^{th}$  Generation Intel® Core (BDW)</td><td>D/Es</td><td>D/Es</td><td>D</td><td>D</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td> $6^{th}$  Generation Intel® Core (SKL)</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D</td><td>D/Es</td><td></td><td></td><td></td><td></td></tr><tr><td>Intel Atom® Processor E3900 series (APL)</td><td>D/E/Es</td><td>D</td><td>D/E</td><td>D</td><td>D/Es</td><td></td><td></td><td>D</td><td></td></tr><tr><td> $7^{th}$  Generation Intel® Core (KBLx)</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D/Es</td><td>D/Es</td><td></td><td></td><td>D/Es</td><td></td></tr><tr><td> $10^{th}$  Generation Intel® Core (ICL)</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D/Es</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D/E/Es</td><td>D/Es</td></tr><tr><td>Intel Atom® Processor X Series (EHL)</td><td>D/E</td><td>D</td><td>D/E</td><td>D</td><td>D/E</td><td>D</td><td>D/E</td><td>D/E</td><td>D</td></tr><tr><td rowspan="2">oneVPL GPU</td><td>Intel® Iris® Xe (TGL/RKL/ADL), Intel® Iris® Xe MAX (DGI)</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D (TGL only)</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D/E/Es</td><td>D/Es</td></tr><tr><td>Intel® ARC</td><td>D/E</td><td>D/E</td><td>D/E</td><td>D</td><td>D/E</td><td>D/E</td><td>D/E</td><td>D/E</td><td></td></tr></table>

Note: in this table two kinds of encode are represented.  
E=Hardware Encode via low power VDEnc  
Es=Hardware Encode via (PAK) + Shader (media kernel +VME)  
Intel<sup>®</sup> Arc A-series and Intel<sup>®</sup> Server GPU (previously known as Arctic Sound-M) add AV1 encode. This cutting edge successor to VP9 adds additional encode control for stack, segmentation, film grain filtering, and other new features. These increase encode quality at a given bitrate or allow a decrease in bitrate to provide increased quality.

![](images/273d1d75f5d8dfdf0c5111099ced4f5645b70db9e50fe69402dac7972aebe352.jpg)

## Media API Options for Hardware Acceleration

There are multiple ways to accelerate video processing on Intel<sup>®</sup> architecture (CPUs, GPUs). To choose the option that benefits you most, ensure your goals align with the tools you choose.

## Industry Standard Frameworks: FFmpeg, GStreamer,

OpenCV, etc.

Used for

• Full media solution w/ network protocols, container support, audio support, etc.

• Easily move across accelerators and HW vendors

## Intel® oneAPI Video Processing Library (oneVPL)

Used for

• Project focused on video elementary stream processing only

· OS agnostic

## Low-level Hardware or OS-specific Solutions: VA-API/DXVA

Used for

• Most control/direct integration with OS-specific graphics stack

• Project is already based on VA-API/DXVA

As shown above there are higher-level tools and lower-level tools. Do you need the extremely low-level control you can get with operating system specific tools like libva\* or DirectX\*? And do you have the extra time it takes to develop these low-level applications? Or is it more important to be able to easily port your code from Linux\* to Windows\* and save time by coding with higher level tools?

More details to help match the approach option to requirements are in the table below.

<table><tr><td></td><td>Intel® Video Processing Library</td><td>Media Frameworks (FFmpeg &amp; GStreamer)</td><td>Low-level/OS-specific solutions (Libva &amp; DXVA)</td></tr><tr><td>Functionality</td><td>Elementary video stream processing with a limited set of frame processing operations</td><td>Full stack (network protocols, container support, audio support)</td><td>Working directly with the OS graphics stack</td></tr><tr><td>Level of control over hardware capabilities</td><td>Medium</td><td>Low</td><td>High</td></tr><tr><td>Portability</td><td>High</td><td>High</td><td>Low</td></tr></table>

## Media Pipeline Parallelism
