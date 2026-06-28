## Backend Interoperability Hints and Tips

This section describes practical hints and tips to effectively use backend interoperability.

## Choosing a Device for a Specific Backend

The first requirement to properly use backend interoperability is to choose a SYCL device associated with the required SYCL backend. There are several ways to accomplish this.

The first is to integrate the required SYCL backend into existing custom device selection logic, by querying the associated backend while scoring each device. If our application is already using custom device selection logic, this should be a straightforward addition. This mechanism is also portable because it uses only standard SYCL queries.

For applications that do not already use custom device selection logic, we can write a short C++ lambda expression to iterate over all devices to find a device with the requested backend, as shown in Figure 20-11. Because this version of find\_device does not request a specific device type, it is effectively a replacement for the standard default\_selector\_v.

```cpp
#include <iostream>
#include <sycl/sycl.hpp>
using namespace sycl;

int main() {
    auto find_device = [](backend b,
                          info::device_type t =
                          info::device_type::all) {
        for (auto d : device::get_devices(t)) {
            if (d.get_backend() == b) {
                return d;
            }
        }
        throw sycl::exception(errc::runtime,
                          "Could not find a device with "
                          "the requested backend!");
    };

    try {
        device d{find_device-backend::opencl});
        std::cout << "Found an OpenCL SYCL device: "
                          << d.get_info<info::device::name>() << "\n";
    } catch (const sycl::exception &e) {
        std::cout << "No OpenCL SYCL devices were found.\n";
    }

    try {
        device d{find_device-backend::ext_oneapi_level_zero});
        std::cout << "Found a Level Zero SYCL device: "
                          << d.get_info<info::device::name>() << "\n";
    } catch (const sycl::exception &e) {
        std::cout << "No Level Zero SYCL devices were found.\n";
    }

    return 0;
}
```  
Figure 20-11. Finding a SYCL device with a specific backend

Finally, for fast prototyping some SYCL implementations can use external mechanisms, such as environment variables, to influence the SYCL devices they enumerate. As an example, the DPC++ SYCL runtime can use the ONEAPI\_DEVICE\_SELECTOR environment variable to limit enumerated devices to specific device types or associated device backends (refer to Chapter 13). This is not an ideal solution for production code

because it requires external configuration, but it is a useful mechanism for prototype code to ensure that an application is using a specific device from a specific backend.

## Be Careful About Contexts!

Recall from Chapters 6 and 13 that many SYCL objects, such as kernels and USM allocations, are generally not accessible by a SYCL context if they were created in a different SYCL context. This is still true when using backend interoperability; therefore, a backend-specific context created using a backend API generally will not have access to objects created in a different SYCL context (and vice versa) even if the SYCL context is associated with the same backend.

To safely share objects between SYCL and a backend, we should always either create our SYCL context from a native backend context using make\_context, or we should get a native backend context from a SYCL context using get\_native.

Always create a SYCL context from a native backend context or get a native backend context from a SYCL context to safely share objects between SYCL and a backend!

## Access Low-Level API-Specific Features

Occasionally a cutting-edge feature will be available in a low-level API before it is available in SYCL, even as a SYCL extension. Some features may even be so backend-specific or so device-specific that they will never be exposed through SYCL. For example, some native backend APIs may provide access to queues with specific properties or unique kernel instructions for specific accelerator hardware. Although we hope and expect these cases to be rare, when these types of features exist, we may still gain access to them using backend interoperability.

## Support for Other Backends

The examples in this chapter demonstrated backend interoperability with OpenCL and Level Zero backends, but SYCL is a growing ecosystem and SYCL implementations are regularly adding support for additional backends and devices. For example, several SYCL implementations supporting CUDA and HIP backends already have some support for interoperability with these backends. Check the documentation for a SYCL implementation to determine which SYCL backends are supported and whether they support backend interoperability!

## Summary

In this chapter, we discovered how each SYCL object is associated with an underlying SYCL backend and how to query the SYCL backends in a system. We described how backend interoperability provides a mechanism for our SYCL application to directly interact with an underlying backend API. We discussed how this enables us to incrementally add SYCL to an application that is directly using a backend API, or to reuse libraries or utility functions written specifically for a backend API. We also discussed how backend interoperability reduces application portability, by restricting which SYCL devices the application will run on.

We specifically explored how backend interoperability for kernels provides similar functionality in SYCL 2020 that was present in earlier versions of SYCL. We examined how an online compiler extension can enable the use of some source languages for kernels, even if they are not directly understood by some SYCL backends.

## Chapter 20 Backend Interoperabi lity

Finally, we reviewed practical hints and tips to effectively use backend interoperability in our programs, such as how to choose a SYCL device for a specific SYCL backend, how to set up a SYCL context for backend interoperability, and how backend interoperability can provide access to features even if they have not been added to SYCL.

![](images/5a33a92a6019c42eaae871e4ad3660c775f08d99947a920f6697e9b18e9a7473.jpg)

cc Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.

# Migrating CUDA Code
