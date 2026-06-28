## Choosing Devices

To explore the mechanisms that let us control where device code will execute, we’ll look at five use cases:

Method#1: Running device code somewhere when we don’t care which device is used. This is often the first step in development because it is the simplest.

Method#2: Explicitly running device code on a CPU device, which is often used for debugging because most development systems have an accessible CPU. CPU debuggers are also typically very rich in features.

Method#3: Dispatching device code to a GPU or other accelerator.

Method#4: Dispatching device code to a heterogeneous set of devices, such as a GPU and an FPGA.

Method#5: Selecting specific devices from a more general class of devices, such as a specific type of FPGA from a collection of available FPGA types.

Developers will typically debug their code as much as possible with Method#2 and only move to Methods #3–#5 when code has been tested as much as is practical with Method#2.

## Method#1: Run on a Device of Any Type

When we don’t care where our device code will run, it is easy to let the runtime pick for us. This automatic selection is designed to make it easy to start writing and running code, when we don’t yet care about what device is chosen. This device selection does not take into account the code to be run, so should be considered an arbitrary choice which likely won’t be optimal.

Before talking about choice of a device, even one that the implementation has selected for us, we should first cover the mechanism through which a program interacts with a device: the queue.

## Queues

A queue is an abstraction to which actions are submitted for execution on a single device. A simplified definition of the queue class is given in Figures 2-3 and 2-4. Actions are usually the launch of data-parallel compute, although other commands are also available such as manual control of data motion for when we want more control than the automatic movement provided by the SYCL runtime. Work submitted to a queue can execute after prerequisites tracked by the runtime are met, such as availability of input data. These prerequisites are covered in Chapters 3 and 8.

```cpp
CHAPTER 2 WHERE CODE EXECUTES

class queue {
public:
    // Create a queue associated with a default
    // (implementation chosen) device.
    queue(const property_list & = {});

    queue(const async_handler &, const property_list & = {});

    // Create a queue using a DeviceSelector.
    // A DeviceSelector is a callable that ranks
    // devices numerically. There are a few SYCL-defined
    // device selectors available such as
    // cpu_selector_v and gpu_selector_v.
    template <typename DeviceSelector>
    explicit queue(const DeviceSelector &deviceSelector,
                    const property_list &propList = {});

    // Create a queue associated with an explicit device to
    // which the program already holds a reference.
    queue(const device &, const property_list & = {});

    // Create a queue associated with a device in a specific
    // SYCL context. A device selector may be used in place
    // of a device.
    queue(const context &, const device &, const property_list & = {});
};
```

## Figure 2-3. Simplified definition of some constructors of the queue class

```cpp
class queue {
public:
  // Submit a command group to this queue.
  // The command group may be a lambda expression or
  // function object. Returns an event reflecting the status
  // of the action performed in the command group.
  template <typename T>
  event submit(T);

  // Wait for all previously submitted actions to finish
  // executing.
  void wait();

  // Wait for all previously submitted actions to finish
  // executing. Pass asynchronous exceptions to an
  // async_handler function.
  void wait_and_throw();
};
```

## Figure 2-4. Simplified definition of some key member functions in the queue class

A queue is bound to a single device, and that binding occurs on construction of the queue. It is important to understand that work submitted to a queue is executed on the single device to which that queue is bound. Queues cannot be mapped to collections of devices because that would create ambiguity on which device should perform work. Similarly, a queue cannot spread the work submitted to it across multiple devices. Instead, there is an unambiguous mapping between a queue and the device on which work submitted to that queue will execute, as shown in Figure 2-5.

![](images/fcf2819045bd1314674c361b03f769aeef1912cac43acd8701f4a3c0a68c2c72.jpg)  
Figure 2-5. A queue is bound to a single device. Work submitted to the queue executes on that device

Multiple queues may be created in a program, in any way that we desire for application architecture or programming style. For example, multiple queues may be created to each bind with a different device or to be used by different threads in a host program. Multiple different queues can be bound to a single device, such as a GPU, and submissions to those different queues will result in the combined work being performed on the device. An example of this is shown in Figure 2-6. Conversely, as we mentioned previously, a queue cannot be bound to more than one device because there must not be any ambiguity on where an action is being requested to execute. If we want a queue that will load balance work across multiple devices, for example, then we can create that abstraction in our code.

![](images/5d581d48ce98bc667317bfa3ab64067cd399e7cd7fc178fc156c859f54e70022.jpg)  
Figure 2-6. Multiple queues can be bound to a single device

Because a queue is bound to a specific device, queue construction is the most common way in code to choose the device on which actions submitted to the queue will execute. Selection of the device when constructing a queue is achieved through a device selector abstraction.

## Binding a Queue to a Device When Any Device Will Do

Figure 2-7 is an example where the device that a queue should bind to is not specified. The default queue constructor that does not take any arguments (as in Figure 2-7) simply chooses some available device behind the scenes. SYCL guarantees that at least one device will always be available, so some device will always be selected by this default selection mechanism. In many cases the selected device may happen to be a CPU which is also executing the host program, although this is not guaranteed.

