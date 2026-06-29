# CUDA Programming Guidelines Basics

The device runtime is a functional subset of the host runtime. It exposes API-level device management, kernel launching, device memcpy, stream management, and event management directly from device code [CUDA_C_Programming_Guide:L14147-L14214].

Programming for the device runtime should be familiar to anyone with experience in CUDA. The syntax and semantics of the device runtime are largely the same as those of the host API, with specific exceptions detailed elsewhere in the documentation [CUDA_C_Programming_Guide:L14147-L14214].

## Dynamic Parallelism Example

The following example demonstrates a simple "Hello World" program that incorporates dynamic parallelism, where a parent kernel launches child kernels [CUDA_C_Programming_Guide:L14147-L14214].

```c
#include <stdio.h>

__global__ void childKernel()
{
    printf("Hello ");
}

__global__ void tailKernel()
{
    printf("World!\n");
}

__global__ void parentKernel()
{
    // launch child
    childKernel<<<1,1>>>();

    if (cudaSuccess != cudaGetLastError()) {
        return;
    }

    // launch tail into cudaStreamTailLaunch stream
    // implicitly synchronizes: waits for child to complete
    tailKernel<<<1,1,0,cudaStreamTailLaunch>>>();
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

This program can be built in a single step using the `nvcc` compiler with the `-rdc=true` flag to enable relocatable device code and linking against the device runtime library (`-lcudadevrt`) [CUDA_C_Programming_Guide:L14147-L14214].

```shell
$ nvcc -arch=sm_75 -rdc=true hello_world.cu -o hello -lcudadevrt
```
