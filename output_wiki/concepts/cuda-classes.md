# Classes in CUDA

CUDA provides support for C++ classes, allowing developers to encapsulate data and behavior within device code. However, certain C++ features are restricted or unsupported to maintain compatibility with the GPU execution model.

## Data Members

Static data members are generally not supported in CUDA device code. The only exception is for static data members that are also `const`-qualified. Non-const static members cannot be used in device functions [CUDA_C_Programming_Guide:L17279-L17280].

## Function Members

Static member functions are supported, but they cannot be declared as `__global__` functions. This restriction applies because `__global__` functions are entry points for kernel launches and have specific calling conventions that are incompatible with static member function semantics in this context [CUDA_C_Programming_Guide:L17281-L17283].

## Related Topics

- [Constqualified variables](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#constqualified-variables)
