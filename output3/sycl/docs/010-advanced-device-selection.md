## Method#4: Using Multiple Devices

As shown in Figures 2-5 and 2-6, we can construct multiple queues in an application. We can bind these queues to a single device (the sum of work to the queues is funneled into the single device), to multiple devices, or to some combination of these. Figure 2-13 provides an example that creates one queue bound to a GPU and another queue bound to an FPGA. The corresponding mapping is shown graphically in Figure 2-14.

![](images/b1c52ac83ede5c4ba1098869d00854e205041abedc688acb5b9a914bb9b33133.jpg)  
Figure 2-13. Creating queues to both GPU and FPGA devices

![](images/0842312eba36f480281fab1eb5f69d9693518fe1d5200311be84f3733045337b.jpg)  
Figure 2-14. GPU + FPGA device selector example: One queue is bound to a GPU and another to an FPGA

## Method#5: Custom (Very Specific) Device Selection

We will now look at how to write a custom selector. In addition to examples in this chapter, there are a few more examples shown in Chapter 12. The built-in device selectors are intended to let us get code up and running quickly. Real applications usually require specialized selection of a device, such as picking a desired GPU from a set of GPU types available in a system. The device selection mechanism is easily extended to arbitrarily complex logic, so we can write whatever code is required to choose the device that we prefer.

## Selection Based on Device Aspects

SYCL defines properties of devices known as aspects. For example, some aspects that a device might exhibit (return true on aspect queries) are gpu, host\_debuggable, fp64, and online\_compiler. Please refer to the “Device

Aspects” section of the SYCL specification for a full list of standard aspects, and their definitions.

To select a device using aspects defined in SYCL, the aspect\_selector can be used as shown in Figure 2-15. In the form of aspect\_selector taking a comma-delimited group of aspects, all aspects must be exhibited by a device for the device to be selected. An alternate form of aspect\_ selector takes two std::vectors. The first vector contains aspects that must be present in a device, and the second vector contains aspects that must not be present in a device (lists negative aspects). Figure 2-15 shows an example of using both of these forms of aspect\_selector.

```cpp
#include <iostream>
#include <sycl/sycl.hpp>
using namespace sycl;

int main() {
    // In the aspect_selector form taking a comma seperated
    // group of aspects, all aspects must be present for a
    // device to be selected.
    queue q1{aspect_selector(aspect::fp16, aspect::gpu));

    // In the aspect_selector form that takes two vectors, the
    // first vector contains aspects that a device must
    // exhibit, and the second contains aspects that must NOT
    // be exhibited.
    queue q2{aspect_selector(
        std::vector{aspect::fp64, aspect::fp16},
        std::vector{aspect::gpu, aspect::accelerator})};

    std::cout
        << "First selected device is: "
        << q1.get_device().get_info<info::device::name>()
        << "\n";

    std::cout
        << "Second selected device is: "
        << q2.get_device().get_info<info::device::name>()
        << "\n";

    return 0;
}

Example Output:
First selected device is: Intel(R) UHD Graphics [0x9a60]
Second selected device is: 11th Gen Intel(R) Core(TM) i9-11900KB @ 3.30GHz
```  
Figure 2-15. Aspect selector

Some aspects may be used to infer performance characteristics of a device. For example, any device with the emulated aspect may not perform as well as a device of the same type, which is not emulated, but may instead exhibit other aspects related to improved debuggability.

## Selection Through a Custom Selector

When existing aspects aren’t sufficient for selection of a specific device, a custom device selector may be defined. Such a selector is simply a C++ callable (e.g., a function or lambda) that takes a const Device& as a parameter and that returns an integer score for the specific device. The SYCL runtime invokes the selector on all available root devices that can be found and chooses the device for which the selector returned the highest score (which must be nonnegative for selection to occur).

In cases where there is a tie for the highest score, the SYCL runtime will choose one of the tied devices. No device for which the selector returned a negative number will be chosen by the runtime, so returning a negative number from a selector guarantees that the device will not be selected.

## Mechanisms to Score a Device

We have many options to create an integer score corresponding to a specific device, such as the following:

1. Return a positive value for a specific device class.

2. String match on a device name and/or device vendor strings.

3. Compute anything that we can imagine leading to an integer value, based on device or platform queries.

For example, one possible approach to select a specific Intel Arria FPGA accelerator board is shown in Figure 2-16.

## Chapter 2 Where Code Executes

```rust
int my_selector(const device &dev) {
    if (dev.get_info<info::device::name%).find("pac_a10") !=
        std::string::npos &&
        dev.get_info<info::device::vendor().find("Intel") !=
        std::string::npos) {
        return 1;
    }
    return -1;
}

Example Output:
Selected device is: pac_a10 : Intel PAC Platform (pac_ee00000)
```
