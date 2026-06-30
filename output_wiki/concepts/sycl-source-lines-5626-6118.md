# sycl Source Lines 5626-6118

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source sycl:L5626-L6118

Citation: [sycl:L5626-L6118]

````text
# Device Information and Kernel Specialization

In this chapter, we look at the advanced concept of making our program more flexible and therefore more portable. This is done by looking at mechanisms to match the capabilities of any system (and accelerators) our application might be executed upon, with a selection of kernels and code that we have written. This is an advanced topic because we can always simply “use the default accelerator” and run the kernels we write on that regardless of what it is. We have learned that this will work even on systems which may have no accelerator because SYCL guarantees there is always a device available that will run a kernel even if it is the CPU that is also running our host application.

When we move beyond “use the default accelerator” and generalpurpose kernels, we find mechanisms are available to choose which device(s) to use, and mechanisms to create more specialized kernels. We discuss both capabilities in this chapter. Together, these two capabilities allow us to construct applications that are highly adaptable to the system on which they are executed.

## Chapter 12 Device Information and Kernel Specialization

Fortunately, the creators of the SYCL specification thought about these needs and gave us interfaces to let us solve this problem. The SYCL specification defines a device class that encapsulates a device on which kernels may be executed. We first cover the ability to query the device class, so that our program can adapt to the device characteristics and capabilities. We may occasionally choose to write different algorithms for different devices. Later in this chapter, we learn that we can apply aspects to a kernel to specialize a kernel and let a compiler take advantage of that. Such specialization helps make a kernel more tailored to a certain class of devices while likely rendering it unsuitable for other devices. Combining these concepts allows us to adapt our program as much, or as little, as we wish. This ensures we can decide how much investment to make in squeezing out performance while starting with broad portability.

## Is There a GPU Present?

Many of us will start with having logic to figure out “Is there a GPU present?” to inform the choices our program will make as it executes. That is the start of what this chapter covers. As we will see, there is much more information available to help us make our programs robust and performant.

Parameterizing a program can help with correctness, functional portability, performance portability, and future proofing.

This chapter dives into the most important queries and how to use them effectively in our programs. Implementations doubtlessly offer more detailed properties that we can query. To learn all possible queries, we

would need to review the latest SYCL specification, the documentation for our particular compiler, and documentation for any runtimes/drivers we may encounter.

Device-specific properties are queryable using get\_info functions, including access to device-specific kernel and work-group properties.

## Refining Kernel Code to Be More Prescriptive

It is useful to consider that our coding, kernel by kernel, will fall broadly into one of these three categories:

• Generic kernel code: Run anywhere, not tuned to a specific class of device.

Device type–specific kernel code: Run on a type of device (e.g., GPU, CPU, FPGA), not tuned to specific models of a device type. This is particularly useful because many device types share common features, so it is safe to make some assumptions that would not apply to fully general code written for all devices.

Tuned device-specific kernel code: Run on a type of device, with tuning that reacts to specific parameters of a device—this covers a broad range of possibilities from a small amount of tuning to very detailed optimization work.

It is our job as programmers to determine when different patterns are needed for different device types. We dedicate Chapters 14, 15, 16, and 17 to illuminating this important thinking.

It is most common to start by focusing on getting things working with a functionally correct implementation of a generic kernel. Chapter 2 specifically talks about what methods are easiest to debug when getting started with a kernel implementation. Once we have a kernel working, we may evolve it to target the capabilities of a specific device type or device model.

Chapter 14 offers a framework of thinking to consider parallelism first, before we dive into device considerations. It is our choice of pattern (a.k.a. algorithm) that dictates our code, and it is our job as programmers to determine when different patterns are needed for different devices. Chapters 15 (GPU), 16 (CPU), and 17 (FPGA) dive more deeply into the qualities that distinguish these device types and motivate a choice in pattern to use. It is these qualities that motivate us to consider writing distinct versions of kernels when the best approach (pattern choice) varies on different device types.

When we have a kernel written for a specific type of device (e.g., a specific CPU, GPU, FPGA, etc.), it is logical to adapt it to specific vendors or even models of such devices. Good coding style is to parameterize code based on features (e.g., item size support found from a device query).

