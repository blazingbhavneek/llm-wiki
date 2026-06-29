# CUDA Toolkit Device Runtime Inclusion

## Overview

In the context of CUDA Toolkit support for dynamic parallelism, the management of the device runtime API differs from typical C/C++ header usage. Similar to the host-side runtime API, the CUDA development environment handles the inclusion of necessary definitions automatically.

## Automatic Inclusion

Developers do not need to explicitly include the `cuda_device_runtime_api.h` header file in their CUDA code. The prototypes for the CUDA device runtime API are included automatically during the program compilation process [CUDA_C_Programming_Guide:L14120-L14125].

This automatic inclusion simplifies code structure when utilizing dynamic parallelism features, as the compiler ensures that the device runtime API prototypes are available without manual header directives.

## Related Concepts

- **Host-Side Runtime API**: The automatic inclusion behavior mirrors that of the host-side CUDA runtime API.
- **Dynamic Parallelism**: This feature is part of the broader toolkit support for dynamic parallelism, allowing kernels to launch other kernels from within device code.

## Caveats

- While explicit inclusion is not required, developers should ensure they are compiling with flags that enable dynamic parallelism (e.g., `-rdc=true`) if they intend to use device runtime API functions, as the automatic inclusion is tied to the compilation context that supports these features.
- The automatic inclusion applies to the *prototypes* of the API. Linking against the device runtime library may still require specific linker flags depending on the build configuration.

## References

- CUDA C++ Programming Guide, Section 13.3.3.1: Including Device Runtime API in CUDA Code [CUDA_C_Programming_Guide:L14120-L14125]
