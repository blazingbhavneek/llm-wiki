# CUDA Dynamic Parallelism Programming Guidelines

Programming guidelines, syntax, and a Hello World example for dynamic parallelism.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L14146-L14207

Citation: [CUDA_C_Programming_Guide:L14146-L14207]

````text

## 13.4. Programming Guidelines

## 13.4.1. Basics

The device runtime is a functional subset of the host runtime. API level device management, kernel launching, device memcpy, stream management, and event management are exposed from the device runtime.

Programming for the device runtime should be familiar to someone who already has experience with CUDA. Device runtime syntax and semantics are largely the same as that of the host API, with any exceptions detailed earlier in this document.

The following example shows a simple Hello World program incorporating dynamic parallelism:

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
}
```

(continues on next page)

(continued from previous page)

```cpp
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
````
