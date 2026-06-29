# CUDA Extended Lambda MSVC Restrictions

When compiling CUDA code with Visual Studio host compilers, specific restrictions apply to the use of extended lambdas. These limitations arise from how the host compiler interacts with CUDA compiler transformations.

## External Linkage Requirement

The enclosing function of an extended lambda must have external linkage when using Visual Studio host compilers [CUDA_C_Programming_Guide:L18638-L18641].

This restriction exists because the Visual Studio host compiler does not support using the address of functions with non-external linkage as template arguments. This capability is required by the CUDA compiler transformations that enable extended lambda functionality [CUDA_C_Programming_Guide:L18638-L18641].

## Prohibition on `if-constexpr` Blocks

An extended lambda shall not be defined within the body of an `if-constexpr` block when using Visual Studio host compilers [CUDA_C_Programming_Guide:L18638-L18641].