## Chapter 2 Where Code Executes

```cpp
#include <iostream>
#include <sycl/sycl.hpp>
using namespace sycl;

int main() {
    // Create queue on whatever default device that the
    // implementation chooses. Implicit use of
    // default_selector_v
    queue q;

    std::cout << "Selected device: "
            << q.get_device().get_info<info::device::name>()
            << "\n";

    return 0;
}

Sample Outputs (one Line per run depending on system):
Selected device: NVIDIA GeForce RTX 3060
Selected device: AMD Radeon RX 5700 XT
Selected device: Intel(R) Data Center GPU Max 1100
Selected device: Intel(R) FPGA Emulation Device
Selected device: AMD Ryzen 5 3600 6-Core Processor
Selected device: Intel(R) UHD Graphics 770
Selected device: Intel(R) Xeon(R) Gold 6128 CPU @ 3.40GHz
Selected device: 11th Gen Intel(R) Core(TM) i9-11900KB @ 3.30GHz
many more possible... these are only examples
```  
Figure 2-7. Implicit default device selector through default construction of a queue

Using the trivial queue constructor is a simple way to begin application development and to get device code up and running. More control over selection of the device bound to a queue can be added as it becomes relevant for our application.

## Method#2: Using a CPU Device for Development, Debugging, and Deployment

A CPU device can be thought of as enabling the host CPU to act as if it was an independent device, allowing our device code to execute regardless of the accelerators available in a system. We always have some processor running the host program, so a CPU device is therefore usually available to our application (very occasionally a CPU might not be exposed as a SYCL device by an implementation, for a variety of reasons). Using a CPU device for code development has a few advantages:

1. Development of device code on less capable systems that don’t have any accelerators: One common use is development and testing of device code on a local system, before deploying to an HPC cluster for performance testing and optimization.

2. Debugging of device code with non-accelerator tooling: Accelerators are often exposed through lower-level APIs that may not have debug tooling as advanced as is available for host CPUs. With this in mind, a CPU device often supports debugging using standard tools familiar to developers.

3. Backup if no other devices are available, to guarantee that device code can be executed functionally: A CPU device may not have performance as a primary goal, or may not match the architecture for which kernel code was optimized, but can often be considered as a functional backup to ensure that device code can always execute in any application.

It should not be a surprise to find that multiple CPU devices are available to a SYCL application, with some aimed at ease of debugging while others may be focused on execution performance. Device aspects can be used to differentiate between these different CPU devices, as described later in this chapter.

When considering use of a CPU device for development and debugging of device code, some consideration should be given to differences between the CPU and a target accelerator architecture (e.g., GPU). Especially

when optimizing code performance, and particularly when using more advanced features such as sub-groups, there can be some differences in functionality and performance across architectures. For example, the subgroup size may change when moving to a new device. Most development and debugging can typically occur on a CPU device, sometimes followed by final tuning and debugging on the target device architecture.

A CPU device is functionally like a hardware accelerator in that a queue can bind to it and it can execute device code. Figure 2-8 shows how the CPU device is a peer to other accelerators that might be available in a system. It can execute device code, in the same way that a GPU or FPGA is able to, and can have one or more queues constructed that bind to it.

![](images/473ebef8134609b4c188a9116f9d8c51608b03ef58a4ae77e6fb58f33ea35c9d.jpg)  
Figure 2-8. A CPU device can execute device code like any accelerator

An application can choose to create a queue that is bound to a CPU device by explicitly passing cpu\_selector\_v to a queue constructor, as shown in Figure 2-9.

```cpp
#include <iostream>
#include <sycl/sycl.hpp>
using namespace sycl;

int main() {
  // Create queue to use the CPU device explicitly
  queue q{cpu_selector_v};

  std::cout << "Selected device: "
              << q.get_device().get_info<info::device::name>()
              << "\n";
  std::cout
    << " -> Device vendor: "
    << q.get_device().get_info<info::device::vendor>()
    << "\n";

  return 0;
}

Example Output:
Selected device: Intel(R) Xeon(R) Gold 6128 CPU @ 3.40GHz
-> Device vendor: Intel(R) Corporation
```  
Figure 2-9. Selecting the host device using the cpu\_selector\_v

Even when not specifically requested (e.g., using cpu\_selector\_v), the CPU device might happen to be chosen by the default selector as occurred in the output in Figure 2-7.

A few variants of device selectors are defined to make it easy for us to target a type of device. The cpu\_selector\_v is one example of these selectors, and we’ll get into others in the coming sections.

## Method#3: Using a GPU (or Other Accelerators)

GPUs are showcased in the next example, but any type of accelerator applies equally. To make it easy to target common classes of accelerators, devices are grouped into several broad categories, and SYCL provides built-in selector classes for them. To choose from a broad category of device type such as “any GPU available in the system,” the corresponding code is very brief, as described in this section.

