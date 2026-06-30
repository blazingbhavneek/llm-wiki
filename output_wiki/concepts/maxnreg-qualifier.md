# 10.39. Maximum Number of Registers per Thread

Covers the __maxnreg__() qualifier for limiting register allocation per thread, its incompatibility with __launch_bounds__(), and the maxrregcount compiler option.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L11686-L11704

Citation: [CUDA_C_Programming_Guide:L11686-L11704]

````text
# 10.39. Maximum Number of Registers per Thread

To provide a mechanism for low-level performance tuning, CUDA C++ provides the \_\_maxnreg\_\_() function qualifier to pass performance tuning information to the backend optimizing compiler. The \_maxnreg\_\_() qualifier specifies the maximum number of registers to be allocated to a single thread in a thread block. In the definition of a \_\_global\_\_ function:

```lisp
__global__ void
__maxnreg__(maxNumberRegistersPerThread)
MyKernel(...)
{
    ...
}
```

▶ maxNumberRegistersPerThread specifies the maximum number of registers to be allocated to a single thread in a thread block of the kernel MyKernel(); it compiles to the .maxnregPTX directive.

The \_\_launch\_bounds\_\_() and \_\_maxnreg\_\_() qualifiers cannot be applied to the same kernel.

Register usage can also be controlled for all \_\_global\_\_ functions in a file using the maxrregcount compiler option. The value of maxrregcount is ignored for functions with the \_\_maxnreg\_\_ qualifier.
````