We should write code to query parameters that describe the actual capabilities of a device instead of its marketing information; it is bad programming practice to query the model number of a device and react to that—such code is less portable because it is not future-proof.

It is common to write a different kernel for each device type that we want to support (a GPU version of a kernel and an FPGA version of a kernel and maybe a generic version of a kernel). When we get more specific, to support a specific device vendor or even device model, we may benefit when we can parameterize a kernel rather than duplicate it. We are free to do either, as we see fit. Code cluttered with too many parameter adjustments may be hard to read or excessively burdened at runtime. It is common however that parameters can fit neatly into a single version of a kernel.

Parameterizing makes the most sense when the algorithm is broadly the same but has been tuned for the capabilities of a specific device. Writing a different kernel is much cleaner when using a completely different approach, pattern, or algorithm.

## How to Enumerate Devices and Capabilities

Chapter 2 enumerates and explains five methods for choosing a device on which to execute. Essentially, Method#1 was the least prescriptive run it somewhere, and we evolve to the most prescriptive Method#5, which considered executing on a fairly precise model of a device from a family of devices. The enumerated methods in between gave a mix of flexibility and prescriptiveness. Figure 12-1, Figure 12-2, and Figure 12-4 help to illustrate how we can select a device.

Figure 12-1 shows that even if we allow the implementation to select a default device for us (Method#1 in Chapter 2), we can still query for information about the selected device.

Figure 12-2 shows how we can try to set up a queue using a specific device (in this case, a GPU), but fall back explicitly on the default device if no GPU is available. This gives us some control of our device choice by biasing us to get a GPU whenever one is available. We know that at least one device is always guaranteed to exist so our kernels can always run in a properly configured system. When there is no GPU, many systems will default to a CPU device but there is no guarantee. Likewise, if we ask for a CPU device explicitly, there is no guarantee there is such a device (but we are guaranteed that some device will exist).

It is not recommended that we use the solution shown in Figure 12-2. In addition to appearing a little scary and error prone, Figure 12-2 does not give us control over which GPU is selected if there are choices of GPUs at runtime. Despite being both instructive and functional, there is a better way. It is recommended that we write custom device selectors as shown in the next code example (Figure 12-4).

```txt
queue q;

std::cout << "By default, we are running on "
       << q.get_device().get_info<info::device::name>()
       << "\n";

Example Outputs (one line per run - depends on system):
By default, we are running on NVIDIA GeForce RTX 3060
By default, we are running on AMD Radeon RX 5700 XT
By default, we are running on Intel(R) UHD Graphics 770
By default, we are running on Intel(R) Xeon(R) Gold 6336Y CPU @ 2.40GHz
By default, we are running on Intel(R) Data Center GPU Max 1100
```  
Figure 12-1. Device we have been assigned by default

Queries about devices rely on installed software (special user-level drivers), to respond regarding a device. SYCL relies on this, just as an operating system needs drivers to access hardware—it is not sufficient that the hardware simply be installed in a machine.

```cpp
auto GPU_is_available = false;

try {
  device testForGPU(gpu_selector_v);
  GPU_is_available = true;
} catch (exception const& ex) {
  std::cout << "Caught this SYCL exception: " << ex.what()
      << std::endl;
}

auto q = GPU_is_available ? queue(gpu_selector_v)
              : queue(default_selector_v);

std::cout
  << "After checking for a GPU, we are running on:\n "
  << q.get_device().get_info<info::device::name>()
  << "\n";

Four Example Outputs (using four different
  systems, each with a GPU):
After checking for a GPU, we are running on:
  AMD Radeon RX 5700 XT
After checking for a GPU, we are running on:
  Intel(R) Data Center GPU Max 1100
After checking for a GPU, we are running on:
  NVIDIA GeForce RTX 3060
After checking for a GPU, we are running on:
  Intel(R) UHD Graphics 770

Example Output (using a system without GPU):
Caught this SYCL exception: No device of
requested type 'info::device_type::gpu' available.
...(PI_ERROR_DEVICE_NOT_FOUND)
After checking for a GPU, we are running on:
  AMD Ryzen 5 3600 6-Core Processor
```

## Figure 12-2. Using try-catch to select a GPU device if possible, use the default device if not

## Aspects

The SYCL standard has a small list of device aspects that can be used to understand the capabilities of a device, to control which devices we choose to use, and to control which kernels we submit to a device. At the end of this chapter, we will discuss “kernel specialization” and kernel templating. For now, we will enumerate the aspects and how to use them in device queries and selection. Figure 12-3 lists aspects that are defined by the SYCL standard to be available for use in every C++ program using SYCL. Aspects are Boolean—a device either has or does not have an aspect. The first four (cpu/gpu/accelerator/custom) are mutually exclusive since device types are defined as an enum by SYCL 2020. Features including aspect::fp16, aspect::fp64, and aspect::atomic64 are “optional features” so they may not be supported by all devices—testing for these can be especially important for a robust application.

<table><tr><td>Standard aspect (all booleans)</td><td>The device...</td></tr><tr><td>aspect::cpu</td><td>executes code on a CPU</td></tr><tr><td>aspect::gpu</td><td>executes code on a GPU</td></tr><tr><td>aspect::accelerator</td><td>executes code on an accelerator</td></tr><tr><td>aspect::custom</td><td>executes fixed functions only, no support for programmable kernels</td></tr><tr><td>aspect::emulated</td><td>executes code in an emulator, not for performance - typically used for debug, profiling, etc.</td></tr><tr><td>aspect::host_debuggable</td><td>can fully support standard debugging</td></tr><tr><td>aspect::fp16</td><td>supports the sycl::half data type</td></tr><tr><td>aspect::fp64</td><td>supports the double data type</td></tr><tr><td>aspect::atomic64</td><td>supports 64-bit atomic operations</td></tr><tr><td>aspect::image</td><td>supports images, a topic not covered in this book (we emphasize the more general and portable buffer instead)</td></tr><tr><td>aspect::online_compileraspect::online_linker</td><td>supports online compilation and/or linking of device code. Such devices may support the build(), compile(), and link() functions, all very advanced topics not covered in this book</td></tr><tr><td>aspect::queue_profiling</td><td>supports queue profiling, an advanced topic discussed a bit, along with other practical tips, in Chapter 13</td></tr><tr><td>aspect::usm_device_allocationsaspect::usm_host_allocationsaspect::usm_atomic_host_allocationsaspect::usm_shared_allocationsaspect::usm_atomic_shared allocations</td><td>supports the corresponding USM capability</td></tr><tr><td>aspect::usm_system_allocations</td><td>supports sharing data allocated by the system allocators, not just the SYCL USM allocation calls; such usage will impact portability and may impact performance</td></tr></table>

Figure 12-3. Aspects defined by the SYCL standard (implementations can add more)

## Custom Device Selector

Figure 12-4 uses a custom device selector. Custom device selectors were first discussed in Chapter 2 as Method#5 for choosing where our code runs (Figure 2-16). The custom device selector evaluates each device available to the application. A particular device is selected based on receiving the highest score (or no device if the highest score is -1). In this example, we will have a little fun with our selector:

• Reject non-GPUs (return -1).

• Favor GPUs with a vendor name including the word “ACME” (return 24 if Martian, 824 otherwise).

• Any other non-Martian GPU is a good one (return 799).

• Martian GPUs, which are not ACME, are rejected (return -1).

The next section, “Being Curious: get\_info<>,” dives into the rich information that get\_devices(), get\_platforms(), and get\_info<> offer. Those interfaces open up any type of logic we might want to utilize to pick our devices, including the simple vendor name checks shown in Figure 2-16 and Figure 12-4.

```cpp
#include <iostream>
#include <sycl/sycl.hpp>
using namespace sycl;

int my_selector(const device& dev) {
    int score = -1;

    // We prefer non-Martian GPUs, especially ACME GPUs
    if (dev.is_gpu()) {
        if (dev.get_info<info::device::vendor>().find("ACME") != std::string::npos)
            score += 25;

        if (dev.get_info<info::device::vendor>().find(
            "Martian") == std::string::npos)
            score += 800;
    }

    // If there is no GPU on the system all devices will be
    // given a negative score and the selector will not select
    // a device. This will cause an exception.
    return score;
}

int main() {
    try {
        auto q = queue{my_selector};
        std::cout
            << "After checking for a GPU, we are running on:\n "
            << q.get_device().get_info<info::device::name>()
            << "\n";
    } catch (exception const& ex) {
        std::cout << "Custom device selector did not select a "
                "device.\n";
        std::cout << "Caught this SYCL exception: " << ex.what()
            << std::endl;
    }

    return 0;
}
Four Example Outputs (using four different systems, each with a GPU):
After checking for a GPU, we are running on:
Intel(R) Gen9 HD Graphics NEO.
After checking for a GPU, we are running on:
NVIDIA GeForce RTX 3060
After checking for a GPU, we are running on:
Intel(R) Data Center GPU Max 1100
After checking for a GPU, we are running on:
AMD Radeon RX 5700 XT

Example Output (using a system without GPU):
After checking for a GPU, we are running on:
Custom device selector did not select a device.
Caught this SYCL exception: No device of requested type available. ...(PI_ERROR_DEVICE_NOT_FOUND)
```

## Figure 12-4. Custom device selector—our preferred solution

## Being Curious: get\_info<>

In order for our program to “know” what devices are available at runtime, we can have our program query available devices from the device class, and then we can learn more details using get\_info<> to inquire about a specific device. We provide a simple program, called curious (see Figure 12-5), that uses these interfaces to dump out information for us to look at directly. This can be especially useful for doing a sanity check when developing or debugging a program that uses these interfaces. Failure of this program to work as expected can often tell us that the software drivers we need are not installed correctly. Figure 12-6 shows a sample output from this program, with the high-level information about the devices that are present.

You may want to see if your system supports a utility such as sycl-ls, before you write your own “list all available SYCL devices” program.

```cpp
// Loop through available platforms
for (auto const& this_platform :
    platform::get_platforms()) {
  std::cout
    << "Found platform: "
    << this_platform.get_info<info::platform::name>()
    << "\n";

  // Loop through available devices in this platform
  for (auto const& this_device :
        this_platform.get_devices()) {
    std::cout
      << " Device: "
      << this_device.get_info<info::device::name>()
      << "\n";
  }
  std::cout << "\n";
}
```

Figure 12-5. Simple use of device query mechanisms: curious.cpp

```txt
% clang++ -fsycl fig_12_5_curious.cpp -o curious

% ./curious
Found platform: NVIDIA CUDA BACKEND
  Device: NVIDIA GeForce RTX 3060

Found platform: AMD HIP BACKEND
  Device: AMD Radeon RX 5700 XT

Found platform: Intel(R) OpenCL
  Device: Intel(R) Xeon(R) E-2176G CPU @ 3.70GHz

Found platform: Intel(R) OpenCL HD Graphics
  Device: Intel(R) UHD Graphics P630 [0x3e96]

Found platform: Intel(R) Level-Zero
  Device: Intel(R) UHD Graphics P630 [0x3e96]

Found platform: Intel(R) FPGA Emulation Platform for OpenCL(TM)
  Device: Intel(R) FPGA Emulation Device
```  
Figure 12-6. Example output from curious.cpp

## Being More Curious: Detailed Enumeration Code

We offer a program, which we have named verycurious.cpp (Figure 12-7), to illustrate some of the detailed information available using get\_info. Again, we find ourselves writing code like this to help when developing or debugging a program.

Now that we have shown how to access the information, we will discuss the information fields that prove the most important to query and act upon in applications.

## Chapter 12 Device Information and Kernel Specialization

```cpp
template <typename queryT, typename T>
void do_query(const T& obj_to_query,
            const std::string& name, int indent = 4) {
    std::cout << std::string(indent, ' ') << name << " is '" 
            << obj_to_query.template get_info<queryT>() 
            << "`\n";
}