## Accelerator Devices

In the terminology of the SYCL specification, there are a few broad groups of accelerator types:

1. CPU devices.

2. GPU devices.

3. Accelerators, which capture devices that don’t identify as either a CPU device or a GPU. This includes FPGA and DSP devices.

A device from any of these categories is easy to bind to a queue using built-in selectors, which can be passed to queue (and some other class) constructors.

## Device Selectors

Classes that must be bound to a specific device, such as the queue class, have constructors that can accept a DeviceSelector. A DeviceSelector is a callable taking a const reference to a device, and which ranks it numerically so that the runtime can choose a device with the highest ranking. For example, one queue constructor which accepts a DeviceSelector is queue(const DeviceSelector &deviceSelector, const property\_list &propList = {});

There are four built-in selectors for the broad classes of common devices.

<table><tr><td>default_selector_v</td><td>Any device of the implementation&#x27;s choosing</td></tr><tr><td>cpu_selector_v</td><td>Select a device that identifies itself as a CPU in device queries</td></tr><tr><td>gpu_selector_v</td><td>Select a device that identifies itself as a GPU in device queries</td></tr><tr><td>accelerator_selector_v</td><td>Select a device that identifies itself as an “accelerator,” which includes FPGAs</td></tr></table>

```javascript
queue myQueue{ gpu_selector_v{} };
```

One additional selector included in DPC++ (not available in SYCL) is available by including the header "sycl/ext/intel/fpga\_ extensions.hpp".

```txt
ext::intel::fpga_selector_v Select a device that identifies itself as an FPGA
```

A queue can be constructed using one of the built-in selectors, such as

Figure 2-10 shows a complete example using the GPU selector, and Figure 2-11 shows the corresponding binding of a queue with an available GPU device.

Figure 2-12 shows an example using a variety of built-in selectors and demonstrates use of device selectors with another class (device) that accepts a device selector on construction.

```cpp
#include <iostream>
#include <sycl/sycl.hpp>
using namespace sycl;

int main() {
  // Create queue bound to an available GPU device
  queue q{gpu_selector_v};

  std::cout << "Selected device: "
              << q.get_device().get_info<info::device::name>()
              << "\n";
  std::cout
    << " -> Device vendor: "
    << q.get_device().get_info<info::device::vendor>()
    << "\n";

  return 0;
}

Example Output:
Selected device: AMD Radeon RX 5700 XT
  -> Device vendor: AMD Corporation
```  
Figure 2-10. GPU device selector example

![](images/db802db0a80cdf36491acdf9340ad1b152865ff4330742b29fa27e266ea99d0d.jpg)  
Figure 2-11. Queue bound to a GPU device available to the application

```cpp
#include <iostream>
#include <string>
#include <sycl/ext/intel/fpga_extensions.hpp>  // For fpga_selector_v
#include <sycl/sycl.hpp>
using namespace sycl;

void output_dev_info(const device& dev,
                    const std::string& selector_name) {
  std::cout << selector_name << ": Selected device: "
              << dev.get_info<info::device::name>() << "\n";
  std::cout << "                  -> Device vendor: "
              << dev.get_info<info::device::vendor>() << "\n";
}

int main() {
  output_dev_info(device{default_selector_v},
                   "default_selector_v");
  output_dev_info(device{cpu_selector_v}, "cpu_selector_v");
  output_dev_info(device{gpu_selector_v}, "gpu_selector_v");
  output_dev_info(device{accelerator_selector_v},
                   "accelerator_selector_v");
  output_dev_info(device{ext::intel::fpga_selector_v},
                   "fpga_selector_v");

  return 0;
}

Example Output:
default_selector_v: Selected device: Intel(R) UHD Graphics [0x9a60]
      -> Device vendor: Intel(R) Corporation
cpu_selector_v: Selected device: 11th Gen Intel(R) Core(TM) i9-11900KB @ 3.30GHz
      -> Device vendor: Intel(R) Corporation
gpu_selector_v: Selected device: Intel(R) UHD Graphics [0x9a60]
      -> Device vendor: Intel(R) Corporation
accelerator_selector_v: Selected device: Intel(R) FPGA Emulation Device
      -> Device vendor: Intel(R) Corporation
fpga_selector_v: Selected device: pac_a10 : Intel PAC Platform (pac_ee00000)
      -> Device vendor: Intel Corp
```

Figure 2-12. Example device identification output from various classes of device selectors and demonstration that device selectors can be used for construction of more than just a queue (in this case, construction of a device class instance)

## When Device Selection Fails

If a GPU selector is used when creating an object such as a queue and if there are no GPU devices available to the runtime, then the selector throws a runtime\_error exception. This is true for all device selector classes in that if no device of the required class is available, then a runtime\_error

exception is thrown. It is reasonable for complex applications to catch that error and instead acquire a less desirable (for the application/algorithm) device class as an alternative. Exceptions and error handling are discussed in more detail in Chapter 5.
