# Virtual Base Classes in CUDA

## Overview
In CUDA C++, there are specific restrictions regarding the use of C++ inheritance features within device code, particularly when interacting with the host-to-device execution model via kernel launches.

## Restrictions on Virtual Inheritance
It is not allowed to pass as an argument to a `__global__` function an object of a class derived from virtual base classes [CUDA_C_Programming_Guide:L17321-L17327]. This restriction applies to the data passed from the host to the device during kernel execution.

## Platform-Specific Constraints
Additional constraints may apply when using the Microsoft host compiler on Windows. Users should refer to the Windows-Specific documentation for further details on compiler-specific limitations regarding virtual base classes [CUDA_C_Programming_Guide:L17321-L17327].
