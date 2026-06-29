# CUDA Host-Device Lambda Performance

## Overview

`__host__ __device__` lambdas allow code to be executed on both the host and device. However, their performance characteristics on the host side differ from standard host-only lambdas due to how the CUDA compiler generates code for them.

## Indirect Function Call Mechanism

When an extended `__host__ __device__` lambda is defined in host code, the CUDA compiler replaces the lambda expression with an instance of a named placeholder type. Unlike `__device__`-only lambdas, which are not callable from the host, `__host__ __device__` lambdas can be invoked from host code.

The key implementation detail is that the placeholder type for an extended `__host__ __device__` lambda invokes the original lambda’s `operator()` using an **indirect function call** [CUDA_C_Programming_Guide:L18896-L18901].

## Performance Implications

The presence of the indirect function call has significant optimization consequences:

1.  **Inlining Difficulty**: The host compiler encounters an indirect call rather than a direct call to the lambda body. This prevents the host compiler from easily inlining the original `__host__ __device__` lambda body into the calling context [CUDA_C_Programming_Guide:L18896-L18901].
2.  **Comparison with Host-Only Lambdas**: In contrast, lambdas that are implicitly or explicitly `__host__` only allow the host compiler to easily inline the lambda body. This direct inlining capability often results in better optimization opportunities for host-only lambdas compared to their `__host__ __device__` counterparts [CUDA_C_Programming_Guide:L18896-L18901].

Consequently, an extended `__host__ __device__` lambda may be less optimized by the host compiler than a standard host-only lambda [CUDA_C_Programming_Guide:L18896-L18901].

## References

- CUDA C++ Programming Guide, Section 18.7.3: Notes on `__host__ __device__` lambdas [CUDA_C_Programming_Guide:L18896-L18901]
