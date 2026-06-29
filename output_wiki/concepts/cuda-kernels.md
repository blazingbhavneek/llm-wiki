# CUDA Kernels

CUDA kernels are C++ functions that, when called, are executed N times in parallel by N different CUDA threads, as opposed to regular C++ functions which execute only once [CUDA_C_Programming_Guide:L833-L835].

## Definition and Syntax

A kernel is defined using the `__global__` declaration specifier [CUDA_C_Programming_Guide:L833-L835]. The number of CUDA threads that execute a kernel for a given call is specified using the `<<<...>>>` execution configuration syntax [CUDA_C_Programming_Guide:L833-L835].

Each thread that executes the kernel is assigned a unique thread ID, which is accessible within the kernel through built-in variables [CUDA_C_Programming_Guide:L833-L835].

## Example

The following example demonstrates a kernel definition and invocation:

```cpp
// Kernel definition
__global__ void VecAdd(float* A, float* B, float* C)
{
    int i = threadIdx.x;
    C[i] = A[i] + B[i];
}

int main()
{
    ...
    // Kernel invocation with N threads
    VecAdd<<<1, N>>>(A, B, C);
    ...
}
```

In this example, the `VecAdd` kernel is launched with an execution configuration of `<<<1, N>>>`, indicating that N threads will execute the function [CUDA_C_Programming_Guide:L839-L854]. Each thread computes the sum of corresponding elements from arrays A and B and stores the result in array C [CUDA_C_Programming_Guide:L839-L854].