int main() {
    // Loop through the available platforms
    for (auto const& this_platform :
        platform::get_platforms()) {
        std::cout << "Found Platform:\n";
        do_query<info::platform::name>(this_platform,
                                    "info::platform::name");
        // query information like these (more in program than
        // shown here in this figure - see book github)

        // Loop through the devices available in this plaform
        for (auto& dev : this_platform.get_devices()) {
            std::cout << "   Device: "
                << dev.get_info<info::device::name>() 
                << "\n";
            // is_cpu() == has(aspect::cpu)
            std::cout << "      is_cpu(): "
                << (dev.is_cpu() ? "Yes" : "No") << "\n";
            // is_cpu() == has(aspect::gpu)
            std::cout << "      is_gpu(): "
                << (dev.is_gpu() ? "Yes" : "No") << "\n";
            std::cout << "      has(fp16): "
                << (dev.has(aspect::fp16) ? "Yes" : "No")
                << "\n";
            // many more queries shown in fig_12_7_very_curious.cpp
            // see book github for source code
        }
        std::cout << "\n";
    }
    return 0;
}
```

Figure 12-7. More detailed use of device query mechanisms: verycurious.cpp (subset shown)

## Very Curious: get\_info plus has()

The has() interface allows a program to test directly for a feature using aspects listed in Figure 12-3. Simple usage is shown in Figure 12-7—with more in the full verycurious.cpp source code in the book GitHub. The verycurious.cpp program is helpful for seeing the details about devices on your system.

## Device Information Descriptors

Our “curious” and “verycurious” program examples, used earlier in this chapter, utilize popular SYCL device class member functions (i.e., is\_cpu, is\_gpu, is\_accelerator, get\_info, has). These member functions are documented in the SYCL specification in a table titled “Member functions of the SYCL device class.”

The “curious” program examples also queried for information using the get\_info member function. There is a set of queries that must be supported by all SYCL devices. The complete list of such items is described in the SYCL specification in a table titled “Device information descriptors.”

## Device-Specific Kernel Information Descriptors

Like platforms and devices, we can query information about our kernels using a get\_info function. Such information (e.g., supported work-group sizes, preferred work-group size, the amount of private memory required per work-item) may be device-specific, and so the get\_info member function of the kernel class accepts a device as an argument.

## The Specifics: Those of “Correctness”

We will divide the specifics into information about necessary conditions (correctness) and information useful for tuning but not necessary for correctness.

In this first correctness category, we will enumerate conditions that should be met in order for kernels to launch properly. Failure to abide by these device limitations will lead to program failures. Figure 12-8 shows how we can fetch a few of these parameters in a way that the values are available for use in host code and in kernel code (via lambda capture). We can modify our code to utilize this information; for instance, it could guide our code on buffer sizing or work-group sizing.

```cpp
queue q;
device dev = q.get_device();

