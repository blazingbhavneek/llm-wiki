# Standard Library

Standard libraries are only supported in host code, but not in device code, unless specified otherwise [CUDA_C_Programming_Guide:L16882-L16885].

## Scope

This restriction applies to the standard library implementations within the CUDA C++ programming environment. Developers must ensure that standard library features are utilized in host-side execution contexts unless specific exceptions are documented [CUDA_C_Programming_Guide:L16882-L16885].
