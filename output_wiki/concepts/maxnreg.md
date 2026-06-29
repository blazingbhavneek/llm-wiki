# __maxnreg__

The `__maxnreg__()` function qualifier is a CUDA C++ feature designed to provide a mechanism for low-level performance tuning by passing specific information to the backend optimizing compiler [CUDA_C_Programming_Guide:L11688-L11688].

## Purpose and Functionality

The `__maxnreg__()` qualifier specifies the maximum number of registers to be allocated to a single thread within a thread block [CUDA_C_Programming_Guide:L11688-L11688]. When applied to a kernel, the specified value compiles to the `.maxnreg` PTX directive [CUDA_C_Programming_Guide:L11699-L11699].

### Usage Example

In the definition of a `__global__` function, the qualifier is used as follows:

```cpp
__global__ void __maxnreg__(maxNumberRegistersPerThread) MyKernel() {
    // Kernel body
}
```

Here, `maxNumberRegistersPerThread` specifies the maximum number of registers to be allocated to a single thread in the thread block of the kernel `MyKernel()` [CUDA_C_Programming_Guide:L11699-L11699].

## Constraints and Interactions

### Incompatibility with `__launch_bounds__`

The `__launch_bounds__()` and `__maxnreg__()` qualifiers cannot be applied to the same kernel [CUDA_C_Programming_Guide:L11701-L11701].

### Interaction with Compiler Options

Register usage can be controlled for all `__global__` functions in a file using the `maxrregcount` compiler option. However, the value of `maxrregcount` is ignored for functions that have the `__maxnreg__` qualifier [CUDA_C_Programming_Guide:L11703-L11703]. This ensures that the explicit register limit defined by `__maxnreg__` takes precedence over global compiler settings for that specific function.

## References

- CUDA C++ Programming Guide, Section 10.39: Maximum Number of Registers per Thread [CUDA_C_Programming_Guide:L11686-L11686]