std::cout << "We are running on:\n"
       << dev.get_info<info::device::name>() << "\n";

// Query results like the following can be used to
// calculate how large your kernel invocations can be.
auto maxWG =
    dev.get_info<info::device::max_work_group_size>();
auto maxGmem =
    dev.get_info<info::device::global_mem_size>();
auto maxLmem =
    dev.get_info<info::device::local_mem_size>();

std::cout << "Max WG size is " << maxWG
       << "\nGlobal memory size is " << maxGmem
       << "\nLocal memory size is " << maxLmem << "\n";
```

Submitting a kernel that violates a required condition (e.g., sub\_group\_sizes) will generate a runtime error.

## Device Queries

device\_type: cpu, gpu, accelerator, custom,<sup>1</sup> automatic, all. These are most often tested by is\_cpu, is\_gpu(), and so on (see Figure 12-7):

max\_work\_item\_sizes: The maximum number of work-items that are permitted in each dimension of the work-group of the nd\_range. The minimum value is (1, 1, 1).

max\_work\_group\_size: The maximum number of work-items that are permitted in a work-group executing a kernel on a single compute unit. The minimum value is 1.

global\_mem\_size: The size of global memory in bytes.

local\_mem\_size: The size of local memory in bytes. The minimum size is 32 K.

max\_compute\_units: Indicative of the amount of parallelism available on a device—implementation-defined, interpret with care!

sub\_group\_sizes: Returns the set of sub-group sizes supported by the device.

Note that many more characteristics are encoded as aspects (see Figure 12-3), such as USM capabilities.

## WE STRONGLY ADVISE AVOIDING MAX\_COMPUTE\_UNITSIN PROGRAM LOGIC

We have found that querying the maximum number of compute units should be avoided, in part because the definition isn’t crisp enough to be useful in code tuning. Instead of using max\_compute\_units, most programs should express their parallelism and let the runtime map it onto available parallelism. Relying on max\_compute\_units for correctness only makes sense when augmented with implementation- and device-specific information. Experts might do that, but most developers do not and do not need to do so! Let the runtime do its job in this case!

## Kernel Queries

The mechanisms discussed in Chapter 10, under “Kernels in Kernel Bundles,” are needed to perform these kernel queries:

work\_group\_size: Returns the maximum workgroup size that can be used to execute a kernel on a specific device

compile\_work\_group\_size: Returns the work-group size specified by a kernel if applicable; otherwise returns (0, 0, 0)

compile\_sub\_group\_size: Returns the sub-group size specified by a kernel if applicable; otherwise returns 0

compile\_num\_sub\_groups: Returns the number of sub-groups specified by a kernel if applicable; otherwise returns 0

max\_sub\_group\_size: Returns the maximum subgroup size for a kernel launched with the specified work-group size

max\_num\_sub\_groups: Returns the maximum number of sub-groups for a kernel

# The Specifics: Those of “Tuning/ Optimization”

There are a few additional parameters that can be considered as finetuning parameters for our kernels. These can be ignored without jeopardizing the correctness of a program. These allow our kernels to really utilize the particulars of the hardware for performance.

Paying attention to the results of these queries can help when tuning for a cache (if it exists).

## Device Queries

global\_mem\_cache\_line\_size: Size of global memory cache line in bytes. global\_mem\_cache\_size: Size of global memory cache in bytes.

local\_mem\_type: The type of local memory supported. This can be info::local\_mem\_type::local implying dedicated local memory storage such as SRAM or info::local\_mem\_type::global. The latter type means that local memory is just implemented as an abstraction on top of global memory with potentially no performance gains.

## Kernel Queries

preferred\_work\_group\_size: The preferred work-group size for executing a kernel on a specific device.

preferred\_work\_group\_size\_multiple: Work-group size should be a multiple of this value (preferred\_work\_group\_size\_multiple) for executing a kernel on a particular device for best performance. The value must not be greater than work\_group\_size.

## Runtime vs. Compile-Time Properties

Implementations may offer compile-time constants/macros, or other functionality, but they are not standard and therefore we do not encourage their use nor do we discuss them in this book. The queries described in this chapter are performed through runtime APIs (get\_info) so the results are not known until runtime. In the next section, we discuss how attributes may be used to control how the kernel is compiled. Other than attributes, the SYCL standard promotes only the use of runtime information with one fairly esoteric exception. SYCL does offer two traits that the application can use to query aspects at compilation time. These traits are there specifically to help avoid instantiating a templated kernel for device features that are not supported by any device. This is a very advanced, and seldom used, feature we do not elaborate upon in this book. The SYCL standard has an example toward the end of the “Device aspects” section that shows the use of any\_device\_has\_v<aspect> and all\_devices\_have\_v<aspect> for this purpose. The standard also defines “specialization constants,” which we do not discuss in this book because they are typically used in very advanced targeted development, such as in libraries. An experimental compile-time property extension is discussed in the Epilogue under “Compile-Time Properties.”

## Kernel Specialization

We can specialize our kernels by having different kernels for different uses and select the appropriate kernel based on aspects (see Figure 12-3) of the device we are targeting. Of course, we can write specialized kernels explicitly and use C++ templating to help. We can inform the compiler that we want our kernel to use specific feature by using SYCL attributes (Figure 12-9) and aspects (Figure 12-3).

For example, the reqd\_work\_group\_size attribute (Figure 12-9) can be used to require a specific work-group size for a kernel, and the device\_has attribute can be used to require specific device aspects for a kernel.

Using attributes helps in two ways:

1. A kernel will throw an exception if it is submitted to a device that does not have one of the listed aspects.

2. The compiler will issue a diagnostic if the kernel (or any of the functions it calls) uses an optional feature (e.g., fp16) that is associated with an aspect that is not listed in the attribute.

The first helps prevent an application from proceeding if it will likely fail, and the second helps catch errors at compile time. For these reasons, using attributes can be helpful.

Figure 12-10 provides an example for illustration that uses run time logic to choose between two code sequences and uses attributes to specialize one of the kernels.

Chapter 12 Device Information and Kernel Specialization

<table><tr><td>Standard attribute</td><td>Specifies</td></tr><tr><td>device_has(aspect, ...)</td><td>This attribute is the only attribute that can be used to decorate a non-kernel function, in addition to the ability (of all attributes) to decorate a kernel function.Requires: that the kernel is only launched with devices meeting the specified aspect(s) from Figure 12-3).</td></tr><tr><td>reqd_work_group_size(dim0)reqd_work_group_size(dim0, dim1)reqd_work_group_size(dim0, dim1, dim2)</td><td>Requires: that the kernel must be launched with the specified workgroup size.</td></tr><tr><td>work_group_size_hint(dim0)work_group_size_hint(dim0, dim1)work_group_size_hint(dim0, dim1, dim2)</td><td>Hints: that the kernel will most likely be launched with the specified workgroup size.</td></tr><tr><td>reqd_sub_group_size(dim)</td><td>Requires: that the kernel must be compiled and executed with the specified sub-group size.</td></tr></table>

Figure 12-9. Attributes defined by the SYCL standard (and not deprecated)

```cpp
#include <iostream>
#include <sycl/sycl.hpp>
using namespace sycl;

