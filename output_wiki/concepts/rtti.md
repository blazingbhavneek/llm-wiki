# Run Time Type Information (RTTI)

Run Time Type Information (RTTI) provides mechanisms for inspecting object types during program execution. In the context of CUDA C/C++ programming, support for RTTI is restricted to the host environment.

## Supported Features

The following RTTI-related features are supported in host code, but not in device code:

* `typeid` operator
* `std::type_info`
* `dynamic_cast` operator

These limitations apply to code executed on the GPU (device code), where type introspection capabilities are not available. Developers must ensure that RTTI-dependent logic is confined to the host side of the application.

[CUDA_C_Programming_Guide:L16867-L16876]
