# Function Recursion

In the context of CUDA programming, recursion is a capability that is restricted based on the function's execution space. Specifically, **__global__ functions do not support recursion** [CUDA_C_Programming_Guide:L17239-L17242].

This limitation is defined under the section regarding function recursion constraints in the CUDA C++ Programming Guide [CUDA_C_Programming_Guide:L17239-L17242]. Developers must ensure that device code called from __global__ functions does not rely on recursive calls within the __global__ function itself, as this is not supported by the compiler and runtime environment.

## See Also

- CUDA C++ Programming Guide: Function Recursion section
- __global__ function execution model
