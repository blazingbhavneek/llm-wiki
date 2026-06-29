# CUDA Dynamic Parallelism (CDP1) Compiling and Linking

When compiling and linking CUDA programs that utilize Dynamic Parallelism (CDP1) using the NVIDIA CUDA Compiler (`nvcc`), the build process must interact with the device runtime library. The device runtime is provided as a static library, named `cudadevrt.lib` on Windows and `libcudadevrt.a` on Linux [CUDA_C_Programming_Guide:L14805-L14807].

## Automatic Linking

By default, when compiling and linking CUDA programs using dynamic parallelism with `nvcc`, the program will automatically link against the static device runtime library `libcudadevrt` [CUDA_C_Programming_Guide:L14801-L14803].

## Manual Linking

Although linking is often automatic, it is possible to explicitly link against the device runtime library. This can be accomplished through `nvcc` and/or `nvlink` [CUDA_C_Programming_Guide:L14807-L14809]. To manually link, the `-lcudadevrt` flag must be included in the compilation or linking command [CUDA_C_Programming_Guide:L14813-L14814].

## Compilation Examples

### Single-Step Compilation

A device runtime program may be compiled and linked in a single step if all required source files can be specified from the command line. This requires enabling relocatable device code with `-rdc=true` [CUDA_C_Programming_Guide:L14810-L14814]:

```shell
$ nvcc -arch=sm_75 -rdc=true hello_world.cu -o hello -lcudadevrt
```

### Two-Stage Compilation (Separate Compilation)

It is also possible to compile CUDA `.cu` source files into object files first, and then link them together in a two-stage process. This approach is useful for larger projects or when using separate compilation [CUDA_C_Programming_Guide:L14815-L14820]:

1. Compile the source file to an object file using the `-dc` flag (device compilation):
   ```shell
   $ nvcc -arch=sm_75 -dc hello_world.cu -o hello_world.o
   ```

2. Link the object file into the final executable, ensuring relocatable device code is enabled and the device runtime is linked:
   ```shell
   $ nvcc -arch=sm_75 -rdc=true hello_world.o -o hello -lcudadevrt
   ```

For more details on separate compilation, refer to the "Using Separate Compilation" section of The CUDA Driver Compiler NVCC guide [CUDA_C_Programming_Guide:L14821].

## Note on CDP2

This section pertains to CUDA Dynamic Parallelism version 1 (CDP1). For information regarding the CDP2 version of the document, see the "Compiling and Linking" section for CDP2 [CUDA_C_Programming_Guide:L14799-L14800].
