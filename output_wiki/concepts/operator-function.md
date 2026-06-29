# Operator Function

In CUDA C++, an operator function is a special member function that defines the behavior of operators for user-defined types. A key constraint on operator functions is that they cannot be declared as `__global__` functions [CUDA_C_Programming_Guide:L17267-L17270]. This restriction applies regardless of whether the operator is intended for host or device execution, meaning operator overloads must be implemented as host functions, device functions, or both, but never as kernels [CUDA_C_Programming_Guide:L17267-L17270].

## Key Constraints

- **No `__global__` Qualifier**: Operator functions cannot be marked with the `__global__` execution space specifier [CUDA_C_Programming_Guide:L17267-L17270].
- **Execution Space**: While they cannot be kernels, operator functions can be defined as `__device__`, `__host__`, or both, allowing them to be used in device code and host code respectively [CUDA_C_Programming_Guide:L17267-L17270].

## Usage

Operator functions are typically used to enable natural syntax for arithmetic, comparison, and other operations on custom classes or structs within CUDA device code. Since they cannot be `__global__`, they are invoked implicitly by the compiler when an operator is used on an instance of the type, rather than being launched as a kernel.

## See Also

- [CUDA C++ Programming Guide: Device Functions](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#device-functions)
- [CUDA C++ Programming Guide: User-Defined Types](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#user-defined-types)
