# CUDA Dynamic Parallelism Toolkit Support

Compiler and linker support for dynamic parallelism, including `nvcc` flags and library linking.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L14119-L14145

Citation: [CUDA_C_Programming_Guide:L14119-L14145]

````text

## 13.3.3. Toolkit Support for Dynamic Parallelism

## 13.3.3.1 Including Device Runtime API in CUDA Code

Similar to the host-side runtime API, prototypes for the CUDA device runtime API are included automatically during program compilation. There is no need to includecuda\_device\_runtime\_api.h explicitly.

## 13.3.3.2 Compiling and Linking

When compiling and linking CUDA programs using dynamic parallelism with nvcc, the program will automatically link against the static device runtime library libcudadevrt.

The device runtime is ofered as a static library (cudadevrt.lib on Windows, libcudadevrt.a under Linux), against which a GPU application that uses the device runtime must be linked. Linking of device libraries can be accomplished through nvcc and/or nvlink. Two simple examples are shown below.

A device runtime program may be compiled and linked in a single step, if all required source files can be specified from the command line:

```shell
$ nvcc -arch=sm_75 -rdc=true hello_world.cu -o hello -lcudadevrt
```

It is also possible to compile CUDA .cu source files first to object files, and then link these together in a two-stage process:

```shell
$ nvcc -arch=sm_75 -dc hello_world.cu -o hello_world.o
$ nvcc -arch=sm_75 -rdc=true hello_world.o -o hello -lcudadevrt
```

Please see the Using Separate Compilation section of The CUDA Driver Compiler NVCC guide for more details.
````
