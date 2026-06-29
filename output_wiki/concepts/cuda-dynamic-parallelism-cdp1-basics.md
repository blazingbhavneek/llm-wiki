# CUDA Dynamic Parallelism (CDP1) Basics

CUDA Dynamic Parallelism (CDP1) enables device code to launch and synchronize with child kernels. This capability is provided through the device runtime, which exposes API-level functions for device management, kernel launching, device memory copies, stream management, and event management [CUDA_C_Programming_Guide:L14830-L14889].

## Device Runtime

The device runtime is a functional subset of the host runtime [CUDA_C_Programming_Guide:L14830-L14889]. Programming for the device runtime is designed to be familiar to those with experience in CUDA, as its syntax and semantics are largely the same as the host API [CUDA_C_Programming_Guide:L14830-L14889].

## Synchronization and Deprecation

Explicit synchronization with child kernels from a parent block, such as using `cudaDeviceSynchronize()` in device code, is deprecated in CUDA 11.6 [CUDA_C_Programming_Guide:L14830-L14889]. This feature is removed for compilation targeting compute capability 9.0 or higher and is slated for full removal in a future CUDA release [CUDA_C_Programming_Guide:L14830-L14889].

## Example: Hello World

The following example demonstrates a simple program incorporating dynamic parallelism, where a parent kernel launches a child kernel and waits for its completion.

```cpp
#include <stdio.h>

__global__ void childKernel()
{
    printf("Hello ");
}

__global__ void parentKernel()
{
    // launch child
    childKernel<<<1,1>>>();
    if (cudaSuccess != cudaGetLastError()) {
        return;
    }

    // wait for child to complete
    if (cudaSuccess != cudaDeviceSynchronize()) {
        return;
    }

    printf("World!\n");
}

int main(int argc, char *argv[])
{
    // launch parent
    parentKernel<<<1,1>>>();
    if (cudaSuccess != cudaGetLastError()) {
        return 1;
    }

    // wait for parent to complete
    if (cudaSuccess != cudaDeviceSynchronize()) {
        return 2;
    }

    return 0;
}
```

This program can be built in a single step using the NVIDIA CUDA Compiler (nvcc). The `-rdc=true` flag is required to enable relocatable device code, and `-lcudadevrt` links the device runtime library [CUDA_C_Programming_Guide:L14830-L14889].

```shell
$ nvcc -arch=sm_75 -rdc=true hello_world.cu -o hello -lcudadevrt
```
