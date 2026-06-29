# Constexpr Functions in CUDA

## Execution Space Restrictions

By default, a `constexpr` function cannot be called from a function with an incompatible execution space [CUDA_C_Programming_Guide:L17619-L17622]. This restriction ensures that compile-time evaluation occurs within the appropriate context (host or device).

## Relaxed Constexpr Mode

The experimental `nvcc` flag `--expt-relaxed-constexpr` removes the restriction on incompatible execution spaces [CUDA_C_Programming_Guide:L17619-L17622]. When this flag is specified:

*   Host code can invoke a `__device__` constexpr function.
*   Device code can invoke a `__host__` constexpr function [CUDA_C_Programming_Guide:L17619-L17622].

When `--expt-relaxed-constexpr` is enabled, the compiler defines the macro `__CUDACC_RELAXED_CONSTEXPR__` [CUDA_C_Programming_Guide:L17619-L17622].

## Function Templates

A function template instantiation may not be a `constexpr` function even if the corresponding template is marked with the keyword `constexpr` [CUDA_C_Programming_Guide:L17619-L17622]. This behavior aligns with the C++11 Standard Section [dcl.constexpr.p6].