int main() {
    queue q;

    constexpr int size = 16;
    std::array<double, size> data;

    // Using "sycl::device_has()" as an attribute does not
    // affect the device we select. Therefore, our host code
    // should check the device's aspects before submitting a
    // kernel which does require that attribute.
    if (q.get_device().has(aspect::fp64)) {
        buffer B{data};
        q.submit([&](handler& h) {
            accessor A{B, h};
            // the attributes here say that the kernel is allowed
            // to require fp64 support any attribute(s) from
            // Figure 12-3 could be specified note that namespace
            // stmt above (for C++) does not affect attributes (a
            // C++ quirk) so sycl:: is needed here
            h.parallel_for(
                size, [=](auto& idx)
                    [[sycl::device_has(aspect::fp64)]] {
                        A[idx] = idx * 2.0;
                        });
        });
        std::cout << "doubles were used\n";
    } else {
        // here we use an alternate method (not needing double
        // math support on the device) to help our code be
        // flexible and hence more portable
        std::array<float, size> fdata;
        {
            buffer B{fdata};
            q.submit([&](handler& h) {
                accessor A{B, h};
                h.parallel_for(
                    size, [=](auto& idx) { A[idx] = idx * 2.0f; });
            });
        }

        for (int i = 0; i < size; i++) data[i] = fdata[i];

        std::cout << "no doubles used\n";
    }
    for (int i = 0; i < size; i++)
        std::cout << "data[" << i << "] = " << data[i] << "\n";
    return 0;
}
```

## Figure 12-10. Specialization of kernel explicitly with the help of attributes

## Summary

The most portable programs will query the devices that are available in a system and adjust their behavior based on runtime information. This chapter opens the door to the rich set of information that is available to allow such tailoring of our code to adjust to the hardware that is present at runtime. We also discussed various ways to specialize kernels so they can be more closely adapted to a particular device type when we decide the investment is worthwhile. These give us the tools to balance portability and performance as necessary to meet our needs, all within the bounds of using C++ with SYCL.

Our programs can be made more functionally portable, more performance portable, and more future-proof by parameterizing our application to adjust to the characteristics of the hardware. We can also test that the hardware present falls within the bounds of any assumptions we have made in the design of our program and either warns or aborts when hardware is found that lies outside the bounds of our assumptions.

![](images/9c9e02adc798b9739ae69c632eef1d4eae72e03503264cfb5641c5392c22b26c.jpg)

cc 1 Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
````
