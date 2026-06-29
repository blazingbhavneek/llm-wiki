# Intel Host Compiler Specifics in CUDA

The CUDA frontend compiler parser does not recognize some of the intrinsic functions supported by the Intel compiler (e.g., icc) [CUDA_C_Programming_Guide:L17528-L17530]. 

When using the Intel compiler as a host compiler, nvcc will therefore enable the macro `__INTEL_COMPILER_USE_INTRINSIC_PROTOTYPES` during preprocessing [CUDA_C_Programming_Guide:L17528-L17530]. This macro enables explicit declarations of the Intel compiler intrinsic functions in the associated header files, allowing nvcc to support use of such functions in host code [CUDA_C_Programming_Guide:L17528-L17530].
